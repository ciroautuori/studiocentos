"""
API Endpoints per il sistema Corsi ISS
Gestione completa corsi di formazione digitale GRATUITI
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.corso import (
    Corso, CorsoIscrizione, CorsoLezione, CorsoRecensione,
    CorsoStato, CorsoCategoria, CorsoLivello, CorsoModalita
)
from app.models.user import User
from app.schemas.corso import (
    CorsoCreate, CorsoUpdate, CorsoResponse, CorsoListResponse,
    CorsoStatsResponse, CorsoIscrizioneCreate, CorsoIscrizioneResponse,
    CorsoLezioneCreate, CorsoLezioneResponse, CorsoRecensioneCreate, CorsoRecensioneResponse
)
from app.core.config import settings
from app.utils.email import send_email
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=CorsoListResponse)
def get_corsi(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    categoria: Optional[CorsoCategoria] = None,
    livello: Optional[CorsoLivello] = None,
    modalita: Optional[CorsoModalita] = None,
    stato: Optional[CorsoStato] = None,
    search: Optional[str] = None,
    solo_iscrizioni_aperte: bool = False,
    solo_gratuiti: bool = True,
    sort_by: str = Query("created_at", regex="^(created_at|data_inizio|titolo|rating_medio|numero_iscritti)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista corsi con filtri avanzati
    """
    query = db.query(Corso)
    
    # Filtri base
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(Corso.pubblicato == True)
        query = query.filter(Corso.archiviato == False)
    
    # Filtri specifici
    if categoria:
        query = query.filter(Corso.categoria == categoria)
    if livello:
        query = query.filter(Corso.livello == livello)
    if modalita:
        query = query.filter(Corso.modalita == modalita)
    if stato:
        query = query.filter(Corso.stato == stato)
    if solo_iscrizioni_aperte:
        query = query.filter(Corso.iscrizioni_aperte == True)
    if solo_gratuiti:
        query = query.filter(Corso.gratuito == True)
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            Corso.titolo.ilike(f"%{search}%"),
            Corso.descrizione.ilike(f"%{search}%"),
            Corso.descrizione_breve.ilike(f"%{search}%"),
            Corso.competenze_acquisite.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Corso, sort_by)))
    else:
        query = query.order_by(asc(getattr(Corso, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    corsi = query.offset(skip).limit(limit).all()
    
    return CorsoListResponse(
        corsi=corsi,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=CorsoResponse)
def create_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_in: CorsoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea un nuovo corso (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per creare corsi"
        )
    
    # Genera codice corso univoco
    ultimo_corso = db.query(Corso).order_by(desc(Corso.id)).first()
    numero = (ultimo_corso.id + 1) if ultimo_corso else 1
    codice_corso = f"ISS-COR-{datetime.now().year}-{numero:03d}"
    
    # Crea corso
    corso = Corso(
        **corso_in.dict(),
        codice_corso=codice_corso,
        creato_da_user_id=current_user.id
    )
    
    db.add(corso)
    db.commit()
    db.refresh(corso)
    
    return corso


@router.get("/{corso_id}", response_model=CorsoResponse)
def get_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli corso specifico
    """
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if not corso.pubblicato or corso.archiviato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Corso non disponibile"
            )
    
    return corso


@router.put("/{corso_id}", response_model=CorsoResponse)
def update_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    corso_in: CorsoUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna corso esistente (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare corsi"
        )
    
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Aggiorna campi
    update_data = corso_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(corso, field, value)
    
    corso.modificato_da_user_id = current_user.id
    
    db.commit()
    db.refresh(corso)
    
    return corso


@router.delete("/{corso_id}")
def delete_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina corso (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per eliminare corsi"
        )
    
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica se ci sono iscrizioni attive
    iscrizioni_attive = db.query(CorsoIscrizione).filter(
        and_(
            CorsoIscrizione.corso_id == corso_id,
            CorsoIscrizione.stato == "attiva"
        )
    ).count()
    
    if iscrizioni_attive > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossibile eliminare corso con iscrizioni attive"
        )
    
    db.delete(corso)
    db.commit()
    
    return {"message": "Corso eliminato con successo"}


@router.post("/{corso_id}/iscrizioni", response_model=CorsoIscrizioneResponse)
def iscriviti_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Iscrizione a un corso
    """
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica disponibilità
    if not corso.iscrizioni_aperte:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Iscrizioni chiuse per questo corso"
        )
    
    if corso.is_full:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Corso al completo"
        )
    
    # Verifica iscrizione esistente
    iscrizione_esistente = db.query(CorsoIscrizione).filter(
        and_(
            CorsoIscrizione.corso_id == corso_id,
            CorsoIscrizione.user_id == current_user.id
        )
    ).first()
    
    if iscrizione_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sei già iscritto a questo corso"
        )
    
    # Crea iscrizione
    iscrizione = CorsoIscrizione(
        corso_id=corso_id,
        user_id=current_user.id
    )
    
    db.add(iscrizione)
    
    # Aggiorna contatore
    corso.numero_iscritti += 1
    
    db.commit()
    db.refresh(iscrizione)
    
    # Invia email di conferma
    try:
        send_email(
            to=current_user.email,
            subject=f"Iscrizione confermata: {corso.titolo}",
            template="corso_iscrizione_confermata",
            context={
                "user_name": current_user.nome,
                "corso_titolo": corso.titolo,
                "corso_data_inizio": corso.data_inizio,
                "corso_modalita": corso.modalita
            }
        )
    except Exception as e:
        # Log error ma non bloccare l'iscrizione
        print(f"Errore invio email: {e}")
    
    return iscrizione


