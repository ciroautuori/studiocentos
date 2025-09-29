"""
API Endpoints per il sistema Volontariato ISS
Gestione completa opportunità, candidature e attività di volontariato
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.volontariato import (
    OpportunitaVolontariato, VolontariatoCandidatura, VolontariatoAttivita,
    VolontariatoCertificato, VolontariatoSkill,
    VolontariatoArea, VolontariatoTipo, VolontariatoModalita, 
    VolontariatoLivello, VolontariatoStato, VolontariatoUrgenza
)
from app.models.user import User
from app.schemas.volontariato import (
    OpportunitaVolontariatoCreate, OpportunitaVolontariatoUpdate, OpportunitaVolontariatoResponse,
    OpportunitaVolontariatoListResponse, VolontariatoCandidaturaCreate, VolontariatoCandidaturaResponse,
    VolontariatoAttivitaCreate, VolontariatoAttivitaResponse,
    VolontariatoCertificatoResponse, VolontariatoSkillCreate, VolontariatoSkillResponse,
    VolontariatoStatsResponse, VolontariatoMatchResponse
)
from app.core.config import settings
from app.utils.email import send_email
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/opportunita", response_model=OpportunitaVolontariatoListResponse)
def get_opportunita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    area: Optional[VolontariatoArea] = None,
    tipo: Optional[VolontariatoTipo] = None,
    modalita: Optional[VolontariatoModalita] = None,
    livello: Optional[VolontariatoLivello] = None,
    urgenza: Optional[VolontariatoUrgenza] = None,
    stato: Optional[VolontariatoStato] = None,
    search: Optional[str] = None,
    solo_candidature_aperte: bool = True,
    citta: Optional[str] = None,
    remoto_disponibile: Optional[bool] = None,
    sort_by: str = Query("created_at", regex="^(created_at|data_inizio_prevista|urgenza|titolo)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista opportunità di volontariato con filtri avanzati
    """
    query = db.query(OpportunitaVolontariato)
    
    # Filtri base
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(OpportunitaVolontariato.pubblicata == True)
        query = query.filter(OpportunitaVolontariato.archiviata == False)
        query = query.filter(OpportunitaVolontariato.stato == VolontariatoStato.ATTIVA)
    
    # Filtri specifici
    if area:
        query = query.filter(OpportunitaVolontariato.area == area)
    if tipo:
        query = query.filter(OpportunitaVolontariato.tipo == tipo)
    if modalita:
        query = query.filter(OpportunitaVolontariato.modalita == modalita)
    if livello:
        query = query.filter(OpportunitaVolontariato.livello_richiesto == livello)
    if urgenza:
        query = query.filter(OpportunitaVolontariato.urgenza == urgenza)
    if stato and (current_user and current_user.ruolo == "admin"):
        query = query.filter(OpportunitaVolontariato.stato == stato)
    if solo_candidature_aperte:
        query = query.filter(OpportunitaVolontariato.candidature_aperte == True)
    if citta:
        query = query.filter(OpportunitaVolontariato.citta.ilike(f"%{citta}%"))
    if remoto_disponibile is not None:
        query = query.filter(OpportunitaVolontariato.possibilita_remoto == remoto_disponibile)
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            OpportunitaVolontariato.titolo.ilike(f"%{search}%"),
            OpportunitaVolontariato.descrizione.ilike(f"%{search}%"),
            OpportunitaVolontariato.descrizione_breve.ilike(f"%{search}%"),
            OpportunitaVolontariato.competenze_richieste.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(OpportunitaVolontariato, sort_by)))
    else:
        query = query.order_by(asc(getattr(OpportunitaVolontariato, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    opportunita = query.offset(skip).limit(limit).all()
    
    return OpportunitaVolontariatoListResponse(
        opportunita=opportunita,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/opportunita", response_model=OpportunitaVolontariatoResponse)
def create_opportunita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    opportunita_in: OpportunitaVolontariatoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea nuova opportunità di volontariato (admin o APS)
    """
    if current_user.ruolo not in ["admin", "aps"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per creare opportunità di volontariato"
        )
    
    # Genera codice opportunità univoco
    ultima_opportunita = db.query(OpportunitaVolontariato).order_by(desc(OpportunitaVolontariato.id)).first()
    numero = (ultima_opportunita.id + 1) if ultima_opportunita else 1
    codice_opportunita = f"ISS-VOL-{datetime.now().year}-{numero:03d}"
    
    # Crea opportunità
    opportunita = OpportunitaVolontariato(
        **opportunita_in.dict(),
        codice_opportunita=codice_opportunita,
        creato_da_user_id=current_user.id,
        responsabile_id=current_user.id
    )
    
    db.add(opportunita)
    db.commit()
    db.refresh(opportunita)
    
    return opportunita


@router.get("/opportunita/{opportunita_id}", response_model=OpportunitaVolontariatoResponse)
def get_opportunita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    opportunita_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli opportunità specifica
    """
    opportunita = db.query(OpportunitaVolontariato).filter(
        OpportunitaVolontariato.id == opportunita_id
    ).first()
    
    if not opportunita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunità non trovata"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if not opportunita.pubblicata or opportunita.archiviata:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Opportunità non disponibile"
            )
    
    return opportunita


@router.put("/opportunita/{opportunita_id}", response_model=OpportunitaVolontariatoResponse)
def update_opportunita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    opportunita_id: int,
    opportunita_in: OpportunitaVolontariatoUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna opportunità di volontariato (admin o responsabile)
    """
    opportunita = db.query(OpportunitaVolontariato).filter(
        OpportunitaVolontariato.id == opportunita_id
    ).first()
    
    if not opportunita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunità non trovata"
        )
    
    # Verifica permessi
    if (current_user.ruolo != "admin" and 
        opportunita.responsabile_id != current_user.id and
        opportunita.creato_da_user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare questa opportunità"
        )
    
    # Aggiorna campi
    update_data = opportunita_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(opportunita, field, value)
    
    opportunita.modificato_da_user_id = current_user.id
    
    db.commit()
    db.refresh(opportunita)
    
    return opportunita


@router.delete("/opportunita/{opportunita_id}")
def delete_opportunita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    opportunita_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina opportunità di volontariato (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono eliminare opportunità"
        )
    
    opportunita = db.query(OpportunitaVolontariato).filter(
        OpportunitaVolontariato.id == opportunita_id
    ).first()
    
    if not opportunita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunità non trovata"
        )
    
    # Verifica se ci sono candidature
    candidature = db.query(VolontariatoCandidatura).filter(
        VolontariatoCandidatura.opportunita_id == opportunita_id
    ).count()
    
    if candidature > 0:
        # Non eliminare, ma archivia
        opportunita.archiviata = True
        opportunita.stato = VolontariatoStato.ARCHIVIATA
        db.commit()
        return {"message": "Opportunità archiviata (aveva candidature)"}
    
    db.delete(opportunita)
    db.commit()
    
    return {"message": "Opportunità eliminata con successo"}


@router.post("/opportunita/{opportunita_id}/candidature", response_model=VolontariatoCandidaturaResponse)
def candidati_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    opportunita_id: int,
    candidatura_in: VolontariatoCandidaturaCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Candidatura per opportunità di volontariato
    """
    opportunita = db.query(OpportunitaVolontariato).filter(
        OpportunitaVolontariato.id == opportunita_id
    ).first()
    
    if not opportunita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunità non trovata"
        )
    
    # Verifica disponibilità
    if not opportunita.candidature_aperte:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Candidature chiuse per questa opportunità"
        )
    
    if opportunita.is_full:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Opportunità al completo"
        )
    
    # Verifica candidatura esistente
    candidatura_esistente = db.query(VolontariatoCandidatura).filter(
        and_(
            VolontariatoCandidatura.opportunita_id == opportunita_id,
            VolontariatoCandidatura.user_id == current_user.id
        )
    ).first()
    
    if candidatura_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hai già inviato una candidatura per questa opportunità"
        )
    
    # Crea candidatura
    candidatura = VolontariatoCandidatura(
        **candidatura_in.dict(),
        opportunita_id=opportunita_id,
        user_id=current_user.id
    )
    
    db.add(candidatura)
    
    # Aggiorna contatore
    opportunita.numero_candidature += 1
    
    db.commit()
    db.refresh(candidatura)
    
    # Invia email di conferma
    try:
        send_email(
            to=current_user.email,
            subject=f"Candidatura inviata: {opportunita.titolo}",
            template="volontariato_candidatura_inviata",
            context={
                "user_name": current_user.nome,
                "opportunita_titolo": opportunita.titolo,
                "opportunita_area": opportunita.area,
                "data_candidatura": candidatura.data_candidatura
            }
        )
        
        # Notifica al responsabile
        if opportunita.responsabile:
            send_email(
                to=opportunita.responsabile.email,
                subject=f"Nuova candidatura: {opportunita.titolo}",
                template="volontariato_nuova_candidatura",
                context={
                    "responsabile_name": opportunita.responsabile.nome,
                    "opportunita_titolo": opportunita.titolo,
                    "candidato_nome": f"{current_user.nome} {current_user.cognome}",
                    "candidatura_url": f"{settings.FRONTEND_URL}/volontariato/candidature/{candidatura.id}"
                }
            )
    except Exception as e:
        print(f"Errore invio email: {e}")
    
    return candidatura


