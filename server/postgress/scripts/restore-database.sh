#!/bin/bash

# =========================================
# PostgreSQL Central - Restore Database
# Usage: ./restore-database.sh <backup_date> <database_name>
# Example: ./restore-database.sh 20240922_120000 iss_wbs
# =========================================

set -e

if [ $# -ne 2 ]; then
    echo "❌ Usage: $0 <backup_date> <database_name>"
    echo "📅 Available backups:"
    ls -la /backups/ | grep "^d" | awk '{print $9}' | grep -E "^[0-9]{8}_[0-9]{6}$" || echo "No backups found"
    echo ""
    echo "🗄️ Available databases: iss_wbs, soliso_db, rimbuild_db, ummr_db"
    exit 1
fi

BACKUP_DATE="$1"
DATABASE_NAME="$2"
BACKUP_DIR="/backups/$BACKUP_DATE"
BACKUP_FILE="$BACKUP_DIR/${DATABASE_NAME}_backup.sql.dump"

echo "🔄 Starting database restore..."
echo "📅 Backup date: $BACKUP_DATE"
echo "🗄️ Database: $DATABASE_NAME"
echo "📁 Backup file: $BACKUP_FILE"

# Verify backup exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    echo "📁 Available backups in $BACKUP_DIR:"
    ls -la "$BACKUP_DIR"/*.dump 2>/dev/null || echo "No dump files found"
    exit 1
fi

# Confirm restore
echo ""
echo "⚠️  WARNING: This will REPLACE all data in database '$DATABASE_NAME'"
echo "📋 Backup info:"
if [ -f "$BACKUP_DIR/backup_manifest.json" ]; then
    cat "$BACKUP_DIR/backup_manifest.json" | grep -A5 -B5 "$DATABASE_NAME" || true
fi

read -p "🤔 Do you want to continue? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 1
fi

echo ""
echo "🚀 Starting restore process..."

# Create temporary restoration script
RESTORE_SCRIPT="/tmp/restore_${DATABASE_NAME}_${BACKUP_DATE}.sh"
cat > "$RESTORE_SCRIPT" << EOF
#!/bin/bash
set -e

echo "📊 Current database size before restore:"
PGPASSWORD="postgres" psql -h postgres-central -U postgres -d postgres -c "
    SELECT pg_database.datname as database_name, 
           pg_size_pretty(pg_database_size(pg_database.datname)) AS size
    FROM pg_database 
    WHERE datname = '$DATABASE_NAME';"

echo "🗑️ Dropping existing database connections..."
PGPASSWORD="postgres" psql -h postgres-central -U postgres -d postgres -c "
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '$DATABASE_NAME'
      AND pid <> pg_backend_pid();"

echo "🔄 Restoring database from backup..."
PGPASSWORD="postgres" pg_restore \
    -h postgres-central \
    -U postgres \
    -d postgres \
    --clean \
    --if-exists \
    --create \
    --verbose \
    "$BACKUP_FILE"

echo "📊 Database size after restore:"
PGPASSWORD="postgres" psql -h postgres-central -U postgres -d postgres -c "
    SELECT pg_database.datname as database_name, 
           pg_size_pretty(pg_database_size(pg_database.datname)) AS size
    FROM pg_database 
    WHERE datname = '$DATABASE_NAME';"

echo "🔍 Verifying restore..."
PGPASSWORD="postgres" psql -h postgres-central -U postgres -d "$DATABASE_NAME" -c "
    SELECT 'Database restored successfully!' as status,
           current_database() as database,
           current_user as user,
           version() as postgres_version;"
EOF

chmod +x "$RESTORE_SCRIPT"

# Execute restore
bash "$RESTORE_SCRIPT"

# Cleanup
rm "$RESTORE_SCRIPT"

echo ""
echo "✅ Database restore completed successfully!"
echo "🗄️ Database: $DATABASE_NAME"
echo "📅 Restored from backup: $BACKUP_DATE" 
echo "🕐 Completed at: $(date)"

# Log restore operation
LOG_FILE="/backups/restore.log"
echo "$(date -Iseconds) - RESTORE: $DATABASE_NAME from $BACKUP_DATE - SUCCESS" >> "$LOG_FILE"
