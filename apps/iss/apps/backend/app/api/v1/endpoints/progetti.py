"""
API Endpoints per il sistema Progetti ISS
Gestione completa progetti di innovazione sociale
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.progetto import (
    Progetto, ProgettoTeamMember, ProgettoAggiornamento, ProgettoDocumento,
    ProgettoStato, ProgettoCategoria, ProgettoTipo, ProgettoVisibilita
)
from app.models.user import User
from app.schemas.progetto import (
    ProgettoCreate, ProgettoUpdate, ProgettoResponse, ProgettoListResponse,
    ProgettoTeamMemberCreate, ProgettoTeamMemberResponse,
    ProgettoAggiornamentoCreate, ProgettoAggiornamentoResponse,
    ProgettoDocumentoCreate, ProgettoDocumentoResponse,
    ProgettoStatsResponse, ProgettoSearchFilters
)
from app.core.config import settings
from app.utils.email import send_email
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=ProgettoListResponse)
def get_progetti(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    categoria: Optional[ProgettoCategoria] = None,
    tipo: Optional[ProgettoTipo] = None,
    stato: Optional[ProgettoStato] = None,
    visibilita: Optional[ProgettoVisibilita] = None,
    search: Optional[str] = None,
    solo_cerca_volontari: bool = False,
    solo_in_evidenza: bool = False,
    citta: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|data_inizio|nome|percentuale_completamento)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista progetti con filtri avanzati
    """
    query = db.query(Progetto)
    
    # Filtri visibilità
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(Progetto.pubblicato == True)
        query = query.filter(Progetto.archiviato == False)
        query = query.filter(Progetto.visibilita.in_([ProgettoVisibilita.PUBBLICO, ProgettoVisibilita.MEMBRI]))
    
    # Filtri specifici
    if categoria:
        query = query.filter(Progetto.categoria == categoria)
    if tipo:
        query = query.filter(Progetto.tipo == tipo)
    if stato:
        query = query.filter(Progetto.stato == stato)
    if visibilita and (current_user and current_user.ruolo == "admin"):
        query = query.filter(Progetto.visibilita == visibilita)
    if solo_cerca_volontari:
        query = query.filter(Progetto.cerca_volontari == True)
    if solo_in_evidenza:
        query = query.filter(Progetto.in_evidenza == True)
    if citta:
        query = query.filter(Progetto.citta.ilike(f"%{citta}%"))
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            Progetto.nome.ilike(f"%{search}%"),
            Progetto.descrizione.ilike(f"%{search}%"),
            Progetto.descrizione_breve.ilike(f"%{search}%"),
            Progetto.obiettivi.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Progetto, sort_by)))
    else:
        query = query.order_by(asc(getattr(Progetto, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    progetti = query.offset(skip).limit(limit).all()
    
    return ProgettoListResponse(
        progetti=progetti,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=ProgettoResponse)
def create_progetto(
    *,
    db: Session = Depends(deps.get_db),
    progetto_in: ProgettoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea un nuovo progetto (admin o utenti autorizzati)
    """
    if current_user.ruolo not in ["admin", "aps"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per creare progetti"
        )
    
    # Genera codice progetto univoco
    ultimo_progetto = db.query(Progetto).order_by(desc(Progetto.id)).first()
    numero = (ultimo_progetto.id + 1) if ultimo_progetto else 1
    codice_progetto = f"ISS-PRJ-{datetime.now().year}-{numero:03d}"
    
    # Crea progetto
    progetto = Progetto(
        **progetto_in.dict(),
        codice_progetto=codice_progetto,
        creato_da_user_id=current_user.id,
        project_manager_id=current_user.id  # Il creatore è il PM iniziale
    )
    
    db.add(progetto)
    db.commit()
    db.refresh(progetto)
    
    # Aggiungi il creatore come team member
    team_member = ProgettoTeamMember(
        progetto_id=progetto.id,
        user_id=current_user.id,
        ruolo="project_manager",
        responsabilita="Gestione generale del progetto"
    )
    db.add(team_member)
    db.commit()
    
    return progetto


@router.get("/{progetto_id}", response_model=ProgettoResponse)
def get_progetto(
    *,
    db: Session = Depends(deps.get_db),
    progetto_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli progetto specifico
    """
    progetto = db.query(Progetto).filter(Progetto.id == progetto_id).first()
    
    if not progetto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progetto non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if not progetto.pubblicato or progetto.archiviato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Progetto non disponibile"
            )
        
        # Verifica livello di visibilità
        if progetto.visibilita == ProgettoVisibilita.PRIVATO:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Progetto privato"
            )
        
        if progetto.visibilita == ProgettoVisibilita.TEAM:
            # Verifica se l'utente fa parte del team
            is_team_member = db.query(ProgettoTeamMember).filter(
                and_(
                    ProgettoTeamMember.progetto_id == progetto_id,
                    ProgettoTeamMember.user_id == current_user.id,
                    ProgettoTeamMember.attivo == True
                )
            ).first()
            
            if not is_team_member:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Accesso riservato al team del progetto"
                )
    
    return progetto


@router.put("/{progetto_id}", response_model=ProgettoResponse)
def update_progetto(
    *,
    db: Session = Depends(deps.get_db),
    progetto_id: int,
    progetto_in: ProgettoUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna progetto esistente (admin o project manager)
    """
    progetto = db.query(Progetto).filter(Progetto.id == progetto_id).first()
    if not progetto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progetto non trovato"
        )
    
    # Verifica permessi
    if (current_user.ruolo != "admin" and 
        progetto.project_manager_id != current_user.id and
        progetto.creato_da_user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare questo progetto"
        )
    
    # Aggiorna campi
    update_data = progetto_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(progetto, field, value)
    
    progetto.modificato_da_user_id = current_user.id
    
    db.commit()
    db.refresh(progetto)
    
    return progetto


@router.delete("/{progetto_id}")
def delete_progetto(
    *,
    db: Session = Depends(deps.get_db),
    progetto_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina progetto (solo admin o creatore)
    """
    progetto = db.query(Progetto).filter(Progetto.id == progetto_id).first()
    if not progetto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progetto non trovato"
        )
    
    # Verifica permessi
    if (current_user.ruolo != "admin" and 
        progetto.creato_da_user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per eliminare questo progetto"
        )
    
    # Verifica se il progetto è in corso
    if progetto.stato == ProgettoStato.IN_CORSO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossibile eliminare progetto in corso. Archivialo prima."
        )
    
    db.delete(progetto)
    db.commit()
    
    return {"message": "Progetto eliminato con successo"}


@router.post("/{progetto_id}/partecipa")
def richiedi_partecipazione(
    *,
    db: Session = Depends(deps.get_db),
    progetto_id: int,
    ruolo_richiesto: str,
    motivazione: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Richiedi partecipazione a un progetto
    """
    progetto = db.query(Progetto).filter(Progetto.id == progetto_id).first()
    if not progetto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progetto non trovato"
        )
    
    if not progetto.cerca_volontari:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questo progetto non cerca volontari al momento"
        )
    
    # Verifica se già nel team
    existing_member = db.query(ProgettoTeamMember).filter(
        and_(
            ProgettoTeamMember.progetto_id == progetto_id,
            ProgettoTeamMember.user_id == current_user.id,
            ProgettoTeamMember.attivo == True
        )
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sei già membro di questo progetto"
        )
    
    return {"message": "Richiesta di partecipazione inviata con successo"}
