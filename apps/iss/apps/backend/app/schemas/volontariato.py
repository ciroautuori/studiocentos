"""
Schemas Pydantic per il modello Volontariato
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum


class TipoImpegno(str, Enum):
    CONTINUATIVO = "continuativo"
    PROGETTO = "progetto"
    EVENTO = "evento"
    EMERGENZA = "emergenza"


class ModalitaVolontariato(str, Enum):
    PRESENZA = "presenza"
    REMOTO = "remoto"
    IBRIDO = "ibrido"


class StatoOpportunita(str, Enum):
    BOZZA = "bozza"
    PUBBLICATA = "pubblicata"
    SOSPESA = "sospesa"
    CHIUSA = "chiusa"


class OpportunitaVolontariatoBase(BaseModel):
    titolo: str = Field(..., min_length=1, max_length=200)
    descrizione_breve: Optional[str] = Field(None, max_length=500)
    descrizione: Optional[str] = None
    tipo_impegno: TipoImpegno
    modalita: ModalitaVolontariato
    ore_settimanali: Optional[int] = Field(None, ge=1, le=40)
    durata_mesi: Optional[int] = Field(None, ge=1)
    data_inizio: Optional[date] = None
    data_fine: Optional[date] = None
    luogo: Optional[str] = Field(None, max_length=200)
    citta: str = Field(..., max_length=100)
    skills_richieste: Optional[str] = None
    requisiti: Optional[str] = None
    benefici: Optional[str] = None
    contatto_referente: Optional[str] = Field(None, max_length=200)
    email_contatto: Optional[str] = Field(None, max_length=200)
    telefono_contatto: Optional[str] = Field(None, max_length=20)


class OpportunitaVolontariatoCreate(OpportunitaVolontariatoBase):
    """Schema per la creazione di un'opportunità di volontariato"""
    pass


class OpportunitaVolontariatoUpdate(BaseModel):
    """Schema per l'aggiornamento di un'opportunità di volontariato"""
    titolo: Optional[str] = Field(None, min_length=1, max_length=200)
    descrizione_breve: Optional[str] = Field(None, max_length=500)
    descrizione: Optional[str] = None
    tipo_impegno: Optional[TipoImpegno] = None
    modalita: Optional[ModalitaVolontariato] = None
    ore_settimanali: Optional[int] = Field(None, ge=1, le=40)
    durata_mesi: Optional[int] = Field(None, ge=1)
    data_inizio: Optional[date] = None
    data_fine: Optional[date] = None
    luogo: Optional[str] = Field(None, max_length=200)
    citta: Optional[str] = Field(None, max_length=100)
    skills_richieste: Optional[str] = None
    requisiti: Optional[str] = None
    benefici: Optional[str] = None
    contatto_referente: Optional[str] = Field(None, max_length=200)
    email_contatto: Optional[str] = Field(None, max_length=200)
    telefono_contatto: Optional[str] = Field(None, max_length=20)
    stato: Optional[StatoOpportunita] = None
    candidature_aperte: Optional[bool] = None


class OpportunitaVolontariatoResponse(OpportunitaVolontariatoBase):
    """Schema per la risposta di un'opportunità di volontariato"""
    id: int
    slug: str
    stato: StatoOpportunita
    candidature_aperte: bool = True
    numero_candidature: int = 0
    numero_volontari_attivi: int = 0
    in_evidenza: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    creato_da_user_id: Optional[int] = None

    class Config:
        from_attributes = True


class OpportunitaVolontariatoListResponse(BaseModel):
    """Schema per la lista paginata di opportunità di volontariato"""
    opportunita: List[OpportunitaVolontariatoResponse]
    total: int
    skip: int
    limit: int
