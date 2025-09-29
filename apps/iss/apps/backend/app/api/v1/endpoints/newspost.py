"""
API Endpoints per il sistema News/Blog ISS
Gestione completa articoli, notizie e contenuti editoriali
"""

from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc

from app.api import deps
from app.models.newspost import (
    NewsPost, NewsCommento, NewsLike, NewsNewsletter, NewsCategoriaSottoscrizione,
    NewsCategoria, NewsStato, NewsTipo
)
from app.models.user import User
from app.schemas.newspost import (
    NewsPostCreate, NewsPostUpdate, NewsPostResponse, NewsPostListResponse,
    NewsCommentoCreate, NewsCommentoResponse,
    NewsLikeResponse, NewsStatsResponse
)
from app.core.config import settings
from app.utils.email import send_email
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/", response_model=NewsPostListResponse)
def get_news_posts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    categoria: Optional[NewsCategoria] = None,
    tipo: Optional[NewsTipo] = None,
    stato: Optional[NewsStato] = None,
    search: Optional[str] = None,
    solo_in_evidenza: bool = False,
    solo_homepage: bool = False,
    autore_id: Optional[int] = None,
    tags: Optional[str] = None,
    sort_by: str = Query("data_pubblicazione", regex="^(data_pubblicazione|created_at|titolo|visualizzazioni)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera lista articoli/news con filtri avanzati
    """
    query = db.query(NewsPost)
    
    # Filtri base per utenti non admin
    if not current_user or current_user.ruolo != "admin":
        query = query.filter(NewsPost.stato == NewsStato.PUBBLICATO)
        query = query.filter(NewsPost.archiviato == False)
        query = query.filter(NewsPost.data_pubblicazione <= datetime.now())
    
    # Filtri specifici
    if categoria:
        query = query.filter(NewsPost.categoria == categoria)
    if tipo:
        query = query.filter(NewsPost.tipo == tipo)
    if stato and (current_user and current_user.ruolo == "admin"):
        query = query.filter(NewsPost.stato == stato)
    if solo_in_evidenza:
        query = query.filter(NewsPost.in_evidenza == True)
    if solo_homepage:
        query = query.filter(NewsPost.homepage_featured == True)
    if autore_id:
        query = query.filter(NewsPost.autore_id == autore_id)
    
    # Filtro tags
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        for tag in tag_list:
            query = query.filter(NewsPost.tags.ilike(f'%"{tag}"%'))
    
    # Ricerca testuale
    if search:
        search_filter = or_(
            NewsPost.titolo.ilike(f"%{search}%"),
            NewsPost.sottotitolo.ilike(f"%{search}%"),
            NewsPost.sommario.ilike(f"%{search}%"),
            NewsPost.contenuto.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Ordinamento
    if sort_order == "desc":
        query = query.order_by(desc(getattr(NewsPost, sort_by)))
    else:
        query = query.order_by(asc(getattr(NewsPost, sort_by)))
    
    # Conteggio totale
    total = query.count()
    
    # Paginazione
    posts = query.offset(skip).limit(limit).all()
    
    return NewsPostListResponse(
        posts=posts,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=NewsPostResponse)
def create_news_post(
    *,
    db: Session = Depends(deps.get_db),
    post_in: NewsPostCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea nuovo articolo/news (admin o editor)
    """
    if current_user.ruolo not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per creare articoli"
        )
    
    # Genera slug univoco
    base_slug = post_in.slug or post_in.titolo.lower().replace(" ", "-")
    slug = base_slug
    counter = 1
    
    while db.query(NewsPost).filter(NewsPost.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Crea post
    post = NewsPost(
        **post_in.dict(exclude={"slug"}),
        slug=slug,
        autore_id=current_user.id
    )
    
    # Auto-pubblica se l'utente è admin
    if current_user.ruolo == "admin" and post.stato == NewsStato.BOZZA:
        post.stato = NewsStato.PUBBLICATO
        post.data_pubblicazione = datetime.now()
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post


@router.get("/{post_id}", response_model=NewsPostResponse)
def get_news_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera dettagli articolo specifico
    """
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if (post.stato != NewsStato.PUBBLICATO or 
            post.archiviato or 
            (post.data_pubblicazione and post.data_pubblicazione > datetime.now())):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Articolo non disponibile"
            )
    
    # Incrementa visualizzazioni
    post.visualizzazioni += 1
    db.commit()
    
    return post


@router.get("/slug/{slug}", response_model=NewsPostResponse)
def get_news_post_by_slug(
    *,
    db: Session = Depends(deps.get_db),
    slug: str,
    current_user: Optional[User] = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Recupera articolo tramite slug
    """
    post = db.query(NewsPost).filter(NewsPost.slug == slug).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    # Verifica visibilità
    if not current_user or current_user.ruolo != "admin":
        if (post.stato != NewsStato.PUBBLICATO or 
            post.archiviato or 
            (post.data_pubblicazione and post.data_pubblicazione > datetime.now())):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Articolo non disponibile"
            )
    
    # Incrementa visualizzazioni
    post.visualizzazioni += 1
    db.commit()
    
    return post


@router.put("/{post_id}", response_model=NewsPostResponse)
def update_news_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    post_in: NewsPostUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiorna articolo (admin, editor o autore)
    """
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    # Verifica permessi
    if (current_user.ruolo not in ["admin", "editor"] and 
        post.autore_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per modificare questo articolo"
        )
    
    # Aggiorna campi
    update_data = post_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(post, field, value)
    
    # Se viene cambiato lo stato a pubblicato, imposta data pubblicazione
    if update_data.get("stato") == NewsStato.PUBBLICATO and not post.data_pubblicazione:
        post.data_pubblicazione = datetime.now()
    
    db.commit()
    db.refresh(post)
    
    return post


@router.delete("/{post_id}")
def delete_news_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Elimina articolo (solo admin)
    """
    if current_user.ruolo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo gli admin possono eliminare articoli"
        )
    
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    db.delete(post)
    db.commit()
    
    return {"message": "Articolo eliminato con successo"}


