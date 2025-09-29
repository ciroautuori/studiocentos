#!/bin/bash

# =========================================
# PostgreSQL Central - Backup All Databases
# =========================================

set -e

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

# Database configurations
DATABASES=(
    "iss_wbs:iss_user"
    "soliso_db:soliso_user" 
    "rimbuild_db:rimbuild_user"
    "ummr_db:ummr_user"
)

echo "🗄️ Starting PostgreSQL Central Backup - $(date)"
echo "📅 Backup date: $DATE"
echo "📁 Backup directory: $BACKUP_DIR"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR/$DATE"

# Backup each database
for db_config in "${DATABASES[@]}"; do
    IFS=':' read -r DB_NAME DB_USER <<< "$db_config"
    
    echo "📦 Backing up database: $DB_NAME (user: $DB_USER)"
    
    BACKUP_FILE="$BACKUP_DIR/$DATE/${DB_NAME}_backup.sql"
    
    # Create compressed backup
    PGPASSWORD="postgres" pg_dump \
        -h postgres-central \
        -U postgres \
        -d "$DB_NAME" \
        --verbose \
        --clean \
        --if-exists \
        --create \
        --format=custom \
        --compress=9 \
        --file="$BACKUP_FILE.dump"
    
    # Create human-readable SQL backup
    PGPASSWORD="postgres" pg_dump \
        -h postgres-central \
        -U postgres \
        -d "$DB_NAME" \
        --verbose \
        --clean \
        --if-exists \
        --create \
        --format=plain \
        --file="$BACKUP_FILE"
    
    # Compress SQL backup
    gzip "$BACKUP_FILE"
    
    echo "✅ Backup completed: ${DB_NAME}_backup.sql.gz ($(stat -f%z "$BACKUP_FILE.gz" 2>/dev/null || stat -c%s "$BACKUP_FILE.gz")bytes)"
done

# Create global backup (all databases)
echo "🌐 Creating global backup..."
GLOBAL_BACKUP="$BACKUP_DIR/$DATE/postgresql_global_backup.sql"

PGPASSWORD="postgres" pg_dumpall \
    -h postgres-central \
    -U postgres \
    --verbose \
    --clean \
    --file="$GLOBAL_BACKUP"

gzip "$GLOBAL_BACKUP"

echo "✅ Global backup completed: postgresql_global_backup.sql.gz"

# Create backup manifest
MANIFEST_FILE="$BACKUP_DIR/$DATE/backup_manifest.json"
cat > "$MANIFEST_FILE" << EOF
{
  "backup_date": "$DATE",
  "backup_timestamp": "$(date -Iseconds)",
  "postgres_version": "$(PGPASSWORD=postgres psql -h postgres-central -U postgres -t -c 'SELECT version();' | xargs)",
  "databases": [
$(for db_config in "${DATABASES[@]}"; do
    IFS=':' read -r DB_NAME DB_USER <<< "$db_config"
    echo "    {\"name\": \"$DB_NAME\", \"user\": \"$DB_USER\", \"file\": \"${DB_NAME}_backup.sql.gz\"},"
done | sed '$ s/,$//')
  ],
  "global_backup": "postgresql_global_backup.sql.gz",
  "retention_days": $RETENTION_DAYS
}
EOF

echo "📋 Backup manifest created: backup_manifest.json"

# Cleanup old backups
echo "🧹 Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -type d -name "*_*" -mtime +$RETENTION_DAYS -exec rm -rf {} + 2>/dev/null || true

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR/$DATE" | cut -f1)
echo "💾 Total backup size: $TOTAL_SIZE"

echo "🎉 Backup completed successfully - $(date)"
echo "📍 Backup location: $BACKUP_DIR/$DATE"