@router.get("/opportunita/{opportunita_id}/candidature", response_model=List[VolontariatoCandidaturaResponse])
def get_candidature_opportunita(
    *,
    db: Session = Depends(deps.get_db),
    opportunita_id: int,
    stato: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista candidature per opportunità (admin o responsabile)
    """
    opportunita = db.query(OpportunitaVolontariato).filter(
        OpportunitaVolontariato.id == opportunita_id
    ).first()
    
    if not opportunita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunità non trovata"
        )
    
    # Verifica permessi
    if (current_user.ruolo not in ["admin"] and 
        opportunita.responsabile_id != current_user.id and
        opportunita.creato_da_user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per vedere le candidature"
        )
    
    query = db.query(VolontariatoCandidatura).filter(
        VolontariatoCandidatura.opportunita_id == opportunita_id
    )
    
    if stato:
        query = query.filter(VolontariatoCandidatura.stato == stato)
    
    candidature = query.order_by(desc(VolontariatoCandidatura.data_candidatura)).all()
    
    return candidature


@router.put("/candidature/{candidatura_id}/stato")
def update_stato_candidatura(
    *,
    db: Session = Depends(deps.get_db),
    candidatura_id: int,
    nuovo_stato: str,
    motivo: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna stato candidatura (admin o responsabile)
    """
    candidatura = db.query(VolontariatoCandidatura).filter(
        VolontariatoCandidatura.id == candidatura_id
    ).first()
    
    if not candidatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidatura non trovata"
        )
    
    # Verifica permessi
    if (current_user.ruolo not in ["admin"] and 
        candidatura.opportunita.responsabile_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare questa candidatura"
        )
    
    candidatura.stato = nuovo_stato
    candidatura.data_risposta = datetime.now()
    
    if nuovo_stato == "rifiutata" and motivo:
        candidatura.motivo_rifiuto = motivo
    
    # Se selezionata, aggiorna contatori
    if nuovo_stato == "selezionata":
        candidatura.opportunita.numero_volontari_selezionati += 1
    
    db.commit()
    
    # Invia notifica al candidato
    try:
        template = f"volontariato_candidatura_{nuovo_stato}"
        send_email(
            to=candidatura.user.email,
            subject=f"Aggiornamento candidatura: {candidatura.opportunita.titolo}",
            template=template,
            context={
                "user_name": candidatura.user.nome,
                "opportunita_titolo": candidatura.opportunita.titolo,
                "stato": nuovo_stato,
                "motivo": motivo
            }
        )
    except Exception as e:
        print(f"Errore invio email: {e}")
    
    return {"message": f"Stato candidatura aggiornato a: {nuovo_stato}"}


