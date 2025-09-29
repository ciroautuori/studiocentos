"""
Schemas Pydantic per il modello Progetto
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class ProgettoStato(str, Enum):
    PIANIFICATO = "pianificato"
    IN_CORSO = "in_corso"
    COMPLETATO = "completato"
    SOSPESO = "sospeso"
    ANNULLATO = "annullato"


class ProgettoCategoria(str, Enum):
    DIGITALE = "digitale"
    SOCIALE = "sociale"
    EDUCATIVO = "educativo"
    AMBIENTALE = "ambientale"
    CULTURALE = "culturale"
    SANITARIO = "sanitario"
    RICERCA = "ricerca"


class ProgettoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=200)
    descrizione_breve: Optional[str] = Field(None, max_length=500)
    descrizione: Optional[str] = None
    categoria: ProgettoCategoria
    obiettivi: Optional[str] = None
    budget_totale: Optional[float] = Field(None, ge=0)
    budget_utilizzato: Optional[float] = Field(None, ge=0)
    data_inizio: date
    data_fine_prevista: Optional[date] = None
    data_fine_effettiva: Optional[date] = None
    responsabile_progetto: Optional[str] = Field(None, max_length=200)
    partner_coinvolti: Optional[str] = None
    beneficiari_target: Optional[str] = None
    impatto_sociale: Optional[str] = None
    immagine_copertina: Optional[str] = None
    sito_web: Optional[str] = None
    repository_codice: Optional[str] = None


class ProgettoCreate(ProgettoBase):
    """Schema per la creazione di un progetto"""
    pass


class ProgettoUpdate(BaseModel):
    """Schema per l'aggiornamento di un progetto"""
    nome: Optional[str] = Field(None, min_length=1, max_length=200)
    descrizione_breve: Optional[str] = Field(None, max_length=500)
    descrizione: Optional[str] = None
    categoria: Optional[ProgettoCategoria] = None
    obiettivi: Optional[str] = None
    budget_totale: Optional[float] = Field(None, ge=0)
    budget_utilizzato: Optional[float] = Field(None, ge=0)
    data_inizio: Optional[date] = None
    data_fine_prevista: Optional[date] = None
    data_fine_effettiva: Optional[date] = None
    responsabile_progetto: Optional[str] = Field(None, max_length=200)
    partner_coinvolti: Optional[str] = None
    beneficiari_target: Optional[str] = None
    impatto_sociale: Optional[str] = None
    immagine_copertina: Optional[str] = None
    sito_web: Optional[str] = None
    repository_codice: Optional[str] = None
    stato: Optional[ProgettoStato] = None
    pubblicato: Optional[bool] = None


class ProgettoResponse(ProgettoBase):
    """Schema per la risposta di un progetto"""
    id: int
    slug: str
    stato: ProgettoStato
    pubblicato: bool
    percentuale_completamento: Optional[float] = None
    numero_team_members: int = 0
    numero_aggiornamenti: int = 0
    in_evidenza: bool = False
    archiviato: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    creato_da_user_id: Optional[int] = None

    class Config:
        from_attributes = True


class ProgettoListResponse(BaseModel):
    """Schema per la lista paginata di progetti"""
    progetti: List[ProgettoResponse]
    total: int
    skip: int
    limit: int
