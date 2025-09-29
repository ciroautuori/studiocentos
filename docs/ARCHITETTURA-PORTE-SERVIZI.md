# Architettura Porte e Servizi - Docker Infrastructure

## 🌐 Overview Generale

Documentazione tecnica completa delle porte, servizi e configurazioni per l'infrastruttura Docker con Traefik centrale e le applicazioni ISS e Soliso.

---

## 📊 Mappatura Porte per Servizio

### 🔵 ISS (Innovazione Sociale Salernitana)
| Servizio | Container | Porta Interna | Porta Esposta | Network |
|----------|-----------|---------------|---------------|---------|
| Backend FastAPI | `iss-backend` | 8000 | via Traefik | `traefik-network` + `iss-internal` |
| PostgreSQL | `iss-postgres` | 5432 | 5432 (interno) | `iss-internal` |
| Frontend Next.js | `iss-frontend` | 3000 | 3000 (dev) | `traefik-network` + `iss-internal` |

**Domini SSL:**
- 🌍 `https://innovazionesocialesalernitana.it` (Frontend)
- 🔗 `https://innovazionesocialesalernitana.it/api` (Backend API)

### 🔴 Soliso (APS)
| Servizio | Container | Porta Interna | Porta Esposta | Network |
|----------|-----------|---------------|---------------|---------|
| Backend FastAPI | `soliso-backend` | 8001 | via Traefik | `traefik-network` + `soliso-internal` |
| PostgreSQL | `soliso-postgres` | 5433 | 5433 (interno) | `soliso-internal` |
| Frontend React | `soliso-frontend` | 80 | via Traefik | `traefik-network` |
| Admin Panel | `soliso-admin` | 80 | via Traefik | `traefik-network` |

**Domini SSL:**
- 🌍 `https://solisoaps.it` (Frontend)
- 🔗 `https://solisoaps.it/api` (Backend API)
- ⚙️ `https://admin.solisoaps.it` (Admin Panel)


### 🟡 Traefik Central
| Servizio | Container | Porta Interna | Porta Esposta | Network |
|----------|-----------|---------------|---------------|---------|
| Reverse Proxy | `traefik-central` | 80 | 80 | `traefik-network` |
| SSL Termination | `traefik-central` | 443 | 443 | `traefik-network` |
| Dashboard | `traefik-central` | 8080 | 8080 | `traefik-network` |

**Domini SSL:**
- 📊 `https://traefik.solisoaps.it` (Dashboard protetto)

---

## 🔒 Configurazione SSL/TLS

### Let's Encrypt Automatico
```yaml
certificatesresolvers.letsencrypt.acme.email=admin@solisoaps.it
certificatesresolvers.letsencrypt.acme.storage=/data/acme.json
certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web
```

### Redirect HTTP → HTTPS
```yaml
entrypoints.web.http.redirections.entrypoint.to=websecure
entrypoints.web.http.redirections.entrypoint.scheme=https
entrypoints.web.http.redirections.entrypoint.permanent=true
```

**⚠️ IMPORTANTE:** Il file `acme.json` deve avere permessi `600`:
```bash
chmod 600 traefik-central/traefik-data/acme.json
```

---

## 🌐 Network Architecture

### Shared Network
- **`traefik-network`**: Network esterno condiviso per routing Traefik
  - Tutti i servizi web esposti pubblicamente
  - Comunicazione inter-applicazione tramite Traefik

### Shared Networks
- **`postgres-network`**: Network condiviso per database centralizzato
  - PostgreSQL Central (porta 5432)  
  - Comunicazione tutte le app ↔ database centrale
  - PgAdmin per gestione web

### Internal Networks  
- **`iss-internal`**: Network privato per ISS (DEPRECATO - usa postgres-network)
- **`soliso-internal`**: Network privato per Soliso (DEPRECATO - usa postgres-network)


---

## 🚀 Comandi di Avvio

### PostgreSQL Central (PRIMO - Avvia per primo)
```bash
cd /home/bfiltoperator_gmail_com/docker-projects/server/postgress
./setup.sh  # Automated setup
# OR manual:
# cp .env.example .env
# docker-compose up -d
```

### Traefik Centrale
```bash
cd /home/bfiltoperator_gmail_com/docker-projects/server/traefik-central
docker-compose up -d
```

### Applications (dopo PostgreSQL Central)
```bash
# ISS Application
cd /home/bfiltoperator_gmail_com/docker-projects/apps/services/iss
docker-compose -f docker-compose.traefik.dev.yml up -d

# Soliso Application  
cd /home/bfiltoperator_gmail_com/docker-projects/apps/services/soliso
docker-compose -f docker-compose.traefik.yml up -d

# RimBuild Application
cd /home/bfiltoperator_gmail_com/docker-projects/apps/services/rimbuild
docker-compose up -d

# UMMR Application
cd /home/bfiltoperator_gmail_com/docker-projects/apps/services/ummr
docker-compose up -d
```

