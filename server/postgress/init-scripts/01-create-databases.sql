-- =========================================
-- PostgreSQL Central - Database Initialization
-- Creates databases and users for all applications
-- =========================================

-- Create ISS Database and User
CREATE DATABASE iss_wbs;
CREATE USER iss_user WITH ENCRYPTED PASSWORD 'iss_secure_2024!';
GRANT ALL PRIVILEGES ON DATABASE iss_wbs TO iss_user;
ALTER USER iss_user CREATEDB;

-- Create Soliso Database and User  
CREATE DATABASE soliso_db;
CREATE USER soliso_user WITH ENCRYPTED PASSWORD 'soliso_secure_2024!';
GRANT ALL PRIVILEGES ON DATABASE soliso_db TO soliso_user;
ALTER USER soliso_user CREATEDB;

-- Create RimBuild Database and User
CREATE DATABASE rimbuild_db;
CREATE USER rimbuild_user WITH ENCRYPTED PASSWORD 'rimbuild_secure_2024!';
GRANT ALL PRIVILEGES ON DATABASE rimbuild_db TO rimbuild_user;
ALTER USER rimbuild_user CREATEDB;

-- Create UMMR Database and User
CREATE DATABASE ummr_db;
CREATE USER ummr_user WITH ENCRYPTED PASSWORD 'ummr_secure_2024!';
GRANT ALL PRIVILEGES ON DATABASE ummr_db TO ummr_user;
ALTER USER ummr_user CREATEDB;

-- =========================================
-- 🔐 SECURITY ENHANCEMENTS
-- =========================================

-- Create read-only monitoring user
CREATE USER monitor_user WITH ENCRYPTED PASSWORD 'monitor_readonly_2024!';
GRANT CONNECT ON DATABASE iss_wbs TO monitor_user;
GRANT CONNECT ON DATABASE soliso_db TO monitor_user;  
GRANT CONNECT ON DATABASE rimbuild_db TO monitor_user;
GRANT CONNECT ON DATABASE ummr_db TO monitor_user;

-- Grant read-only access to all tables (will be applied by each app)
-- Apps need to run: GRANT SELECT ON ALL TABLES IN SCHEMA public TO monitor_user;

-- =========================================
-- 📊 DATABASE CONFIGURATION
-- =========================================

-- ISS Database specific configuration
\c iss_wbs;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE SCHEMA IF NOT EXISTS analytics;
GRANT ALL ON SCHEMA analytics TO iss_user;

-- Soliso Database specific configuration  
\c soliso_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE SCHEMA IF NOT EXISTS events;
CREATE SCHEMA IF NOT EXISTS projects;
GRANT ALL ON SCHEMA events TO soliso_user;
GRANT ALL ON SCHEMA projects TO soliso_user;

-- RimBuild Database specific configuration
\c rimbuild_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE SCHEMA IF NOT EXISTS builds;
CREATE SCHEMA IF NOT EXISTS reports;
GRANT ALL ON SCHEMA builds TO rimbuild_user;
GRANT ALL ON SCHEMA reports TO rimbuild_user;

-- UMMR Database specific configuration
\c ummr_db;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE SCHEMA IF NOT EXISTS monitoring;
CREATE SCHEMA IF NOT EXISTS metrics;
GRANT ALL ON SCHEMA monitoring TO ummr_user;
GRANT ALL ON SCHEMA metrics TO ummr_user;

-- =========================================
-- ✅ COMPLETION LOG
-- =========================================
\c postgres;
INSERT INTO pg_stat_statements_info VALUES ('PostgreSQL Central Setup Completed', CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;
