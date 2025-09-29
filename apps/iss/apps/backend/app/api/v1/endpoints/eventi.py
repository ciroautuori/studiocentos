"""
API Endpoints per il sistema Eventi ISS
Gestione completa eventi, workshop e attività GRATUITE e accessibili
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.evento import (
    Evento, EventoIscrizione, EventoCheckIn, EventoRecensione,
    EventoStato, EventoTipo, EventoCategoria, EventoModalita, EventoTarget
)
from app.models.user import User
from app.schemas.evento import (
    EventoCreate, EventoUpdate, EventoResponse, EventoListResponse,
    EventoIscrizioneCreate, EventoIscrizioneResponse,
    EventoCheckInResponse, EventoRecensioneCreate, EventoRecensioneResponse,
    EventoStatsResponse, EventoCalendarResponse
)
from app.core.config import settings
from app.utils.email import send_email
from app.utils.qr_code import generate_qr_code
from datetime import datetime, timedelta
import uuid

router = APIRouter()


@router.get("/", response_model=EventoListResponse)
def get_eventi(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[EventoTipo] = None,
    categoria: Optional[EventoCategoria] = None,
    modalita: Optional[EventoModalita] = None,
    target: Optional[EventoTarget] = None,
    stato: Optional[EventoStato] = None,
    search: Optional[str] = None,
    solo_iscrizioni_aperte: bool = False,
    solo_gratuiti: bool = True,
    data_da: Optional[datetime] = None,
    data_a: Optional[datetime] = None,
    citta: Optional[str] = None,
    sort_by: str = Query("data_inizio", regex="^(data_inizio|created_at|titolo|numero_iscritti)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista eventi con filtri avanzati
    """
    query = db.query(Evento)
    
    # Filtri base
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(Evento.pubblicato == True)
        query = query.filter(Evento.archiviato == False)
    
    # Filtri specifici
    if tipo:
        query = query.filter(Evento.tipo == tipo)
    if categoria:
        query = query.filter(Evento.categoria == categoria)
    if modalita:
        query = query.filter(Evento.modalita == modalita)
    if target:
        query = query.filter(Evento.target == target)
    if stato:
        query = query.filter(Evento.stato == stato)
    if solo_iscrizioni_aperte:
        query = query.filter(Evento.iscrizioni_aperte == True)
    if solo_gratuiti:
        query = query.filter(Evento.gratuito == True)
    if citta:
        query = query.filter(Evento.citta.ilike(f"%{citta}%"))
    
    # Filtri data
    if data_da:
        query = query.filter(Evento.data_inizio >= data_da)
    if data_a:
        query = query.filter(Evento.data_fine <= data_a)
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            Evento.titolo.ilike(f"%{search}%"),
            Evento.descrizione.ilike(f"%{search}%"),
            Evento.descrizione_breve.ilike(f"%{search}%"),
            Evento.organizzatore_principale.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Evento, sort_by)))
    else:
        query = query.order_by(asc(getattr(Evento, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    eventi = query.offset(skip).limit(limit).all()
    
    return EventoListResponse(
        eventi=eventi,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=EventoResponse)
def create_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_in: EventoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea un nuovo evento (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per creare eventi"
        )
    
    # Genera codice evento univoco
    ultimo_evento = db.query(Evento).order_by(desc(Evento.id)).first()
    numero = (ultimo_evento.id + 1) if ultimo_evento else 1
    codice_evento = f"ISS-EVT-{datetime.now().year}-{numero:03d}"
    
    # Crea evento
    evento = Evento(
        **evento_in.dict(),
        codice_evento=codice_evento,
        creato_da_user_id=current_user.id
    )
    
    db.add(evento)
    db.commit()
    db.refresh(evento)
    
    return evento


@router.get("/{evento_id}", response_model=EventoResponse)
def get_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli evento specifico
    """
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if not evento.pubblicato or evento.archiviato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento non disponibile"
            )
    
    return evento


@router.put("/{evento_id}", response_model=EventoResponse)
def update_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    evento_in: EventoUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna evento esistente (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare eventi"
        )
    
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    # Aggiorna campi
    update_data = evento_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(evento, field, value)
    
    evento.modificato_da_user_id = current_user.id
    
    db.commit()
    db.refresh(evento)
    
    return evento


@router.delete("/{evento_id}")
def delete_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina evento (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per eliminare eventi"
        )
    
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    # Verifica se ci sono iscrizioni
    iscrizioni = db.query(EventoIscrizione).filter(
        EventoIscrizione.evento_id == evento_id
    ).count()
    
    if iscrizioni > 0:
        # Non eliminare, ma archivia
        evento.archiviato = True
        db.commit()
        return {"message": "Evento archiviato (aveva iscrizioni)"}
    
    db.delete(evento)
    db.commit()
    
    return {"message": "Evento eliminato con successo"}


@router.post("/{evento_id}/iscrizioni", response_model=EventoIscrizioneResponse)
def iscriviti_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    iscrizione_in: EventoIscrizioneCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Iscrizione a un evento
    """
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    # Verifica disponibilità
    if not evento.iscrizioni_aperte:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Iscrizioni chiuse per questo evento"
        )
    
    if evento.is_full:
        if not evento.lista_attesa:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Evento al completo e lista d'attesa non disponibile"
            )
    
    # Verifica iscrizione esistente
    iscrizione_esistente = db.query(EventoIscrizione).filter(
        and_(
            EventoIscrizione.evento_id == evento_id,
            EventoIscrizione.user_id == current_user.id
        )
    ).first()
    
    if iscrizione_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sei già iscritto a questo evento"
        )
    
    # Determina stato iscrizione
    stato = "confermata"
    if evento.is_full and evento.lista_attesa:
        stato = "lista_attesa"
    
    # Crea iscrizione
    iscrizione = EventoIscrizione(
        evento_id=evento_id,
        user_id=current_user.id,
        stato=stato,
        **iscrizione_in.dict()
    )
    
    db.add(iscrizione)
    
    # Aggiorna contatore solo se confermata
    if stato == "confermata":
        evento.numero_iscritti += 1
    
    db.commit()
    db.refresh(iscrizione)
    
    # Invia email di conferma
    try:
        template = "evento_iscrizione_confermata" if stato == "confermata" else "evento_lista_attesa"
        status_text = "confermata" if stato == "confermata" else "in lista d'attesa"
        send_email(
            to=current_user.email,
            subject=f"Iscrizione {status_text}: {evento.titolo}",
            template=template,
            context={
                "user_name": current_user.nome,
                "evento_titolo": evento.titolo,
                "evento_data": evento.data_inizio,
                "evento_modalita": evento.modalita,
                "evento_sede": evento.sede if evento.is_in_presenza else None,
                "evento_link": evento.link_evento if evento.is_online else None
            }
        )
    except Exception as e:
        print(f"Errore invio email: {e}")
    
    return iscrizione