@router.get("/{corso_id}/iscrizioni", response_model=List[CorsoIscrizioneResponse])
def get_iscrizioni_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista iscrizioni corso (solo admin o docente)
    """
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica permessi
    if current_user.ruolo not in ["admin"] and corso.creato_da_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per vedere le iscrizioni"
        )
    
    iscrizioni = db.query(CorsoIscrizione).filter(
        CorsoIscrizione.corso_id == corso_id
    ).all()
    
    return iscrizioni


@router.post("/{corso_id}/recensioni", response_model=CorsoRecensioneResponse)
def create_recensione_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    recensione_in: CorsoRecensioneCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea recensione per un corso
    """
    # Verifica iscrizione e completamento
    iscrizione = db.query(CorsoIscrizione).filter(
        and_(
            CorsoIscrizione.corso_id == corso_id,
            CorsoIscrizione.user_id == current_user.id,
            CorsoIscrizione.stato == "completata"
        )
    ).first()
    
    if not iscrizione:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Puoi recensire solo corsi che hai completato"
        )
    
    # Verifica recensione esistente
    recensione_esistente = db.query(CorsoRecensione).filter(
        and_(
            CorsoRecensione.corso_id == corso_id,
            CorsoRecensione.user_id == current_user.id
        )
    ).first()
    
    if recensione_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hai già recensito questo corso"
        )
    
    # Crea recensione
    recensione = CorsoRecensione(
        **recensione_in.dict(),
        corso_id=corso_id,
        user_id=current_user.id
    )
    
    db.add(recensione)
    db.commit()
    db.refresh(recensione)
    
    # Aggiorna rating medio corso
    avg_rating = db.query(func.avg(CorsoRecensione.rating)).filter(
        CorsoRecensione.corso_id == corso_id
    ).scalar()
    
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    corso.rating_medio = float(avg_rating) if avg_rating else None
    corso.numero_recensioni += 1
    
    db.commit()
    
    return recensione


@router.get("/{corso_id}/recensioni", response_model=List[CorsoRecensioneResponse])
def get_recensioni_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> Any:
    """
    Lista recensioni corso
    """
    recensioni = db.query(CorsoRecensione).filter(
        and_(
            CorsoRecensione.corso_id == corso_id,
            CorsoRecensione.pubblicata == True
        )
    ).order_by(desc(CorsoRecensione.created_at)).offset(skip).limit(limit).all()
    
    return recensioni


@router.get("/{corso_id}/stats", response_model=CorsoStatsResponse)
def get_stats_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Statistiche corso (solo admin o docente)
    """
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica permessi
    if current_user.ruolo not in ["admin"] and corso.creato_da_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per vedere le statistiche"
        )
    
    # Calcola statistiche
    stats = {
        "corso_id": corso_id,
        "numero_iscritti": corso.numero_iscritti,
        "numero_completati": corso.numero_completati,
        "tasso_completamento": float(corso.tasso_completamento) if corso.tasso_completamento else 0.0,
        "rating_medio": float(corso.rating_medio) if corso.rating_medio else 0.0,
        "numero_recensioni": corso.numero_recensioni,
        "posti_disponibili": corso.posti_disponibili
    }
    
    return CorsoStatsResponse(**stats)


@router.get("/categorie/stats")
def get_categorie_stats(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Statistiche per categoria di corso
    """
    stats = db.query(
        Corso.categoria,
        func.count(Corso.id).label("numero_corsi"),
        func.sum(Corso.numero_iscritti).label("totale_iscritti"),
        func.avg(Corso.rating_medio).label("rating_medio")
    ).filter(
        and_(
            Corso.pubblicato == True,
            Corso.archiviato == False
        )
    ).group_by(Corso.categoria).all()
    
    return [
        {
            "categoria": stat.categoria,
            "numero_corsi": stat.numero_corsi,
            "totale_iscritti": stat.totale_iscritti or 0,
            "rating_medio": float(stat.rating_medio) if stat.rating_medio else 0.0
        }
        for stat in stats
    ]


@router.post("/{corso_id}/lezioni", response_model=CorsoLezioneResponse)
def create_lezione(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    lezione_in: CorsoLezioneCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea lezione per un corso (solo admin o docente)
    """
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica permessi
    if current_user.ruolo not in ["admin"] and corso.creato_da_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per creare lezioni"
        )
    
    lezione = CorsoLezione(
        **lezione_in.dict(),
        corso_id=corso_id
    )
    
    db.add(lezione)
    db.commit()
    db.refresh(lezione)
    
    return lezione


@router.get("/{corso_id}/lezioni", response_model=List[CorsoLezioneResponse])
def get_lezioni_corso(
    *,
    db: Session = Depends(deps.get_db),
    corso_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Lista lezioni del corso
    """
    corso = db.query(Corso).filter(Corso.id == corso_id).first()
    if not corso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Corso non trovato"
        )
    
    # Verifica se l'utente è iscritto o è admin
    if current_user:
        iscrizione = db.query(CorsoIscrizione).filter(
            and_(
                CorsoIscrizione.corso_id == corso_id,
                CorsoIscrizione.user_id == current_user.id
            )
        ).first()
        
        if not iscrizione and current_user.ruolo != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Devi essere iscritto al corso per vedere le lezioni"
            )
    
    lezioni = db.query(CorsoLezione).filter(
        CorsoLezione.corso_id == corso_id
    ).order_by(CorsoLezione.numero_lezione).all()
    
    return lezioni
