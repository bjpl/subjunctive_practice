#!/bin/bash

# Start FastAPI Backend Server
# Spanish Subjunctive Practice Application

echo "Starting FastAPI Backend Server..."
echo "=================================="

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Install/upgrade requirements
echo "Installing requirements..."
pip install -r backend/requirements.txt --quiet

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please create .env file with required configuration."
    exit 1
fi

# Set Python path
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Start server
echo "Starting server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/api/docs"
echo "=================================="
echo ""

cd "$PROJECT_ROOT"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