@router.get("/{evento_id}/iscrizioni", response_model=List[EventoIscrizioneResponse])
def get_iscrizioni_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    stato: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista iscrizioni evento (solo admin o organizzatore)
    """
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    # Verifica permessi
    if current_user.ruolo not in ["admin"] and evento.creato_da_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per vedere le iscrizioni"
        )
    
    query = db.query(EventoIscrizione).filter(EventoIscrizione.evento_id == evento_id)
    
    if stato:
        query = query.filter(EventoIscrizione.stato == stato)
    
    iscrizioni = query.all()
    return iscrizioni


@router.post("/{evento_id}/check-in/{user_id}", response_model=EventoCheckInResponse)
def check_in_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Check-in partecipante evento
    """
    # Verifica permessi (admin o organizzatore)
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    if current_user.ruolo not in ["admin"] and evento.creato_da_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per fare check-in"
        )
    
    # Verifica iscrizione
    iscrizione = db.query(EventoIscrizione).filter(
        and_(
            EventoIscrizione.evento_id == evento_id,
            EventoIscrizione.user_id == user_id,
            EventoIscrizione.stato == "confermata"
        )
    ).first()
    
    if not iscrizione:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Iscrizione non trovata o non confermata"
        )
    
    # Verifica check-in esistente
    check_in_esistente = db.query(EventoCheckIn).filter(
        and_(
            EventoCheckIn.evento_id == evento_id,
            EventoCheckIn.user_id == user_id
        )
    ).first()
    
    if check_in_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-in già effettuato"
        )
    
    # Crea check-in
    check_in = EventoCheckIn(
        evento_id=evento_id,
        user_id=user_id,
        metodo_check_in="manuale"
    )
    
    db.add(check_in)
    
    # Aggiorna iscrizione
    iscrizione.check_in_effettuato = True
    iscrizione.data_check_in = datetime.now()
    
    db.commit()
    db.refresh(check_in)
    
    return check_in


