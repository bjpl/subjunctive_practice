-- Database Initialization Script
-- Spanish Subjunctive Practice Application

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database if not exists (already created by Docker)
-- CREATE DATABASE subjunctive_practice;

-- Set timezone to UTC
SET timezone = 'UTC';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE subjunctive_practice TO app_user;

-- Create schema
CREATE SCHEMA IF NOT EXISTS public;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO app_user;

-- Enable row-level security if needed
-- ALTER DATABASE subjunctive_practice SET row_security = on;

-- Create custom functions or triggers here if needed

COMMENT ON DATABASE subjunctive_practice IS 'Spanish Subjunctive Practice Learning Application';