@router.post("/attivita", response_model=VolontariatoAttivitaResponse)
def registra_attivita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    attivita_in: VolontariatoAttivitaCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Registra attività di volontariato svolta
    """
    # Verifica che la candidatura appartenga all'utente
    candidatura = db.query(VolontariatoCandidatura).filter(
        and_(
            VolontariatoCandidatura.id == attivita_in.candidatura_id,
            VolontariatoCandidatura.user_id == current_user.id,
            VolontariatoCandidatura.stato == "selezionata"
        )
    ).first()
    
    if not candidatura:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidatura non trovata o non selezionata"
        )
    
    # Crea attività
    attivita = VolontariatoAttivita(
        **attivita_in.dict()
    )
    
    db.add(attivita)
    db.commit()
    db.refresh(attivita)
    
    return attivita


@router.get("/attivita/mie", response_model=List[VolontariatoAttivitaResponse])
def get_mie_attivita_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista attività di volontariato dell'utente corrente
    """
    attivita = db.query(VolontariatoAttivita).join(VolontariatoCandidatura).filter(
        VolontariatoCandidatura.user_id == current_user.id
    ).order_by(desc(VolontariatoAttivita.data_attivita)).offset(skip).limit(limit).all()
    
    return attivita


@router.get("/certificati/miei", response_model=List[VolontariatoCertificatoResponse])
def get_miei_certificati_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista certificati di volontariato dell'utente corrente
    """
    certificati = db.query(VolontariatoCertificato).filter(
        VolontariatoCertificato.user_id == current_user.id
    ).order_by(desc(VolontariatoCertificato.data_rilascio)).all()
    
    return certificati


@router.post("/skills", response_model=VolontariatoSkillResponse)
def add_skill_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    skill_in: VolontariatoSkillCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiungi competenza di volontariato
    """
    # Verifica se la skill esiste già
    existing_skill = db.query(VolontariatoSkill).filter(
        and_(
            VolontariatoSkill.user_id == current_user.id,
            VolontariatoSkill.nome_competenza == skill_in.nome_competenza
        )
    ).first()
    
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hai già aggiunto questa competenza"
        )
    
    skill = VolontariatoSkill(
        **skill_in.dict(),
        user_id=current_user.id
    )
    
    db.add(skill)
    db.commit()
    db.refresh(skill)
    
    return skill


