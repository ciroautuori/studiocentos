from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Schema base per gli eventi


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    additional_images: Optional[list] = []
    is_featured: bool = False

# Schema per la creazione di un evento


class EventCreate(EventBase):
    pass

# Schema per l'aggiornamento di un evento (tutti i campi sono opzionali)


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    additional_images: Optional[list] = None
    is_featured: Optional[bool] = None

# Schema per l'output di un evento (include i campi di database)


class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
