# 🛠️ Development Workflow

## Commit Smart per Progetto

```bash
# ISS
./scripts/smart-commit.sh apps/iss "Descrizione modifica"

# Soliso
./scripts/smart-commit.sh apps/soliso "Descrizione modifica"

# Infrastruttura
./scripts/smart-commit.sh server/traefik "Descrizione modifica"
```

## Workflow Standard

```bash
# 1. Lavora sul progetto
cd apps/iss/

# 2. Torna alla root
cd ../..

# 3. Commit dedicato
git add apps/iss/
git commit -m "🎨 [ISS] Descrizione"

# 4. Push
git push origin main
```
