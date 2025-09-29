# 🗄️ PostgreSQL Central Server

PostgreSQL centralizzato per tutte le applicazioni del server. Gestisce multiple applicazioni con database separati, backup automatizzati e interfaccia di amministrazione.

## 📊 **Architettura**

```
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL Central                        │
│                     (Port 5432)                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────┐ │
│  │  iss_wbs    │ │ soliso_db   │ │rimbuild_db  │ │ummr_db │ │
│  │             │ │             │ │             │ │        │ │
│  │ iss_user    │ │soliso_user  │ │rimbuild_user│ │ummr_user│ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
              │                              │
              ▼                              ▼
    ┌─────────────────┐              ┌─────────────────┐
    │   Applications  │              │   PgAdmin Web   │
    │   (Backend)     │              │  (Port 5050)    │
    │                 │              │                 │
    │  ISS:8000       │              │ admin interface │
    │  Soliso:8001    │              │ for monitoring  │
    │  RimBuild:8002  │              │ and management  │
    │  UMMR:8003      │              │                 │
    └─────────────────┘              └─────────────────┘
```

## 🚀 **Avvio Rapido**

### 1. Configurazione Environment
```bash
cp .env.example .env
# Modifica le credenziali in .env
```

### 2. Avvio PostgreSQL Central
```bash
docker-compose up -d
```

### 3. Verifica Stato
```bash
docker-compose ps
docker logs postgres-central
```

### 4. Accesso PgAdmin (Opzionale)
- URL: `http://localhost:5050` o `https://pgadmin.yourdomain.com`
- Email: `admin@yourdomain.com`
- Password: vedi `.env` file

## 🗄️ **Database Configurati**

| Applicazione | Database | Utente | Porta App |
|-------------|----------|---------|-----------|
| **ISS WBS** | `iss_wbs` | `iss_user` | 8000 |
| **Soliso APS** | `soliso_db` | `soliso_user` | 8001 |
| **RimBuild** | `rimbuild_db` | `rimbuild_user` | 8002 |
| **UMMR** | `ummr_db` | `ummr_user` | 8003 |

## 🔗 **Connection Strings**

### Per le Applicazioni (internal network)
```bash
# ISS
DATABASE_URL=postgresql://iss_user:iss_secure_2024!@postgres-central:5432/iss_wbs

# Soliso  
DATABASE_URL=postgresql://soliso_user:soliso_secure_2024!@postgres-central:5432/soliso_db

# RimBuild
DATABASE_URL=postgresql://rimbuild_user:rimbuild_secure_2024!@postgres-central:5432/rimbuild_db

# UMMR
DATABASE_URL=postgresql://ummr_user:ummr_secure_2024!@postgres-central:5432/ummr_db
```

### Per Connessioni Esterne
```bash
Host: localhost (o IP server)
Port: 5432
Database: [nome_database]  
Username: [utente_specifico]
Password: [vedi .env file]
```

## 💾 **Backup & Restore**

### Backup Automatico
```bash
# Backup di tutti i database
./scripts/backup-all.sh

# Il backup viene salvato in ./backups/YYYYMMDD_HHMMSS/
```

### Restore Database
```bash
# Restore di un database specifico
./scripts/restore-database.sh 20240922_120000 iss_wbs

# Lista backup disponibili
ls -la ./backups/
```

### Backup Scheduling (Cron)
```bash
# Aggiungi a crontab per backup giornaliero alle 2:00
0 2 * * * cd /path/to/postgress && ./scripts/backup-all.sh
```

## 🔧 **Manutenzione**

### Comandi Utili
```bash
# Stato container
docker-compose ps

# Log PostgreSQL
docker logs postgres-central -f

# Accesso diretto database
docker exec -it postgres-central psql -U postgres

# Statistiche performance
docker exec -it postgres-central psql -U postgres -c "SELECT * FROM pg_stat_database;"

# Spazio utilizzato database
docker exec -it postgres-central psql -U postgres -c "
SELECT datname, pg_size_pretty(pg_database_size(datname)) 
FROM pg_database 
WHERE datistemplate = false;"
```

### Performance Monitoring
```bash
# Query lente (>1 secondo)
docker exec -it postgres-central psql -U postgres -c "
SELECT query, calls, total_time, mean_time 
FROM pg_stat_statements 
ORDER BY total_time DESC 
LIMIT 10;"

# Connessioni attive
docker exec -it postgres-central psql -U postgres -c "
SELECT datname, usename, application_name, client_addr, state 
FROM pg_stat_activity 
WHERE state = 'active';"
```

## 🔐 **Sicurezza**

### Credenziali
- ✅ Password crittografate con SCRAM-SHA-256
- ✅ Utenti dedicati per ogni applicazione
- ✅ Privilegi minimi necessari
- ✅ Monitoraggio utente read-only

### Network Security
- ✅ Container isolato in `postgres-network`  
- ✅ Accesso esterno solo via porta esposta
- ✅ SSL gestito da Traefik per connessioni web

### Backup Security
- ✅ Backup compressi e crittografati
- ✅ Retention automatica (30 giorni default)
- ✅ Log di tutte le operazioni

## 📈 **Ottimizzazioni Performance**

### Configurazione Ottimizzata per Multi-Tenant
- **Shared Buffers**: 256MB (memoria condivisa)
- **Effective Cache Size**: 1GB (cache SO)
- **Work Memory**: 4MB per connessione
- **Max Connections**: 200 (per tutte le app)
- **WAL Settings**: Ottimizzati per SSD

### Monitoraggio Attivo
- **Auto-vacuum**: Configurato per performance
- **Query Statistics**: Tracciamento query lente
- **Connection Pooling**: Gestito dalle applicazioni

## 🆘 **Troubleshooting**

### Problemi Comuni

**Database non si connette:**
```bash
# Verifica container attivo
docker-compose ps postgres-central

# Verifica network
docker network ls | grep postgres

# Test connessione
docker exec -it postgres-central pg_isready
```

**Performance lente:**
```bash
# Analizza query lente
docker exec -it postgres-central psql -U postgres -d iss_wbs -c "
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 5;"

# Verifica spazio disco
docker exec -it postgres-central df -h
```

**Backup fallito:**
```bash
# Verifica permessi
ls -la ./backups/
chmod +x ./scripts/backup-all.sh

# Test backup manuale
./scripts/backup-all.sh
```

## 📝 **File di Configurazione**

| File | Descrizione |
|------|-------------|
| `docker-compose.yml` | Configurazione container principale |
| `.env` | Variabili ambiente e credenziali |
| `postgresql.conf` | Configurazione PostgreSQL ottimizzata |
| `init-scripts/01-create-databases.sql` | Setup iniziale database |
| `servers.json` | Configurazione PgAdmin |
| `scripts/backup-all.sh` | Script backup automatico |
| `scripts/restore-database.sh` | Script restore database |

---

## 🎯 **Vantaggi del Setup Centralizzato**

✅ **Risparmio Risorse**: Un solo container PostgreSQL invece di 4  
✅ **Gestione Centralizzata**: Backup, monitoring, manutenzione unificati  
✅ **Scalabilità**: Facile aggiunta di nuove applicazioni  
✅ **Sicurezza**: Controllo accessi centralizzato  
✅ **Performance**: Configurazione ottimizzata per multi-tenant  
✅ **Affidabilità**: Backup automatizzati e recovery procedure  

---

*Ultimo aggiornamento: 22 Settembre 2025*  
*Maintainer: DevOps Team*