@router.post("/{post_id}/like", response_model=NewsLikeResponse)
def like_news_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Metti/togli like a un articolo
    """
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    # Verifica se esiste già il like
    existing_like = db.query(NewsLike).filter(
        and_(
            NewsLike.post_id == post_id,
            NewsLike.user_id == current_user.id
        )
    ).first()
    
    if existing_like:
        # Rimuovi like
        db.delete(existing_like)
        post.like_count -= 1
        liked = False
    else:
        # Aggiungi like
        like = NewsLike(
            post_id=post_id,
            user_id=current_user.id
        )
        db.add(like)
        post.like_count += 1
        liked = True
    
    db.commit()
    
    return NewsLikeResponse(
        post_id=post_id,
        user_id=current_user.id,
        liked=liked,
        total_likes=post.like_count
    )


@router.post("/{post_id}/commenti", response_model=NewsCommentoResponse)
def create_commento(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    commento_in: NewsCommentoCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Crea commento a un articolo
    """
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    if not post.commenti_abilitati:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="I commenti sono disabilitati per questo articolo"
        )
    
    # Crea commento
    commento = NewsCommento(
        **commento_in.dict(),
        post_id=post_id,
        user_id=current_user.id
    )
    
    db.add(commento)
    
    # Aggiorna contatore
    post.commenti_count += 1
    
    db.commit()
    db.refresh(commento)
    
    return commento


@router.get("/{post_id}/commenti", response_model=List[NewsCommentoResponse])
def get_commenti_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
) -> Any:
    """
    Lista commenti di un articolo
    """
    commenti = db.query(NewsCommento).filter(
        and_(
            NewsCommento.post_id == post_id,
            NewsCommento.approvato == True
        )
    ).order_by(NewsCommento.created_at).offset(skip).limit(limit).all()
    
    return commenti


@router.get("/{post_id}/stats", response_model=NewsStatsResponse)
def get_stats_post(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Statistiche articolo (admin, editor o autore)
    """
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    # Verifica permessi
    if (current_user.ruolo not in ["admin", "editor"] and 
        post.autore_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per vedere le statistiche"
        )
    
    stats = {
        "post_id": post_id,
        "visualizzazioni": post.visualizzazioni,
        "like_count": post.like_count,
        "share_count": post.share_count,
        "commenti_count": post.commenti_count,
        "engagement_score": post.engagement_score,
        "giorni_dalla_pubblicazione": post.giorni_dalla_pubblicazione
    }
    
    return NewsStatsResponse(**stats)


@router.get("/categorie/stats")
def get_categorie_stats(
    *,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Statistiche per categoria di news
    """
    stats = db.query(
        NewsPost.categoria,
        func.count(NewsPost.id).label("numero_articoli"),
        func.sum(NewsPost.visualizzazioni).label("totale_visualizzazioni"),
        func.avg(NewsPost.like_count).label("media_like")
    ).filter(
        and_(
            NewsPost.stato == NewsStato.PUBBLICATO,
            NewsPost.archiviato == False
        )
    ).group_by(NewsPost.categoria).all()
    
    return [
        {
            "categoria": stat.categoria,
            "numero_articoli": stat.numero_articoli,
            "totale_visualizzazioni": stat.totale_visualizzazioni or 0,
            "media_like": float(stat.media_like) if stat.media_like else 0.0
        }
        for stat in stats
    ]


@router.get("/trending")
def get_trending_posts(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(10, ge=1, le=50),
    periodo_giorni: int = Query(7, ge=1, le=30)
) -> Any:
    """
    Articoli di tendenza negli ultimi giorni
    """
    data_limite = datetime.now() - timedelta(days=periodo_giorni)
    
    posts = db.query(NewsPost).filter(
        and_(
            NewsPost.stato == NewsStato.PUBBLICATO,
            NewsPost.archiviato == False,
            NewsPost.data_pubblicazione >= data_limite
        )
    ).order_by(
        desc(NewsPost.visualizzazioni + NewsPost.like_count * 2 + NewsPost.share_count * 3)
    ).limit(limit).all()
    
    return posts


@router.post("/{post_id}/newsletter")
def add_to_newsletter(
    *,
    db: Session = Depends(deps.get_db),
    post_id: int,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Aggiungi articolo alla prossima newsletter (admin o editor)
    """
    if current_user.ruolo not in ["admin", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Non hai i permessi per gestire la newsletter"
        )
    
    post = db.query(NewsPost).filter(NewsPost.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Articolo non trovato"
        )
    
    post.newsletter_featured = True
    db.commit()
    
    return {"message": "Articolo aggiunto alla newsletter"}


@router.get("/autore/{autore_id}")
def get_posts_by_author(
    *,
    db: Session = Depends(deps.get_db),
    autore_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
) -> Any:
    """
    Articoli di un autore specifico
    """
    posts = db.query(NewsPost).filter(
        and_(
            NewsPost.autore_id == autore_id,
            NewsPost.stato == NewsStato.PUBBLICATO,
            NewsPost.archiviato == False
        )
    ).order_by(desc(NewsPost.data_pubblicazione)).offset(skip).limit(limit).all()
    
    return posts