@router.get("/{evento_id}/qr-code/{user_id}")
def get_qr_code_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Genera QR code per check-in evento
    """
    # Verifica che l'utente possa accedere al QR (se stesso o admin)
    if current_user.id != user_id and current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non puoi accedere a questo QR code"
        )
    
    # Verifica iscrizione
    iscrizione = db.query(EventoIscrizione).filter(
        and_(
            EventoIscrizione.evento_id == evento_id,
            EventoIscrizione.user_id == user_id,
            EventoIscrizione.stato == "confermata"
        )
    ).first()
    
    if not iscrizione:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Iscrizione non trovata"
        )
    
    # Genera token univoco per check-in
    token = str(uuid.uuid4())
    
    # Salva token temporaneo (potresti usare Redis per questo)
    # Per ora lo includiamo nel QR code
    
    qr_data = f"{settings.API_V1_STR}/eventi/{evento_id}/check-in-qr?token={token}&user_id={user_id}"
    
    qr_code_image = generate_qr_code(qr_data)
    
    return {"qr_code": qr_code_image, "token": token}


@router.post("/{evento_id}/recensioni", response_model=EventoRecensioneResponse)
def create_recensione_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    recensione_in: EventoRecensioneCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea recensione per un evento
    """
    # Verifica partecipazione
    iscrizione = db.query(EventoIscrizione).filter(
        and_(
            EventoIscrizione.evento_id == evento_id,
            EventoIscrizione.user_id == current_user.id,
            EventoIscrizione.partecipato == True
        )
    ).first()
    
    if not iscrizione:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Puoi recensire solo eventi a cui hai partecipato"
        )
    
    # Verifica recensione esistente
    recensione_esistente = db.query(EventoRecensione).filter(
        and_(
            EventoRecensione.evento_id == evento_id,
            EventoRecensione.user_id == current_user.id
        )
    ).first()
    
    if recensione_esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hai già recensito questo evento"
        )
    
    # Crea recensione
    recensione = EventoRecensione(
        **recensione_in.dict(),
        evento_id=evento_id,
        user_id=current_user.id
    )
    
    db.add(recensione)
    db.commit()
    db.refresh(recensione)
    
    # Aggiorna rating medio evento
    avg_rating = db.query(func.avg(EventoRecensione.rating)).filter(
        EventoRecensione.evento_id == evento_id
    ).scalar()
    
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    evento.rating_medio = float(avg_rating) if avg_rating else None
    evento.numero_recensioni += 1
    
    db.commit()
    
    return recensione


@router.get("/{evento_id}/recensioni", response_model=List[EventoRecensioneResponse])
def get_recensioni_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> Any:
    """
    Lista recensioni evento
    """
    recensioni = db.query(EventoRecensione).filter(
        and_(
            EventoRecensione.evento_id == evento_id,
            EventoRecensione.pubblicata == True
        )
    ).order_by(desc(EventoRecensione.created_at)).offset(skip).limit(limit).all()
    
    return recensioni


@router.get("/{evento_id}/stats", response_model=EventoStatsResponse)
def get_stats_evento(
    *,
    db: Session = Depends(deps.get_db),
    evento_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Statistiche evento (solo admin o organizzatore)
    """
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento non trovato"
        )
    
    # Verifica permessi
    if current_user.ruolo not in ["admin"] and evento.creato_da_user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per vedere le statistiche"
        )
    
    # Calcola statistiche
    stats = {
        "evento_id": evento_id,
        "numero_iscritti": evento.numero_iscritti,
        "numero_partecipanti_effettivi": evento.numero_partecipanti_effettivi,
        "tasso_partecipazione": (evento.numero_partecipanti_effettivi / evento.numero_iscritti * 100) if evento.numero_iscritti > 0 else 0.0,
        "rating_medio": float(evento.rating_medio) if evento.rating_medio else 0.0,
        "numero_recensioni": evento.numero_recensioni,
        "posti_disponibili": evento.posti_disponibili
    }
    
    return EventoStatsResponse(**stats)


@router.get("/calendar/", response_model=List[EventoCalendarResponse])
def get_eventi_calendar(
    *,
    db: Session = Depends(deps.get_db),
    anno: int = Query(datetime.now().year),
    mese: Optional[int] = None
) -> Any:
    """
    Eventi per vista calendario
    """
    query = db.query(Evento).filter(
        and_(
            Evento.pubblicato == True,
            Evento.archiviato == False,
            func.extract('year', Evento.data_inizio) == anno
        )
    )
    
    if mese:
        query = query.filter(func.extract('month', Evento.data_inizio) == mese)
    
    eventi = query.order_by(Evento.data_inizio).all()
    
    return [
        EventoCalendarResponse(
            id=evento.id,
            titolo=evento.titolo,
            data_inizio=evento.data_inizio,
            data_fine=evento.data_fine,
            tipo=evento.tipo,
            modalita=evento.modalita,
            sede=evento.sede,
            gratuito=evento.gratuito,
            iscrizioni_aperte=evento.iscrizioni_aperte
        )
        for evento in eventi
    ]
