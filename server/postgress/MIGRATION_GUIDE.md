# 🔄 Guida Migrazione a PostgreSQL Centralizzato

Questa guida ti aiuta a migrare le applicazioni esistenti dal PostgreSQL dedicato al PostgreSQL centralizzato.

## 🗄️ **1. Modifiche Database URL**

### ISS Application
```bash
# PRIMA (PostgreSQL dedicato)
DATABASE_URL=postgresql://postgres:password@iss-postgres:5432/iss_wbs

# DOPO (PostgreSQL centralizzato)  
DATABASE_URL=postgresql://iss_user:iss_secure_2024!@postgres-central:5432/iss_wbs
```

### Soliso Application
```bash
# PRIMA (PostgreSQL dedicato)
DATABASE_URL=postgresql://root:password@postgres:5433/soliso_db

# DOPO (PostgreSQL centralizzato)
DATABASE_URL=postgresql://soliso_user:soliso_secure_2024!@postgres-central:5432/soliso_db
```

### RimBuild Application
```bash
# PRIMA (PostgreSQL dedicato)
DATABASE_URL=postgresql://postgres:password@rimbuild-postgres:5432/rimbuild_db

# DOPO (PostgreSQL centralizzato)
DATABASE_URL=postgresql://rimbuild_user:rimbuild_secure_2024!@postgres-central:5432/rimbuild_db
```

### UMMR Application
```bash
# PRIMA (PostgreSQL dedicato)
DATABASE_URL=postgresql://postgres:password@ummr-postgres:5432/ummr_db

# DOPO (PostgreSQL centralizzato)
DATABASE_URL=postgresql://ummr_user:ummr_secure_2024!@postgres-central:5432/ummr_db
```

## 🐳 **2. Modifiche Docker Compose**

### RIMUOVI dalle applicazioni:
```yaml
# ❌ RIMUOVI questo blocco da ogni docker-compose.yml
services:
  postgres:  # o db, database, etc.
    image: postgres:15-alpine
    container_name: app-postgres
    environment:
      POSTGRES_DB: app_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-internal

volumes:
  postgres_data:
```

### AGGIUNGI alle applicazioni:
```yaml
# ✅ AGGIUNGI questa configurazione network
networks:
  postgres-network:
    external: true
    
services:
  backend:  # o il tuo servizio backend
    # ... altre configurazioni ...
    networks:
      - traefik-network
      - postgres-network  # ← AGGIUNGI questa linea
    depends_on:
      - postgres-central  # ← OPZIONALE: dipendenza esplicita
```

## 🔧 **3. Script di Migrazione Dati**

### Backup Database Esistente
```bash
# ISS
docker exec iss-postgres pg_dump -U postgres iss_wbs > iss_backup.sql

# Soliso  
docker exec soliso-postgres pg_dump -U root soliso_db > soliso_backup.sql

# E così via per ogni app...
```

### Restore nel PostgreSQL Centralizzato
```bash
# 1. Avvia PostgreSQL Central
cd /path/to/server/postgress
docker-compose up -d

# 2. Restore data (esempio ISS)
docker exec -i postgres-central psql -U iss_user -d iss_wbs < iss_backup.sql

# Oppure usa lo script dedicato
./scripts/restore-database.sh [backup_date] iss_wbs
```

## 🔄 **4. Procedura Completa Step-by-Step**

### Step 1: Avvia PostgreSQL Central
```bash
cd /home/bfiltoperator_gmail_com/docker-projects/server/postgress
cp .env.example .env
# Configura le credenziali in .env
docker-compose up -d
```

### Step 2: Backup Database Esistenti  
```bash
# Per ogni applicazione, esegui backup
cd /path/to/app
docker-compose exec postgres pg_dump -U [user] [database] > backup.sql
```

### Step 3: Aggiorna Configurazione App
```bash
# Modifica docker-compose.yml (rimuovi postgres, aggiungi network)
# Modifica .env (aggiorna DATABASE_URL)
```

### Step 4: Restore Data
```bash
# Importa dati nel PostgreSQL Central
docker exec -i postgres-central psql -U [new_user] -d [database] < backup.sql
```

### Step 5: Test & Deploy
```bash
# Riavvia applicazione con nuova configurazione
cd /path/to/app
docker-compose down
docker-compose up -d

# Verifica connessione database
docker logs [app-backend-container]
```

## 🛠️ **5. File di Configurazione Template**

### Template .env per Applicazioni
```bash
# Database Configuration (PostgreSQL Central)
DATABASE_URL=postgresql://[app_user]:[password]@postgres-central:5432/[app_database]

# Altri parametri dell'applicazione...
BACKEND_URL=http://backend:[port]
FRONTEND_URL=https://[domain]
```

### Template docker-compose.yml sezione networks
```yaml
version: '3.8'

services:
  backend:
    # ... configurazione esistente ...
    networks:
      - traefik-network
      - postgres-network  # ← PostgreSQL Central
    environment:
      - DATABASE_URL=postgresql://app_user:password@postgres-central:5432/app_db

networks:
  traefik-network:
    external: true
  postgres-network:
    external: true
```

## ✅ **6. Checklist Migrazione**

### Pre-Migrazione
- [ ] PostgreSQL Central avviato e funzionante
- [ ] Database e utenti creati automaticamente
- [ ] Backup database esistenti completato
- [ ] Network `postgres-network` creato

### Durante Migrazione  
- [ ] Configurazione DATABASE_URL aggiornata
- [ ] Servizi PostgreSQL dedicati rimossi da docker-compose
- [ ] Network postgres-network aggiunto alle applicazioni
- [ ] Dati importati nel PostgreSQL Central

### Post-Migrazione
- [ ] Applicazioni si connettono correttamente
- [ ] Dati integri e accessibili  
- [ ] Performance accettabili
- [ ] Backup automatico configurato
- [ ] Monitoring attivo via PgAdmin

## 🆘 **7. Troubleshooting**

### Errore di Connessione
```bash
# Verifica che l'app sia nel network giusto
docker network inspect postgres-network

# Test connessione dal container dell'app
docker exec -it [app-container] ping postgres-central
```

### Errore di Autenticazione
```bash
# Verifica credenziali nel PostgreSQL Central
docker exec -it postgres-central psql -U postgres -c "\\du"

# Reset password se necessario
docker exec -it postgres-central psql -U postgres -c "
ALTER USER app_user WITH PASSWORD 'new_password';"
```

### Performance Issues
```bash
# Monitora connessioni attive
docker exec -it postgres-central psql -U postgres -c "
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"

# Verifica query lente
docker exec -it postgres-central psql -U postgres -c "
SELECT query, calls, total_time FROM pg_stat_statements 
ORDER BY total_time DESC LIMIT 10;"
```

---

## 💡 **Vantaggi Post-Migrazione**

✅ **Riduzione Risorse**: Da 4 container PostgreSQL a 1  
✅ **Gestione Unificata**: Backup e monitoring centralizzati  
✅ **Sicurezza Migliorata**: Controllo accessi granulare  
✅ **Manutenzione Semplificata**: Un solo container da aggiornare  
✅ **Scalabilità**: Facile aggiunta di nuove applicazioni  

*La migrazione può essere fatta gradualmente, un'applicazione alla volta.*
