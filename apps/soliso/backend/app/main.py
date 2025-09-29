from fastapi import FastAPI, Depends
from datetime import timedelta
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
import os


from app.core.config import settings
from app.core.database import engine, Base
from app.api import events, projects, auth

# Importa il modulo di autenticazione
from app.core.auth import (
    Token, authenticate_admin,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)
root_path = os.getenv("ROOT_PATH", "")

# Crea l'applicazione FastAPI
app = FastAPI(
    title="Events and Projects API",
    description="API per gestire eventi e progetti",
    version="0.1.0",
    root_path=root_path
)

# Endpoint per il login


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    is_authenticated = authenticate_admin(
        form_data.username, form_data.password)

    if not is_authenticated:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=401,
            detail="Username o password non corretti",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Configurazione CORS (Cross-Origin Resource Sharing)
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5174",  # Alternative port
    "http://127.0.0.1:5173",  # Alternative localhost
    "http://127.0.0.1:5174",  # Alternative port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta la directory dei file statici
app.mount("/static", StaticFiles(directory=settings.STATIC_FILES_DIR), name="static")

# Aggiungi i router API
app.include_router(events.router)
app.include_router(projects.router)
app.include_router(auth.router)


# Endpoint root semplice


@app.get("/")
def read_root():
    return {
        "message": "Benvenuto all'API Events and Projects!",
        "docs": f"{settings.API_PREFIX}/docs",
    }