### Verifica Stato
```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker logs traefik-central
```

---

## 🔧 Variabili d'Ambiente Critiche

### ISS Backend
```env
DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@db:5432/iss_wbs
SECRET_KEY=iss-dev-secret-key-change-in-production
ALLOWED_ORIGINS=https://innovazionesocialesalernitana.it,https://admin.innovazionesocialesalernitana.it
BACKEND_INTERNAL_URL=http://backend:8000
```

### Soliso Backend
```env
DATABASE_URL=postgresql+psycopg2://root:password@postgres:5433/soliso_db
SECRET_KEY=your_secret_key_change_in_production
ROOT_PATH=/api
FRONTEND_URL=https://solisoaps.it
BACKEND_URL=https://solisoaps.it/api
```

---

## ⚠️ Conflicts Prevention

### Porte Riservate
- **5432**: PostgreSQL Central - Database centralizzato per TUTTE le app
- **5050**: PgAdmin Web UI - Gestione database centralizzato
- **8000**: Backend ISS - NON utilizzare per altri servizi
- **8001**: Backend Soliso - NON utilizzare per altri servizi
- **8002**: Backend RimBuild - NON utilizzare per altri servizi
- **8003**: Backend UMMR - NON utilizzare per altri servizi
- **80/443**: Traefik - Riservate per reverse proxy
- **8080**: Traefik Dashboard - Riservata

### Nuovi Servizi
Per aggiungere nuovi servizi:
1. Usare porte consecutive: `8004, 8005, ...` per backend
2. **NON serve più PostgreSQL dedicato** - usa PostgreSQL Central
3. Aggiungere al database: modifica `/server/postgress/init-scripts/01-create-databases.sql`
4. Aggiungere sempre ai network: `traefik-network` + `postgres-network`
5. Configurare SSL con `certresolver=letsencrypt`

---

## 📋 Health Checks

### Backend Services
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:PORT/')"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Traefik
```yaml
healthcheck:
  test: ["CMD", "traefik", "healthcheck"]
  interval: 30s
  timeout: 5s
  retries: 3
```

---

## 🐛 Troubleshooting Comune

### SSL Non Funziona
```bash
# Verificare permessi acme.json
chmod 600 traefik-central/traefik-data/acme.json
docker-compose restart traefik -f traefik-central/docker-compose.yml
```

### Conflitti di Porta
```bash
# Verificare porte in uso
netstat -tlnp | grep :PORTA
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### Database Connection Issues
```bash
# Verificare network connectivity
docker exec CONTAINER_NAME ping DATABASE_HOST
docker logs CONTAINER_NAME | grep -i database
```

### Router Non Trovato
```bash
# Verificare labels Traefik
docker inspect CONTAINER_NAME | grep traefik
docker logs traefik-central | grep -i router
```

---

## 🗄️ PostgreSQL Central - Migrazione

### Setup Iniziale
```bash
# 1. Avvia PostgreSQL Central
cd /home/bfiltoperator_gmail_com/docker-projects/server/postgress
./setup.sh

# 2. Verifica database creati
docker exec -it postgres-central psql -U postgres -c "\l"

# 3. PgAdmin Web UI (opzionale)  
# URL: http://localhost:5050
# Credentials: vedi .env file
```

### Migrazione Applicazioni
```bash
# Per ogni app, aggiorna docker-compose.yml:
# 1. RIMUOVI servizio PostgreSQL dedicato
# 2. AGGIUNGI network postgres-network  
# 3. AGGIORNA DATABASE_URL in .env

# Esempio DATABASE_URL:
# ISS: postgresql://iss_user:iss_secure_2024!@postgres-central:5432/iss_wbs
# Soliso: postgresql://soliso_user:soliso_secure_2024!@postgres-central:5432/soliso_db
```

### Backup & Monitoring
```bash
# Backup automatico tutti database
./server/postgress/scripts/backup-all.sh

# Restore database specifico
./server/postgress/scripts/restore-database.sh 20240922_120000 iss_wbs

# Monitoring connessioni
docker exec -it postgres-central psql -U postgres -c "SELECT * FROM pg_stat_activity;"
```

---

## 📝 Note per Team Sviluppo

1. **PostgreSQL Central obbligatorio** - NON creare più database dedicati
2. **Sempre usare network `postgres-network` + `traefik-network`**
3. **Testare SSL locale con domini configurati in `/etc/hosts`**
4. **Mai hardcodare porte - usare sempre variabili d'ambiente**
5. **Documentare ogni nuova porta/servizio in questo file**
6. **Verificare conflitti prima del deploy in produzione**

---

*Ultimo aggiornamento: 22 Settembre 2025*
*Maintainer: DevOps Team*
