#!/bin/bash

echo "🚀 Avvio Infrastruttura Docker con Traefik Centrale"
echo "================================================="

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funzione per logging
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Crea la rete Traefik se non esiste
log_info "Verificando rete traefik-network..."
if ! docker network ls | grep -q traefik-network; then
    log_info "Creando rete traefik-network..."
    docker network create traefik-network
else
    log_warn "Rete traefik-network già esistente"
fi

# 2. Crea directory per dati Traefik
log_info "Creando directory traefik-data..."
mkdir -p /home/bfiltoperator_gmail_com/docker-projects/traefik-central/traefik-data
sudo chmod 600 /home/bfiltoperator_gmail_com/docker-projects/traefik-central/traefik-data/acme.json 2>/dev/null || touch /home/bfiltoperator_gmail_com/docker-projects/traefik-central/traefik-data/acme.json

# 3. Avvia Traefik centrale
log_info "Avviando Traefik centrale..."
cd /home/bfiltoperator_gmail_com/docker-projects/traefik-central
docker-compose up -d

# 4. Verifica che Traefik sia avviato
sleep 5
if docker-compose ps | grep -q "Up"; then
    log_info "✅ Traefik avviato con successo!"
    log_info "Dashboard: http://localhost:8080"
else
    log_error "❌ Errore nell'avvio di Traefik"
    exit 1
fi

echo ""
echo "🎉 Infrastruttura pronta!"
echo "Ora puoi avviare le applicazioni con:"
echo "  ./start-soliso.sh"
