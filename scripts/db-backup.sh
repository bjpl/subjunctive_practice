#!/bin/bash

# Database Backup Script for Railway PostgreSQL
# Spanish Subjunctive Practice Application

set -e  # Exit on error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install it first."
        exit 1
    fi
}

# Create backup directory
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# Get database URL from Railway
get_database_url() {
    log_info "Fetching database URL from Railway..."

    check_command "railway"

    # Get DATABASE_URL from Railway
    DATABASE_URL=$(railway variables get DATABASE_URL 2>/dev/null || echo "")

    if [ -z "$DATABASE_URL" ]; then
        log_error "Could not fetch DATABASE_URL from Railway"
        log_info "Trying alternative method..."

        # Alternative: use railway run to get env var
        DATABASE_URL=$(railway run printenv DATABASE_URL 2>/dev/null || echo "")

        if [ -z "$DATABASE_URL" ]; then
            log_error "Failed to get DATABASE_URL. Make sure you're in the right Railway project."
            exit 1
        fi
    fi

    log_success "Database URL retrieved"
}

# Backup database
backup_database() {
    local backup_file="$BACKUP_DIR/backup_${TIMESTAMP}.sql"
    local backup_file_compressed="${backup_file}.gz"

    log_info "Starting database backup..."
    log_info "Backup file: $backup_file_compressed"

    # Use pg_dump via Railway
    railway run pg_dump "$DATABASE_URL" > "$backup_file" || {
        log_error "Database backup failed"
        rm -f "$backup_file"
        exit 1
    }

    # Compress backup
    log_info "Compressing backup..."
    gzip "$backup_file"

    # Get file size
    BACKUP_SIZE=$(du -h "$backup_file_compressed" | cut -f1)

    log_success "Database backup completed"
    log_info "Backup size: $BACKUP_SIZE"
    log_info "Backup location: $backup_file_compressed"

    echo "$backup_file_compressed"
}

# Restore database from backup
restore_database() {
    local backup_file="$1"

    if [ ! -f "$backup_file" ]; then
        log_error "Backup file not found: $backup_file"
        exit 1
    fi

    log_warning "This will restore the database from: $backup_file"
    log_warning "Current database data will be OVERWRITTEN!"
    read -p "Are you sure you want to continue? (yes/no) " -r
    echo

    if [ "$REPLY" != "yes" ]; then
        log_info "Restore cancelled"
        exit 0
    fi

    log_info "Starting database restore..."

    # Decompress if needed
    local sql_file="$backup_file"
    if [[ "$backup_file" == *.gz ]]; then
        log_info "Decompressing backup..."
        sql_file="${backup_file%.gz}"
        gunzip -c "$backup_file" > "$sql_file"
    fi

    # Restore via Railway
    railway run psql "$DATABASE_URL" < "$sql_file" || {
        log_error "Database restore failed"
        exit 1
    }

    # Cleanup decompressed file if we created it
    if [[ "$backup_file" == *.gz ]]; then
        rm -f "$sql_file"
    fi

    log_success "Database restore completed"
}

# Clean old backups
clean_old_backups() {
    log_info "Cleaning backups older than $RETENTION_DAYS days..."

    local deleted_count=0

    # Find and delete old backups
    while IFS= read -r -d '' backup_file; do
        rm -f "$backup_file"
        deleted_count=$((deleted_count + 1))
        log_info "Deleted: $(basename "$backup_file")"
    done < <(find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +$RETENTION_DAYS -print0)

    if [ $deleted_count -eq 0 ]; then
        log_info "No old backups to clean"
    else
        log_success "Deleted $deleted_count old backup(s)"
    fi
}

# List backups
list_backups() {
    log_info "Available backups in $BACKUP_DIR:"
    echo ""

    if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR")" ]; then
        log_warning "No backups found"
        return
    fi

    # List backups with details
    ls -lh "$BACKUP_DIR"/backup_*.sql.gz 2>/dev/null | while read -r line; do
        echo "$line"
    done || log_warning "No backups found"
}

# Upload backup to cloud storage (optional)
upload_to_cloud() {
    local backup_file="$1"

    log_info "Cloud backup upload..."

    # Example: AWS S3 upload
    if command -v aws &> /dev/null && [ -n "${AWS_BACKUP_BUCKET:-}" ]; then
        log_info "Uploading to AWS S3: s3://$AWS_BACKUP_BUCKET/backups/"
        aws s3 cp "$backup_file" "s3://$AWS_BACKUP_BUCKET/backups/" || {
            log_warning "S3 upload failed"
            return 1
        }
        log_success "Uploaded to S3"
    fi

    # Example: Google Cloud Storage upload
    if command -v gsutil &> /dev/null && [ -n "${GCS_BACKUP_BUCKET:-}" ]; then
        log_info "Uploading to Google Cloud Storage: gs://$GCS_BACKUP_BUCKET/backups/"
        gsutil cp "$backup_file" "gs://$GCS_BACKUP_BUCKET/backups/" || {
            log_warning "GCS upload failed"
            return 1
        }
        log_success "Uploaded to GCS"
    fi
}

# Main function
main() {
    log_info "Spanish Subjunctive Practice - Database Backup"
    log_info "=============================================="

    # Parse command
    local command="${1:-backup}"

    case "$command" in
        backup)
            create_backup_dir
            get_database_url
            BACKUP_FILE=$(backup_database)

            # Optional cloud upload
            if [ "${UPLOAD_TO_CLOUD:-false}" == "true" ]; then
                upload_to_cloud "$BACKUP_FILE"
            fi

            # Clean old backups
            clean_old_backups

            log_success "Backup process completed"
            ;;

        restore)
            if [ -z "${2:-}" ]; then
                log_error "Please specify backup file to restore"
                echo "Usage: $0 restore <backup_file>"
                list_backups
                exit 1
            fi

            get_database_url
            restore_database "$2"
            ;;

        list)
            list_backups
            ;;

        clean)
            clean_old_backups
            ;;

        *)
            log_error "Unknown command: $command"
            echo ""
            echo "Usage: $0 [command] [options]"
            echo ""
            echo "Commands:"
            echo "  backup              Create a new database backup (default)"
            echo "  restore <file>      Restore database from backup file"
            echo "  list                List all available backups"
            echo "  clean               Remove backups older than retention period"
            echo ""
            echo "Environment Variables:"
            echo "  BACKUP_DIR          Directory to store backups (default: ./backups)"
            echo "  RETENTION_DAYS      Days to keep backups (default: 30)"
            echo "  UPLOAD_TO_CLOUD     Enable cloud upload (default: false)"
            echo "  AWS_BACKUP_BUCKET   AWS S3 bucket for backups"
            echo "  GCS_BACKUP_BUCKET   Google Cloud Storage bucket for backups"
            echo ""
            echo "Examples:"
            echo "  $0 backup"
            echo "  $0 restore backups/backup_20250102_120000.sql.gz"
            echo "  $0 list"
            echo "  RETENTION_DAYS=7 $0 clean"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
