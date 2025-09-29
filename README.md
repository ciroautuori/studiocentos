# 🚀 StudioCentOS - Monorepo

> Monorepo professionale con commit dedicati per progetto

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Git](https://img.shields.io/badge/Git-Workflow-orange.svg)]()
[![DevOps](https://img.shields.io/badge/DevOps-Ready-green.svg)]()

## 🏗️ Architettura

```
📁 studiocentos/
├── 📁 apps/                  # Applicazioni
│   ├── 📁 iss/               # ISS Project
│   ├── 📁 soliso/            # Soliso Project
│   └── 📁 studiocentos/      # StudioCentOS App
├── 📁 server/                # Infrastruttura Server
│   ├── 📁 postgress/         # PostgreSQL Database
│   └── 📁 traefik/           # Traefik Reverse Proxy
├── 📁 utils/                 # Utilities
├── 📁 docs/                  # Documentation
└── 📁 scripts/               # Automation Scripts
```

## 📝 Workflow Commit

### Pattern Commit Dedicati
```bash
# Ogni progetto mantiene i suoi commit separati
🎨 [ISS] Add new dashboard feature
⚙️ [SOLISO] Update API endpoints  
📱 [STUDIOCENTOS] Mobile app improvements
🗄️ [POSTGRES] Database schema migration
🔀 [TRAEFIK] Configure SSL certificates
```

### Workflow Standard
```bash
# 1. Lavora sul progetto specifico
cd apps/iss/
# ... fai modifiche ...

# 2. Torna alla root e commit dedicato
cd ../..
git add apps/iss/
git commit -m "🎨 [ISS] Descrizione modifica

✅ Modifiche:
- Feature implementata
- Bug corretti

📁 Path: apps/iss/
🕐 $(date +'%Y-%m-%d %H:%M:%S')"

# 3. Push
git push origin main
```

## 🚀 Quick Start

### Commit Smart (con script helper)
```bash
# Commit automatico per area con emoji e prefix
./scripts/smart-commit.sh apps/iss "Add new feature"
./scripts/smart-commit.sh apps/soliso "Update backend"
./scripts/smart-commit.sh server/traefik "SSL config"
```

### Setup Nuovo Progetto
```bash
# Crea nuovo progetto con template
./scripts/setup-new-project.sh my-app frontend
```

### Pre-Deploy Check
```bash
# Verifica modifiche non committate
./scripts/deploy-check.sh
```

## 🎯 Progetti Attivi

### Apps
- **ISS** - Sistema ISS
- **Soliso** - Applicazione Soliso
- **StudioCentOS** - App principale

### Server/Infrastructure
- **PostgreSQL** - Database principale
- **Traefik** - Reverse proxy e SSL

## 📚 Vantaggi Setup

✅ **Repository unico** - Tutto centralizzato su GitHub  
✅ **Commit dedicati** - Ogni progetto con history separata  
✅ **Zero conflitti** - Lavoro parallelo su progetti diversi  
✅ **History pulita** - Prefissi [AREA] per identificazione  
✅ **Collaborazione team** - Workflow ottimizzato  
✅ **GitHub friendly** - Insights, blame, graph funzionano perfettamente

## 📚 Documentation

- [Development Workflow](docs/DEVELOPMENT.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Monorepo Setup Guide](MONOREPO_SETUP_GUIDE.md)

---

**Created:** 2025-09-29  
**Author:** Ciro Autuori  
**License:** MIT  
**Repository:** https://github.com/ciroautuori/studiocentos.git
