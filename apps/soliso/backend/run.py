import os
import uvicorn
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

if __name__ == "__main__":
    # Ottieni il debug mode dal file .env
    debug = os.getenv("DEBUG", "False").lower() == "true"

    # Avvia il server Uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=debug  # Riavvio automatico in modalità debug
    )
