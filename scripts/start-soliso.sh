#!/bin/bash

echo "🛍️ Avvio Applicazione Soliso"
echo "============================"

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verifica che Traefik sia avviato
log_info "Verificando che Traefik sia attivo..."
if ! docker ps | grep -q traefik-central; then
    log_error "❌ Traefik non è attivo! Esegui prima: ./start-infrastructure.sh"
    exit 1
fi

# Verifica che la rete esista
if ! docker network ls | grep -q traefik-network; then
    log_error "❌ Rete traefik-network non trovata! Esegui prima: ./start-infrastructure.sh"
    exit 1
fi

log_info "✅ Traefik attivo e rete disponibile"

# Avvia Soliso
log_info "Avviando applicazione Soliso..."
cd /home/bfiltoperator_gmail_com/docker-projects/soliso
docker-compose -f docker-compose.traefik.yml up -d --build

# Verifica avvio
sleep 10
log_info "Verificando stato dei servizi..."

services=("soliso-backend" "soliso-frontend" "soliso-admin" "soliso-postgres")
all_up=true

for service in "${services[@]}"; do
    if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$service.*Up"; then
        log_info "✅ $service: OK"
    else
        log_error "❌ $service: ERRORE"
        all_up=false
    fi
done

echo ""
if [ "$all_up" = true ]; then
    log_info "🎉 Soliso avviato con successo!"
    echo ""
    echo "🌐 Applicazione disponibile su:"
    echo "   Frontend: https://solisoaps.it"
    echo "   Admin:    https://admin.solisoaps.it"
    echo "   API:      https://solisoaps.it/api"
    echo ""
    echo "📊 Dashboard Traefik: https://traefik.solisoaps.it"
    echo ""
    echo "⚠️  IMPORTANTE: Configura il DNS per puntare a questo server:"
    echo "   solisoaps.it         -> IP_DEL_SERVER"
    echo "   admin.solisoaps.it   -> IP_DEL_SERVER"  
    echo "   traefik.solisoaps.it -> IP_DEL_SERVER"
else
    log_error "❌ Alcuni servizi hanno problemi. Controlla i log:"
    echo "docker-compose -f docker-compose.traefik.yml logs"
fi
