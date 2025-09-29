#!/bin/bash

# =========================================
# PostgreSQL Central - Setup Script
# Automated setup for centralized PostgreSQL
# =========================================

set -e

echo "🗄️ PostgreSQL Central Setup"
echo "=============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root (for network creation)
check_docker_permissions() {
    if ! docker ps &> /dev/null; then
        echo -e "${RED}❌ Docker not accessible. Please run with sudo or add user to docker group${NC}"
        exit 1
    fi
}

# Create required networks
create_networks() {
    echo -e "${BLUE}🔗 Creating Docker networks...${NC}"
    
    # Create postgres network if not exists
    if ! docker network inspect postgres-network &> /dev/null; then
        echo "📡 Creating postgres-network..."
        docker network create postgres-network \
            --driver bridge \
            --subnet=172.20.0.0/16 \
            --gateway=172.20.0.1
        echo -e "${GREEN}✅ postgres-network created${NC}"
    else
        echo -e "${YELLOW}ℹ️ postgres-network already exists${NC}"
    fi
    
    # Create traefik network if not exists  
    if ! docker network inspect traefik-network &> /dev/null; then
        echo "📡 Creating traefik-network..."
        docker network create traefik-network \
            --driver bridge \
            --subnet=172.21.0.0/16 \
            --gateway=172.21.0.1
        echo -e "${GREEN}✅ traefik-network created${NC}"
    else
        echo -e "${YELLOW}ℹ️ traefik-network already exists${NC}"
    fi
}

# Setup environment file
setup_environment() {
    echo -e "${BLUE}⚙️ Setting up environment...${NC}"
    
    if [ ! -f .env ]; then
        echo "📄 Creating .env from template..."
        cp .env.example .env
        
        # Generate secure passwords
        POSTGRES_PASS=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        PGADMIN_PASS=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
        
        # Update .env with generated passwords
        sed -i "s/centralPostgres2024!/${POSTGRES_PASS}/" .env
        sed -i "s/adminPass123!/${PGADMIN_PASS}/" .env
        
        echo -e "${GREEN}✅ .env file created with secure passwords${NC}"
        echo -e "${YELLOW}🔐 IMPORTANT: Save these credentials securely!${NC}"
        echo "   PostgreSQL Password: ${POSTGRES_PASS}"
        echo "   PgAdmin Password: ${PGADMIN_PASS}"
    else
        echo -e "${YELLOW}ℹ️ .env file already exists${NC}"
    fi
}

# Create required directories
create_directories() {
    echo -e "${BLUE}📁 Creating directories...${NC}"
    
    directories=(
        "./data/postgres"
        "./backups"
        "./logs"
    )
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo "📂 Created: $dir"
        fi
    done
    
    # Set proper permissions
    chmod 755 ./data/postgres
    chmod 755 ./backups
    chmod +x ./scripts/*.sh
    
    echo -e "${GREEN}✅ Directories created${NC}"
}

# Start PostgreSQL Central
start_services() {
    echo -e "${BLUE}🚀 Starting PostgreSQL Central...${NC}"
    
    # Pull latest images
    docker-compose pull
    
    # Start services
    docker-compose up -d
    
    echo "⏳ Waiting for PostgreSQL to be ready..."
    sleep 10
    
    # Check if PostgreSQL is healthy
    for i in {1..30}; do
        if docker exec postgres-central pg_isready &> /dev/null; then
            echo -e "${GREEN}✅ PostgreSQL is ready!${NC}"
            break
        fi
        
        if [ $i -eq 30 ]; then
            echo -e "${RED}❌ PostgreSQL failed to start after 30 attempts${NC}"
            echo "📋 Container logs:"
            docker logs postgres-central --tail 20
            exit 1
        fi
        
        echo "⏳ Attempt $i/30 - waiting for PostgreSQL..."
        sleep 2
    done
}

# Verify installation
verify_installation() {
    echo -e "${BLUE}🔍 Verifying installation...${NC}"
    
    # Check container status
    echo "📊 Container status:"
    docker-compose ps
    
    echo ""
    echo "🗄️ Database verification:"
    
    # List databases
    docker exec postgres-central psql -U postgres -c "\\l" | grep -E "(iss_wbs|soliso_db|rimbuild_db|ummr_db)" && {
        echo -e "${GREEN}✅ Application databases created successfully${NC}"
    } || {
        echo -e "${RED}❌ Application databases not found${NC}"
        exit 1
    }
    
    # Test connections for each app database
    databases=("iss_wbs:iss_user" "soliso_db:soliso_user" "rimbuild_db:rimbuild_user" "ummr_db:ummr_user")
    
    for db_config in "${databases[@]}"; do
        IFS=':' read -r DB_NAME DB_USER <<< "$db_config"
        
        if docker exec postgres-central psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" &> /dev/null; then
            echo -e "${GREEN}✅ $DB_NAME ($DB_USER) - Connection OK${NC}"
        else
            echo -e "${RED}❌ $DB_NAME ($DB_USER) - Connection FAILED${NC}"
        fi
    done
}

# Display final information
show_final_info() {
    echo ""
    echo -e "${GREEN}🎉 PostgreSQL Central Setup Completed!${NC}"
    echo "=================================="
    echo ""
    echo "📊 Service Information:"
    echo "   PostgreSQL: localhost:5432"
    echo "   PgAdmin: http://localhost:5050"
    echo ""
    echo "🗄️ Application Databases:"
    echo "   ISS WBS: postgresql://iss_user:***@postgres-central:5432/iss_wbs" 
    echo "   Soliso: postgresql://soliso_user:***@postgres-central:5432/soliso_db"
    echo "   RimBuild: postgresql://rimbuild_user:***@postgres-central:5432/rimbuild_db"
    echo "   UMMR: postgresql://ummr_user:***@postgres-central:5432/ummr_db"
    echo ""
    echo "🔧 Management Commands:"
    echo "   Backup All: ./scripts/backup-all.sh"
    echo "   Restore DB: ./scripts/restore-database.sh <date> <db_name>"
    echo "   Logs: docker logs postgres-central -f"
    echo "   Status: docker-compose ps"
    echo ""
    echo "📖 Documentation:"
    echo "   README.md - Complete documentation"
    echo "   MIGRATION_GUIDE.md - Migration from dedicated PostgreSQL"
    echo ""
    echo -e "${YELLOW}⚠️ Next Steps:${NC}"
    echo "1. Update application docker-compose.yml files (see MIGRATION_GUIDE.md)"
    echo "2. Update DATABASE_URL in application .env files"
    echo "3. Add postgres-network to application networks"
    echo "4. Migrate existing data (see migration guide)"
    echo ""
    echo -e "${BLUE}🔐 Credentials stored in .env file${NC}"
}

# Main execution
main() {
    echo "Starting PostgreSQL Central setup..."
    
    check_docker_permissions
    create_networks
    setup_environment
    create_directories
    start_services
    verify_installation
    show_final_info
}

# Execute main function
main "$@"