@router.get("/skills/mie", response_model=List[VolontariatoSkillResponse])
def get_mie_skills_volontariato(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista competenze di volontariato dell'utente corrente
    """
    skills = db.query(VolontariatoSkill).filter(
        VolontariatoSkill.user_id == current_user.id
    ).order_by(VolontariatoSkill.nome_competenza).all()
    
    return skills


@router.get("/match/{user_id}", response_model=List[VolontariatoMatchResponse])
def get_opportunita_match(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Trova opportunità di volontariato che matchano con le skills dell'utente
    """
    # Verifica permessi
    if current_user.id != user_id and current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non puoi vedere i match di altri utenti"
        )
    
    # Ottieni skills dell'utente
    user_skills = db.query(VolontariatoSkill).filter(
        VolontariatoSkill.user_id == user_id
    ).all()
    
    if not user_skills:
        return []
    
    # Logica di matching semplificata (in produzione si userebbe un algoritmo più sofisticato)
    skill_names = [skill.nome_competenza.lower() for skill in user_skills]
    skill_categories = [skill.categoria.lower() for skill in user_skills]
    
    opportunita = db.query(OpportunitaVolontariato).filter(
        and_(
            OpportunitaVolontariato.pubblicata == True,
            OpportunitaVolontariato.candidature_aperte == True,
            OpportunitaVolontariato.stato == VolontariatoStato.ATTIVA
        )
    ).all()
    
    matches = []
    for opp in opportunita:
        match_score = 0
        
        # Verifica se già candidato
        already_applied = db.query(VolontariatoCandidatura).filter(
            and_(
                VolontariatoCandidatura.opportunita_id == opp.id,
                VolontariatoCandidatura.user_id == user_id
            )
        ).first()
        
        if already_applied:
            continue
        
        # Calcola punteggio di match basato su competenze richieste
        if opp.competenze_richieste:
            competenze_richieste = opp.competenze_richieste.lower()
            for skill_name in skill_names:
                if skill_name in competenze_richieste:
                    match_score += 10
            
            for category in skill_categories:
                if category in competenze_richieste:
                    match_score += 5
        
        # Bonus per area di interesse
        if opp.area.value in [skill.categoria for skill in user_skills]:
            match_score += 15
        
        if match_score > 0:
            matches.append(VolontariatoMatchResponse(
                opportunita=opp,
                match_score=match_score,
                motivi_match=[
                    "Competenze compatibili",
                    "Area di interesse"
                ]
            ))
    
    # Ordina per punteggio di match
    matches.sort(key=lambda x: x.match_score, reverse=True)
    
    return matches[:limit]


@router.get("/stats/aree")
def get_stats_aree_volontariato(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Statistiche per area di volontariato
    """
    stats = db.query(
        OpportunitaVolontariato.area,
        func.count(OpportunitaVolontariato.id).label("numero_opportunita"),
        func.sum(OpportunitaVolontariato.numero_candidature).label("totale_candidature"),
        func.sum(OpportunitaVolontariato.numero_volontari_selezionati).label("totale_selezionati")
    ).filter(
        and_(
            OpportunitaVolontariato.pubblicata == True,
            OpportunitaVolontariato.archiviata == False
        )
    ).group_by(OpportunitaVolontariato.area).all()
    
    return [
        {
            "area": stat.area,
            "numero_opportunita": stat.numero_opportunita,
            "totale_candidature": stat.totale_candidature or 0,
            "totale_selezionati": stat.totale_selezionati or 0
        }
        for stat in stats
    ]
