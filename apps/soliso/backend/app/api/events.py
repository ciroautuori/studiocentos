from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.config import settings
from app.schemas.event import Event as EventSchema, EventCreate, EventUpdate
from app.crud import event as event_crud

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.get("/", response_model=List[EventSchema])
def read_events(
    skip: int = 0,
    limit: int = 100,
    featured: Optional[bool] = None,
    upcoming: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """
    Ottenere l'elenco degli eventi con possibilità di filtrare eventi in evidenza o futuri.
    """
    if featured:
        events = event_crud.get_featured_events(db, skip=skip, limit=limit)
    elif upcoming:
        events = event_crud.get_upcoming_events(db, skip=skip, limit=limit)
    else:
        events = event_crud.get_events(db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=EventSchema)
def read_event(event_id: int, db: Session = Depends(get_db)):
    """
    Ottenere un evento specifico tramite il suo ID.
    """
    db_event = event_crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    return db_event


@router.post("/", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    start_date: datetime = Form(...),
    end_date: Optional[datetime] = Form(None),
    location: Optional[str] = Form(None),
    is_featured: bool = Form(False),
    image: Optional[UploadFile] = File(None),
    additional_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    """
    Creare un nuovo evento con possibilità di caricare un'immagine.
    """
    # Gestione del caricamento dell'immagine
    image_url = None
    if image:
        # Crea directory se non esiste
        upload_dir = os.path.join(
            settings.STATIC_FILES_DIR, "images", "events")
        os.makedirs(upload_dir, exist_ok=True)

        # Genera nome file univoco
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)

        # Salva il file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # URL relativo per accedere all'immagine
        image_url = f"/static/images/events/{file_name}"

    # Gestione delle immagini aggiuntive
    additional_image_urls = []
    if additional_images:
        upload_dir = os.path.join(
            settings.STATIC_FILES_DIR, "images", "events")
        os.makedirs(upload_dir, exist_ok=True)

        for img in additional_images:
            # Genera nome file univoco
            file_extension = os.path.splitext(img.filename)[1]
            file_name = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, file_name)

            # Salva il file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)

            # Aggiungi l'URL all'elenco
            additional_image_urls.append(f"/static/images/events/{file_name}")

    # Crea oggetto evento
    event_data = EventCreate(
        title=title,
        description=description,
        start_date=start_date,
        end_date=end_date,
        location=location,
        image_url=image_url,
        additional_images=additional_image_urls,
        is_featured=is_featured
    )

    return event_crud.create_event(db=db, event=event_data)


@router.put("/{event_id}", response_model=EventSchema)
async def update_event(
    event_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    start_date: Optional[datetime] = Form(None),
    end_date: Optional[datetime] = Form(None),
    location: Optional[str] = Form(None),
    is_featured: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    additional_images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    """
    Aggiornare un evento esistente.
    """
    # Verifica che l'evento esista
    db_event = event_crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    # Gestione del caricamento della nuova immagine, se presente
    image_url = None
    if image:
        # Crea directory se non esiste
        upload_dir = os.path.join(
            settings.STATIC_FILES_DIR, "images", "events")
        os.makedirs(upload_dir, exist_ok=True)

        # Elimina la vecchia immagine se esiste
        if db_event.image_url:
            old_image_path = os.path.join(
                settings.STATIC_FILES_DIR, db_event.image_url.lstrip('/static/'))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

        # Genera nome file univoco
        file_extension = os.path.splitext(image.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)

        # Salva il file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # URL relativo per accedere all'immagine
        image_url = f"/static/images/events/{file_name}"

    # Gestione delle immagini aggiuntive
    additional_image_urls = None
    if additional_images:
        upload_dir = os.path.join(
            settings.STATIC_FILES_DIR, "images", "events")
        os.makedirs(upload_dir, exist_ok=True)

        # Elimina le vecchie immagini aggiuntive
        if db_event.additional_images:
            for old_img_url in db_event.additional_images:
                old_image_path = os.path.join(
                    settings.STATIC_FILES_DIR, old_img_url.lstrip('/static/'))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        additional_image_urls = []
        for img in additional_images:
            # Genera nome file univoco
            file_extension = os.path.splitext(img.filename)[1]
            file_name = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(upload_dir, file_name)

            # Salva il file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img.file, buffer)

            # Aggiungi l'URL all'elenco
            additional_image_urls.append(f"/static/images/events/{file_name}")

    # Crea oggetto per l'aggiornamento
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if start_date is not None:
        update_data["start_date"] = start_date
    if end_date is not None:
        update_data["end_date"] = end_date
    if location is not None:
        update_data["location"] = location
    if is_featured is not None:
        update_data["is_featured"] = is_featured
    if image_url is not None:
        update_data["image_url"] = image_url
    if additional_image_urls is not None:
        update_data["additional_images"] = additional_image_urls
    else:
        update_data["additional_images"] = db_event.additional_images

    event_update = EventUpdate(**update_data)
    return event_crud.update_event(db=db, event_id=event_id, event=event_update)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Eliminare un evento.
    """
    # Verifica che l'evento esista
    db_event = event_crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Evento non trovato")

    # Elimina l'immagine associata se esiste
    if db_event.image_url:
        image_path = os.path.join(
            settings.STATIC_FILES_DIR, db_event.image_url.lstrip('/static/'))
        if os.path.exists(image_path):
            os.remove(image_path)

    success = event_crud.delete_event(db=db, event_id=event_id)
    if not success:
        raise HTTPException(
            status_code=500, detail="Errore durante l'eliminazione")

    return None
