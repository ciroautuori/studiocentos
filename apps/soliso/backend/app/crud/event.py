from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate


def get_event(db: Session, event_id: int) -> Optional[Event]:
    """
    Ottiene un evento dal database tramite il suo ID.
    """
    return db.query(Event).filter(Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    """
    Ottiene una lista di eventi con paginazione.
    """
    return db.query(Event).offset(skip).limit(limit).all()


def get_featured_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    """
    Ottiene gli eventi in evidenza.
    """
    return db.query(Event).filter(Event.is_featured == True).offset(skip).limit(limit).all()


def get_upcoming_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    """
    Ottiene gli eventi futuri.
    """
    now = datetime.now()
    return db.query(Event).filter(Event.start_date >= now).order_by(Event.start_date).offset(skip).limit(limit).all()


def create_event(db: Session, event: EventCreate) -> Event:
    """
    Crea un nuovo evento nel database.
    """
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: int, event: EventUpdate) -> Optional[Event]:
    """
    Aggiorna un evento esistente.
    """
    db_event = get_event(db, event_id)
    if not db_event:
        return None

    # Aggiorna solo i campi presenti nell'update
    update_data = event.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int) -> bool:
    """
    Elimina un evento dal database.
    """
    db_event = get_event(db, event_id)
    if not db_event:
        return False

    db.delete(db_event)
    db.commit()
    return True
