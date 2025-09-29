from fastapi import APIRouter, Depends, HTTPException
from typing import List

# Importa il modulo di autenticazione
from app.core.auth import get_current_admin, TokenData

# Importa i tuoi modelli e servizi
# from app.models.user import UserModel
# from app.services.user_service import get_all_users

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # Protegge automaticamente tutte le rotte
    dependencies=[Depends(get_current_admin)],
    responses={401: {"description": "Non autorizzato"}},
    # Nasconde le rotte dalla documentazione Swagger
    include_in_schema=False
)


@router.get("/dashboard")
async def admin_dashboard(current_admin: TokenData = Depends(get_current_admin)):
    return {
        "message": f"Benvenuto nel pannello admin, {current_admin.username}!",
        "status": "Accesso riservato"
    }


@router.get("/utenti")
async def lista_utenti():
    # Qui chiameresti il tuo servizio utenti
    # users = get_all_users()
    users = [{"id": 1, "name": "Utente di esempio"}]  # Esempio
    return users


@router.post("/contenuti")
async def crea_contenuto():
    # Qui la tua logica per creare contenuti
    return {"status": "Contenuto creato con successo", "id": 123}

# Altre rotte admin...
