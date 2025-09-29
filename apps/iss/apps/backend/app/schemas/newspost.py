"""
Schemas Pydantic per il modello NewsPost
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class NewsCategoria(str, Enum):
    FORMAZIONE = "formazione"
    PARTNERSHIP = "partnership"
    EVENTI = "eventi"
    PROGETTI = "progetti"
    VOLONTARIATO = "volontariato"
    TECNOLOGIA = "tecnologia"
    SOCIALE = "sociale"


class NewsStato(str, Enum):
    BOZZA = "bozza"
    PUBBLICATO = "pubblicato"
    ARCHIVIATO = "archiviato"


class NewsPostBase(BaseModel):
    titolo: str = Field(..., min_length=1, max_length=200)
    contenuto_breve: Optional[str] = Field(None, max_length=500)
    contenuto: Optional[str] = None
    categoria: NewsCategoria
    immagine_copertina: Optional[str] = None
    tags: Optional[str] = None
    meta_description: Optional[str] = Field(None, max_length=160)


class NewsPostCreate(NewsPostBase):
    """Schema per la creazione di un post"""
    pass


class NewsPostUpdate(BaseModel):
    """Schema per l'aggiornamento di un post"""
    titolo: Optional[str] = Field(None, min_length=1, max_length=200)
    contenuto_breve: Optional[str] = Field(None, max_length=500)
    contenuto: Optional[str] = None
    categoria: Optional[NewsCategoria] = None
    immagine_copertina: Optional[str] = None
    tags: Optional[str] = None
    meta_description: Optional[str] = Field(None, max_length=160)
    stato: Optional[NewsStato] = None
    pubblicato: Optional[bool] = None
    in_evidenza: Optional[bool] = None


class NewsPostResponse(NewsPostBase):
    """Schema per la risposta di un post"""
    id: int
    slug: str
    stato: NewsStato
    pubblicato: bool
    in_evidenza: bool = False
    numero_visualizzazioni: int = 0
    numero_like: int = 0
    numero_commenti: int = 0
    data_pubblicazione: Optional[datetime] = None
    autore: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    creato_da_user_id: Optional[int] = None

    class Config:
        from_attributes = True


class NewsPostListResponse(BaseModel):
    """Schema per la lista paginata di post"""
    articoli: List[NewsPostResponse]
    total: int
    skip: int
    limit: int
