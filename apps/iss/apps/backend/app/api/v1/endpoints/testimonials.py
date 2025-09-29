"""
API Endpoints per il sistema Testimonials ISS
Gestione completa testimonianze, recensioni e feedback utenti
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.testimonial import (
    Testimonial, TestimonialRichiesta, TestimonialTemplate, TestimonialMetrica,
    TestimonialTipo, TestimonialCategoria, TestimonialStato, TestimonialFormato
)
from app.models.user import User
from app.schemas.testimonial import (
    TestimonialCreate, TestimonialUpdate, TestimonialResponse, TestimonialListResponse,
    TestimonialRichiestaCreate, TestimonialRichiestaResponse,
    TestimonialTemplateCreate, TestimonialTemplateResponse,
    TestimonialStatsResponse
)
from app.core.config import settings
from app.utils.email import send_email
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=TestimonialListResponse)
def get_testimonials(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tipo: Optional[TestimonialTipo] = None,
    categoria: Optional[TestimonialCategoria] = None,
    formato: Optional[TestimonialFormato] = None,
    stato: Optional[TestimonialStato] = None,
    rating_min: Optional[int] = Query(None, ge=1, le=5),
    search: Optional[str] = None,
    solo_in_evidenza: bool = False,
    solo_verificate: bool = True,
    corso_id: Optional[int] = None,
    evento_id: Optional[int] = None,
    progetto_id: Optional[int] = None,
    sort_by: str = Query("data_pubblicazione", regex="^(data_pubblicazione|created_at|rating|visualizzazioni)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista testimonials con filtri avanzati
    """
    query = db.query(Testimonial)
    
    # Filtri base per utenti non admin
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(Testimonial.stato == TestimonialStato.PUBBLICATA)
        query = query.filter(Testimonial.consenso_pubblicazione == True)
    
    # Filtri specifici
    if tipo:
        query = query.filter(Testimonial.tipo == tipo)
    if categoria:
        query = query.filter(Testimonial.categoria == categoria)
    if formato:
        query = query.filter(Testimonial.formato == formato)
    if stato and (current_user and current_user.ruolo == "admin"):
        query = query.filter(Testimonial.stato == stato)
    if rating_min:
        query = query.filter(Testimonial.rating >= rating_min)
    if solo_in_evidenza:
        query = query.filter(Testimonial.in_evidenza == True)
    if solo_verificate:
        query = query.filter(Testimonial.verificata == True)
    
    # Filtri per contesto specifico
    if corso_id:
        query = query.filter(Testimonial.corso_id == corso_id)
    if evento_id:
        query = query.filter(Testimonial.evento_id == evento_id)
    if progetto_id:
        query = query.filter(Testimonial.progetto_id == progetto_id)
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            Testimonial.titolo.ilike(f"%{search}%"),
            Testimonial.contenuto.ilike(f"%{search}%"),
            Testimonial.contenuto_breve.ilike(f"%{search}%"),
            Testimonial.nome_autore.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(Testimonial, sort_by)))
    else:
        query = query.order_by(asc(getattr(Testimonial, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    testimonials = query.offset(skip).limit(limit).all()
    
    return TestimonialListResponse(
        testimonials=testimonials,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=TestimonialResponse)
def create_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_in: TestimonialCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea nuova testimonial
    """
    # Genera slug univoco se non fornito
    if not testimonial_in.slug:
        base_slug = testimonial_in.titolo.lower().replace(" ", "-")
        slug = base_slug
        counter = 1
        
        while db.query(Testimonial).filter(Testimonial.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        testimonial_in.slug = slug
    
    # Crea testimonial
    testimonial = Testimonial(
        **testimonial_in.dict(),
        user_id=current_user.id,
        nome_autore=testimonial_in.nome_autore or current_user.nome,
        cognome_autore=testimonial_in.cognome_autore or current_user.cognome
    )
    
    # Auto-approva se admin
    if current_user.ruolo == "admin":
        testimonial.stato = TestimonialStato.PUBBLICATA
        testimonial.data_pubblicazione = datetime.now()
    
    db.add(testimonial)
    db.commit()
    db.refresh(testimonial)
    
    return testimonial


@router.get("/{testimonial_id}", response_model=TestimonialResponse)
def get_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli testimonial specifica
    """
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if (testimonial.stato != TestimonialStato.PUBBLICATA or 
            not testimonial.consenso_pubblicazione):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Testimonial non disponibile"
            )
    
    # Incrementa visualizzazioni
    testimonial.visualizzazioni += 1
    db.commit()
    
    return testimonial


@router.get("/slug/{slug}", response_model=TestimonialResponse)
def get_testimonial_by_slug(
    *,
    db: Session = Depends(deps.get_db),
    slug: str,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera testimonial tramite slug
    """
    testimonial = db.query(Testimonial).filter(Testimonial.slug == slug).first()
    
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if (testimonial.stato != TestimonialStato.PUBBLICATA or 
            not testimonial.consenso_pubblicazione):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Testimonial non disponibile"
            )
    
    # Incrementa visualizzazioni
    testimonial.visualizzazioni += 1
    db.commit()
    
    return testimonial


@router.put("/{testimonial_id}", response_model=TestimonialResponse)
def update_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_id: int,
    testimonial_in: TestimonialUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna testimonial (admin o autore)
    """
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    # Verifica permessi
    if (current_user.ruolo != "admin" and testimonial.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare questa testimonial"
        )
    
    # Aggiorna campi
    update_data = testimonial_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(testimonial, field, value)
    
    # Se viene pubblicata, imposta data pubblicazione
    if update_data.get("stato") == TestimonialStato.PUBBLICATA and not testimonial.data_pubblicazione:
        testimonial.data_pubblicazione = datetime.now()
    
    db.commit()
    db.refresh(testimonial)
    
    return testimonial


@router.delete("/{testimonial_id}")
def delete_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina testimonial (admin o autore)
    """
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    # Verifica permessi
    if (current_user.ruolo != "admin" and testimonial.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per eliminare questa testimonial"
        )
    
    db.delete(testimonial)
    db.commit()
    
    return {"message": "Testimonial eliminata con successo"}


@router.post("/{testimonial_id}/like")
def like_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Metti/togli like a una testimonial
    """
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    # Logica semplificata - in produzione si userebbe una tabella separata
    testimonial.like_count += 1
    db.commit()
    
    return {"message": "Like aggiunto", "total_likes": testimonial.like_count}


@router.post("/{testimonial_id}/verifica")
def verifica_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_id: int,
    note_verifica: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Verifica testimonial (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono verificare testimonials"
        )
    
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    testimonial.verificata = True
    testimonial.verificata_da_id = current_user.id
    testimonial.data_verifica = datetime.now()
    testimonial.note_verifica = note_verifica
    
    db.commit()
    
    return {"message": "Testimonial verificata con successo"}


@router.post("/{testimonial_id}/modera")
def modera_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    testimonial_id: int,
    note_moderazione: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Modera testimonial (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono moderare testimonials"
        )
    
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial non trovata"
        )
    
    testimonial.moderata = True
    testimonial.moderata_da_id = current_user.id
    testimonial.note_moderazione = note_moderazione
    
    db.commit()
    
    return {"message": "Testimonial moderata con successo"}


@router.post("/richieste", response_model=TestimonialRichiestaResponse)
def create_richiesta_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    richiesta_in: TestimonialRichiestaCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea richiesta di testimonial (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono richiedere testimonials"
        )
    
    # Genera token univoco
    import uuid
    token = str(uuid.uuid4())
    
    richiesta = TestimonialRichiesta(
        **richiesta_in.dict(),
        inviata_da_id=current_user.id,
        token_risposta=token
    )
    
    db.add(richiesta)
    db.commit()
    db.refresh(richiesta)
    
    # Invia email di richiesta
    try:
        send_email(
            to=richiesta.email_destinatario,
            subject="Richiesta Testimonial - ISS",
            template="testimonial_richiesta",
            context={
                "nome_destinatario": richiesta.nome_destinatario,
                "messaggio": richiesta.messaggio_richiesta,
                "link_risposta": f"{settings.FRONTEND_URL}/testimonials/rispondi/{token}"
            }
        )
    except Exception as e:
        print(f"Errore invio email: {e}")
    
    return richiesta


@router.get("/richieste", response_model=List[TestimonialRichiestaResponse])
def get_richieste_testimonial(
    *,
    db: Session = Depends(deps.get_db),
    stato: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Lista richieste testimonial (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere le richieste"
        )
    
    query = db.query(TestimonialRichiesta)
    
    if stato:
        query = query.filter(TestimonialRichiesta.stato == stato)
    
    richieste = query.order_by(desc(TestimonialRichiesta.data_invio)).all()
    
    return richieste


@router.get("/stats/overview", response_model=TestimonialStatsResponse)
def get_testimonial_stats(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Statistiche generali testimonials (admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono vedere le statistiche"
        )
    
    # Calcola statistiche
    totale_testimonials = db.query(Testimonial).count()
    pubblicate = db.query(Testimonial).filter(Testimonial.stato == TestimonialStato.PUBBLICATA).count()
    verificate = db.query(Testimonial).filter(Testimonial.verificata == True).count()
    
    rating_medio = db.query(func.avg(Testimonial.rating)).filter(
        Testimonial.stato == TestimonialStato.PUBBLICATA
    ).scalar()
    
    stats = {
        "totale_testimonials": totale_testimonials,
        "pubblicate": pubblicate,
        "verificate": verificate,
        "rating_medio": float(rating_medio) if rating_medio else 0.0,
        "in_evidenza": db.query(Testimonial).filter(Testimonial.in_evidenza == True).count()
    }
    
    return TestimonialStatsResponse(**stats)


@router.get("/categorie/stats")
def get_categorie_stats(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Statistiche per categoria di testimonial
    """
    stats = db.query(
        Testimonial.categoria,
        func.count(Testimonial.id).label("numero_testimonials"),
        func.avg(Testimonial.rating).label("rating_medio"),
        func.sum(Testimonial.visualizzazioni).label("totale_visualizzazioni")
    ).filter(
        Testimonial.stato == TestimonialStato.PUBBLICATA
    ).group_by(Testimonial.categoria).all()
    
    return [
        {
            "categoria": stat.categoria,
            "numero_testimonials": stat.numero_testimonials,
            "rating_medio": float(stat.rating_medio) if stat.rating_medio else 0.0,
            "totale_visualizzazioni": stat.totale_visualizzazioni or 0
        }
        for stat in stats
    ]


@router.get("/featured")
def get_featured_testimonials(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(6, ge=1, le=20)
) -> Any:
    """
    Testimonials in evidenza per homepage
    """
    testimonials = db.query(Testimonial).filter(
        and_(
            Testimonial.stato == TestimonialStato.PUBBLICATA,
            Testimonial.in_evidenza == True,
            Testimonial.verificata == True
        )
    ).order_by(desc(Testimonial.rating), desc(Testimonial.data_pubblicazione)).limit(limit).all()
    
    return testimonials


@router.get("/random")
def get_random_testimonials(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(3, ge=1, le=10)
) -> Any:
    """
    Testimonials casuali per widget
    """
    testimonials = db.query(Testimonial).filter(
        and_(
            Testimonial.stato == TestimonialStato.PUBBLICATA,
            Testimonial.verificata == True,
            Testimonial.rating >= 4
        )
    ).order_by(func.random()).limit(limit).all()
    
    return testimonials
