@echo off
REM Quick Start Script for Phase II Todo Application
REM This script helps you get started quickly

echo ========================================
echo Phase II Todo App - Quick Start
echo ========================================
echo.

echo Step 1: Database Setup
echo -----------------------
echo IMPORTANT: You must complete this step first!
echo.
echo 1. Visit https://neon.tech and sign up (free)
echo 2. Create a new project named "todo-app"
echo 3. Copy your connection string
echo 4. Open backend\.env and replace DATABASE_URL with your connection string
echo 5. In Neon SQL Editor, run the script from backend\scripts\init_db.sql
echo.
echo Press any key when database is ready...
pause >nul

echo.
echo Step 2: Install Backend Dependencies
echo -------------------------------------
cd backend
echo Creating virtual environment...
uv venv
echo.
echo Activating virtual environment...
call .venv\Scripts\activate
echo.
echo Installing dependencies...
uv pip install -e ".[dev]"
echo.
echo Backend dependencies installed!
cd ..

echo.
echo Step 3: Install Frontend Dependencies
echo --------------------------------------
cd frontend
echo Installing npm packages...
call npm install
echo.
echo Frontend dependencies installed!
cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   .venv\Scripts\activate
echo   uvicorn src.main:app --reload --port 8000
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then visit: http://localhost:3000
echo.
echo Press any key to exit...
pause >nul
