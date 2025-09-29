"""
Schemas Pydantic per il modello Testimonial
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TestimonialTipo(str, Enum):
    CORSO = "corso"
    EVENTO = "evento"
    PROGETTO = "progetto"
    VOLONTARIATO = "volontariato"
    GENERALE = "generale"


class TestimonialStato(str, Enum):
    PENDING = "pending"
    APPROVATO = "approvato"
    RIFIUTATO = "rifiutato"


class TestimonialBase(BaseModel):
    nome_autore: str = Field(..., min_length=1, max_length=100)
    ruolo_autore: Optional[str] = Field(None, max_length=100)
    organizzazione: Optional[str] = Field(None, max_length=200)
    contenuto: str = Field(..., min_length=10, max_length=1000)
    rating: int = Field(..., ge=1, le=5)
    tipo_contesto: TestimonialTipo
    contesto_id: Optional[int] = None
    contesto_nome: Optional[str] = Field(None, max_length=200)
    email_autore: Optional[str] = Field(None, max_length=200)
    consenso_pubblicazione: bool = True


class TestimonialCreate(TestimonialBase):
    """Schema per la creazione di un testimonial"""
    pass


class TestimonialUpdate(BaseModel):
    """Schema per l'aggiornamento di un testimonial"""
    nome_autore: Optional[str] = Field(None, min_length=1, max_length=100)
    ruolo_autore: Optional[str] = Field(None, max_length=100)
    organizzazione: Optional[str] = Field(None, max_length=200)
    contenuto: Optional[str] = Field(None, min_length=10, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)
    tipo_contesto: Optional[TestimonialTipo] = None
    contesto_id: Optional[int] = None
    contesto_nome: Optional[str] = Field(None, max_length=200)
    email_autore: Optional[str] = Field(None, max_length=200)
    consenso_pubblicazione: Optional[bool] = None
    stato: Optional[TestimonialStato] = None
    verificato: Optional[bool] = None
    in_evidenza: Optional[bool] = None


class TestimonialResponse(TestimonialBase):
    """Schema per la risposta di un testimonial"""
    id: int
    stato: TestimonialStato
    verificato: bool = False
    in_evidenza: bool = False
    data_creazione: datetime
    data_approvazione: Optional[datetime] = None
    moderato_da_user_id: Optional[int] = None

    class Config:
        from_attributes = True


class TestimonialListResponse(BaseModel):
    """Schema per la lista paginata di testimonial"""
    testimonials: List[TestimonialResponse]
    total: int
    skip: int
    limit: int
