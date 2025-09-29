"""
API Endpoints per il sistema Partners ISS
Gestione completa partner, sponsor e collaborazioni strategiche
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.partner import (
    Partner, PartnerContatto, PartnerAttivita, PartnerDocumento,
    PartnerTipo, PartnerCategoria, PartnerLivello, PartnerStato, PartnerSettore
)
from app.models.user import User
from app.schemas.partner import (
    PartnerCreate, PartnerUpdate, PartnerResponse, PartnerListResponse,
    PartnerContattoCreate, PartnerContattoResponse,
    PartnerAttivitaCreate, PartnerAttivitaResponse,
    PartnerDocumentoCreate, PartnerDocumentoResponse,
    PartnerStatsResponse
)
from app.core.config import settings
from app.utils.email import send_email
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=PartnerListResponse)
def get_partners(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[PartnerTipo] = None,
    categoria: Optional[PartnerCategoria] = None,
    livello: Optional[PartnerLivello] = None,
    stato: Optional[PartnerStato] = None,
    settore: Optional[PartnerSettore] = None,
    search: Optional[str] = None,
    solo_attivi: bool = True,
    solo_strategici: bool = False,
    citta: Optional[str] = None,
    paese: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|nome_organizzazione|livello|data_inizio_partnership)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista partners con filtri avanzati
    """
    query = db.query(Partner)
    
    # Filtri base per utenti non admin
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(Partner.visibile_sito == True)
        query = query.filter(Partner.archiviato == False)
    
    # Filtri specifici
    if tipo:
        query = query.filter(Partner.tipo == tipo)
    if categoria:
        query = query.filter(Partner.categoria == categoria)
    if livello:
        query = query.filter(Partner.livello == livello)
    if stato:
        query = query.filter(Partner.stato == stato)
    if settore:
        query = query.filter(Partner.settore == settore)
    if solo_attivi:
        query = query.filter(Partner.stato == PartnerStato.ATTIVA)
    if solo_strategici:
        query = query.filter(Partner.partner_strategico == True)
    if citta:
        query = query.filter(Partner.citta.ilike(f"%{citta}%"))
    if paese:
        query = query.filter(Partner.paese.ilike(f"%{paese}%"))
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            Partner.nome_organizzazione.ilike(f"%{search}%"),
            Partner.nome_breve.ilike(f"%{search}%"),
            Partner.descrizione.ilike(f"%{search}%"),
            Partner.descrizione_breve.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Partner, sort_by)))
    else:
        query = query.order_by(asc(getattr(Partner, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    partners = query.offset(skip).limit(limit).all()
    
    return PartnerListResponse(
        partners=partners,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=PartnerResponse)
def create_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_in: PartnerCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea nuovo partner (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono creare partner"
        )
    
    # Genera codice partner univoco
    ultimo_partner = db.query(Partner).order_by(desc(Partner.id)).first()
    numero = (ultimo_partner.id + 1) if ultimo_partner else 1
    codice_partner = f"ISS-PTR-{datetime.now().year}-{numero:03d}"
    
    # Genera slug univoco
    base_slug = partner_in.nome_organizzazione.lower().replace(" ", "-")
    slug = base_slug
    counter = 1
    
    while db.query(Partner).filter(Partner.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Crea partner
    partner = Partner(
        **partner_in.dict(),
        codice_partner=codice_partner,
        slug=slug,
        creato_da_user_id=current_user.id
    )
    
    db.add(partner)
    db.commit()
    db.refresh(partner)
    
    return partner


@router.get("/{partner_id}", response_model=PartnerResponse)
def get_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli partner specifico
    """
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if not partner.visibile_sito or partner.archiviato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner non disponibile"
            )
    
    return partner


@router.get("/slug/{slug}", response_model=PartnerResponse)
def get_partner_by_slug(
    *,
    db: Session = Depends(deps.get_db),
    slug: str,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera partner tramite slug
    """
    partner = db.query(Partner).filter(Partner.slug == slug).first()
    
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if not partner.visibile_sito or partner.archiviato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner non disponibile"
            )
    
    return partner


@router.put("/{partner_id}", response_model=PartnerResponse)
def update_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    partner_in: PartnerUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna partner (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono modificare partner"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    # Aggiorna campi
    update_data = partner_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(partner, field, value)
    
    partner.modificato_da_user_id = current_user.id
    
    db.commit()
    db.refresh(partner)
    
    return partner


@router.delete("/{partner_id}")
def delete_partner(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina partner (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono eliminare partner"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    # Verifica se ci sono attività o documenti
    attivita_count = db.query(PartnerAttivita).filter(PartnerAttivita.partner_id == partner_id).count()
    documenti_count = db.query(PartnerDocumento).filter(PartnerDocumento.partner_id == partner_id).count()
    
    if attivita_count > 0 or documenti_count > 0:
        # Non eliminare, ma archivia
        partner.archiviato = True
        partner.stato = PartnerStato.CONCLUSA
        db.commit()
        return {"message": "Partner archiviato (aveva attività/documenti collegati)"}
    
    db.delete(partner)
    db.commit()
    
    return {"message": "Partner eliminato con successo"}


@router.post("/{partner_id}/contatti", response_model=PartnerContattoResponse)
def add_partner_contatto(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    contatto_in: PartnerContattoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiungi contatto al partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono aggiungere contatti"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    contatto = PartnerContatto(
        **contatto_in.dict(),
        partner_id=partner_id
    )
    
    db.add(contatto)
    db.commit()
    db.refresh(contatto)
    
    return contatto


@router.get("/{partner_id}/contatti", response_model=List[PartnerContattoResponse])
def get_partner_contatti(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista contatti partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere i contatti"
        )
    
    contatti = db.query(PartnerContatto).filter(
        and_(
            PartnerContatto.partner_id == partner_id,
            PartnerContatto.attivo == True
        )
    ).order_by(desc(PartnerContatto.principale), PartnerContatto.nome).all()
    
    return contatti


@router.post("/{partner_id}/attivita", response_model=PartnerAttivitaResponse)
def create_partner_attivita(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    attivita_in: PartnerAttivitaCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Registra attività con partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono registrare attività"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    attivita = PartnerAttivita(
        **attivita_in.dict(),
        partner_id=partner_id,
        creata_da_id=current_user.id
    )
    
    db.add(attivita)
    db.commit()
    db.refresh(attivita)
    
    return attivita


@router.get("/{partner_id}/attivita", response_model=List[PartnerAttivitaResponse])
def get_partner_attivita(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista attività partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere le attività"
        )
    
    attivita = db.query(PartnerAttivita).filter(
        PartnerAttivita.partner_id == partner_id
    ).order_by(desc(PartnerAttivita.data_attivita)).offset(skip).limit(limit).all()
    
    return attivita


@router.post("/{partner_id}/documenti", response_model=PartnerDocumentoResponse)
def upload_partner_documento(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    documento_in: PartnerDocumentoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Carica documento partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono caricare documenti"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    documento = PartnerDocumento(
        **documento_in.dict(),
        partner_id=partner_id,
        caricato_da_id=current_user.id
    )
    
    db.add(documento)
    db.commit()
    db.refresh(documento)
    
    return documento


@router.get("/{partner_id}/documenti", response_model=List[PartnerDocumentoResponse])
def get_partner_documenti(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    tipo_documento: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista documenti partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere i documenti"
        )
    
    query = db.query(PartnerDocumento).filter(PartnerDocumento.partner_id == partner_id)
    
    if tipo_documento:
        query = query.filter(PartnerDocumento.tipo_documento == tipo_documento)
    
    documenti = query.order_by(desc(PartnerDocumento.created_at)).all()
    
    return documenti


@router.get("/{partner_id}/stats", response_model=PartnerStatsResponse)
def get_partner_stats(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Statistiche partner (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere le statistiche"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    # Calcola statistiche
    numero_attivita = db.query(PartnerAttivita).filter(PartnerAttivita.partner_id == partner_id).count()
    numero_documenti = db.query(PartnerDocumento).filter(PartnerDocumento.partner_id == partner_id).count()
    numero_contatti = db.query(PartnerContatto).filter(
        and_(PartnerContatto.partner_id == partner_id, PartnerContatto.attivo == True)
    ).count()
    
    stats = {
        "partner_id": partner_id,
        "giorni_partnership": partner.giorni_partnership,
        "giorni_scadenza": partner.giorni_scadenza,
        "numero_attivita": numero_attivita,
        "numero_documenti": numero_documenti,
        "numero_contatti": numero_contatti,
        "is_active": partner.is_active,
        "valutazione_partnership": float(partner.valutazione_partnership) if partner.valutazione_partnership else None
    }
    
    return PartnerStatsResponse(**stats)


@router.get("/livelli/stats")
def get_livelli_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Statistiche per livello di partnership (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere le statistiche"
        )
    
    stats = db.query(
        Partner.livello,
        func.count(Partner.id).label("numero_partners"),
        func.avg(Partner.valutazione_partnership).label("valutazione_media"),
        func.sum(Partner.contributo_finanziario).label("contributo_totale")
    ).filter(
        and_(
            Partner.stato == PartnerStato.ATTIVA,
            Partner.archiviato == False
        )
    ).group_by(Partner.livello).all()
    
    return [
        {
            "livello": stat.livello,
            "numero_partners": stat.numero_partners,
            "valutazione_media": float(stat.valutazione_media) if stat.valutazione_media else 0.0,
            "contributo_totale": float(stat.contributo_totale) if stat.contributo_totale else 0.0
        }
        for stat in stats
    ]


@router.get("/settori/stats")
def get_settori_stats(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Statistiche per settore di partnership
    """
    stats = db.query(
        Partner.settore,
        func.count(Partner.id).label("numero_partners"),
        func.avg(Partner.valutazione_partnership).label("valutazione_media")
    ).filter(
        and_(
            Partner.stato == PartnerStato.ATTIVA,
            Partner.archiviato == False,
            Partner.visibile_sito == True
        )
    ).group_by(Partner.settore).all()
    
    return [
        {
            "settore": stat.settore,
            "numero_partners": stat.numero_partners,
            "valutazione_media": float(stat.valutazione_media) if stat.valutazione_media else 0.0
        }
        for stat in stats
    ]


@router.get("/featured")
def get_featured_partners(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(12, ge=1, le=50)
) -> Any:
    """
    Partners in evidenza per homepage
    """
    partners = db.query(Partner).filter(
        and_(
            Partner.stato == PartnerStato.ATTIVA,
            Partner.in_evidenza == True,
            Partner.visibile_sito == True,
            Partner.archiviato == False
        )
    ).order_by(
        desc(Partner.livello),
        desc(Partner.data_inizio_partnership)
    ).limit(limit).all()
    
    return partners


@router.get("/scadenza/prossime")
def get_partnership_in_scadenza(
    *,
    db: Session = Depends(deps.get_db),
    giorni: int = Query(30, ge=1, le=365),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Partnership in scadenza nei prossimi giorni (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere le scadenze"
        )
    
    data_limite = datetime.now() + timedelta(days=giorni)
    
    partners = db.query(Partner).filter(
        and_(
            Partner.stato == PartnerStato.ATTIVA,
            Partner.data_fine_partnership != None,
            Partner.data_fine_partnership <= data_limite,
            Partner.data_fine_partnership >= datetime.now()
        )
    ).order_by(Partner.data_fine_partnership).all()
    
    return partners


@router.post("/{partner_id}/rinnova")
def rinnova_partnership(
    *,
    db: Session = Depends(deps.get_db),
    partner_id: int,
    nuova_scadenza: datetime,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Rinnova partnership (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono rinnovare partnership"
        )
    
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner non trovato"
        )
    
    partner.data_fine_partnership = nuova_scadenza
    partner.modificato_da_user_id = current_user.id
    
    db.commit()
    
    return {"message": f"Partnership rinnovata fino al {nuova_scadenza.strftime('%d/%m/%Y')}"}
