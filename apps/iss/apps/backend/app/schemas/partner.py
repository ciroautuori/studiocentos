"""
Schemas Pydantic per il modello Partner
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class PartnerTipo(str, Enum):
    ISTITUZIONE_ACCADEMICA = "istituzione_accademica"
    ENTE_PUBBLICO = "ente_pubblico"
    AZIENDA_PRIVATA = "azienda_privata"
    ONG = "ong"
    FONDAZIONE = "fondazione"
    ASSOCIAZIONE = "associazione"


class PartnerLivello(str, Enum):
    STRATEGICO = "strategico"
    ISTITUZIONALE = "istituzionale"
    OPERATIVO = "operativo"
    OCCASIONALE = "occasionale"


class PartnerStato(str, Enum):
    ATTIVA = "attiva"
    SOSPESA = "sospesa"
    CONCLUSA = "conclusa"


class PartnerSettore(str, Enum):
    EDUCAZIONE = "educazione"
    TECNOLOGIA = "tecnologia"
    SOCIALE = "sociale"
    SANITARIO = "sanitario"
    AMBIENTALE = "ambientale"
    CULTURALE = "culturale"
    PUBBLICA_AMMINISTRAZIONE = "pubblica_amministrazione"


class PartnerBase(BaseModel):
    nome_organizzazione: str = Field(..., min_length=1, max_length=200)
    nome_breve: Optional[str] = Field(None, max_length=50)
    descrizione_breve: Optional[str] = Field(None, max_length=500)
    descrizione: Optional[str] = None
    tipo: PartnerTipo
    livello: PartnerLivello
    settore: PartnerSettore
    sito_web: Optional[str] = None
    email_contatto: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    indirizzo: Optional[str] = Field(None, max_length=300)
    citta: str = Field(..., max_length=100)
    paese: str = Field(default="Italia", max_length=100)
    logo_url: Optional[str] = None
    data_inizio_partnership: Optional[date] = None
    data_fine_partnership: Optional[date] = None
    contributo_finanziario: Optional[float] = Field(None, ge=0)
    valutazione_partnership: Optional[float] = Field(None, ge=1, le=5)


class PartnerCreate(PartnerBase):
    """Schema per la creazione di un partner"""
    pass


class PartnerUpdate(BaseModel):
    """Schema per l'aggiornamento di un partner"""
    nome_organizzazione: Optional[str] = Field(None, min_length=1, max_length=200)
    nome_breve: Optional[str] = Field(None, max_length=50)
    descrizione_breve: Optional[str] = Field(None, max_length=500)
    descrizione: Optional[str] = None
    tipo: Optional[PartnerTipo] = None
    livello: Optional[PartnerLivello] = None
    settore: Optional[PartnerSettore] = None
    sito_web: Optional[str] = None
    email_contatto: Optional[str] = Field(None, max_length=200)
    telefono: Optional[str] = Field(None, max_length=20)
    indirizzo: Optional[str] = Field(None, max_length=300)
    citta: Optional[str] = Field(None, max_length=100)
    paese: Optional[str] = Field(None, max_length=100)
    logo_url: Optional[str] = None
    data_inizio_partnership: Optional[date] = None
    data_fine_partnership: Optional[date] = None
    contributo_finanziario: Optional[float] = Field(None, ge=0)
    valutazione_partnership: Optional[float] = Field(None, ge=1, le=5)
    stato: Optional[PartnerStato] = None
    partner_strategico: Optional[bool] = None
    visibile_sito: Optional[bool] = None
    in_evidenza: Optional[bool] = None


class PartnerResponse(PartnerBase):
    """Schema per la risposta di un partner"""
    id: int
    codice_partner: str
    slug: str
    stato: PartnerStato
    partner_strategico: bool = False
    visibile_sito: bool = True
    in_evidenza: bool = False
    archiviato: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    creato_da_user_id: Optional[int] = None

    class Config:
        from_attributes = True


class PartnerListResponse(BaseModel):
    """Schema per la lista paginata di partner"""
    partners: List[PartnerResponse]
    total: int
    skip: int
    limit: int
