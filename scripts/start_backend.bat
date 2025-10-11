@echo off
REM Start FastAPI Backend Server
REM Spanish Subjunctive Practice Application

echo Starting FastAPI Backend Server...
echo ==================================

REM Get script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM Change to project root
cd /d "%PROJECT_ROOT%"

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/upgrade requirements
echo Installing requirements...
pip install -r backend\requirements.txt --quiet

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create .env file with required configuration.
    exit /b 1
)

REM Set Python path
set PYTHONPATH=%PROJECT_ROOT%;%PYTHONPATH%

REM Start server
echo Starting server on http://localhost:8000
echo API Documentation: http://localhost:8000/api/docs
echo ==================================
echo.

cd /d "%PROJECT_ROOT%"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
