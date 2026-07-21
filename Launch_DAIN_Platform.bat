@echo off
title DAIN Platform Launcher
echo ===================================================
echo   Starting DAIN Platform Development Environment
echo ===================================================
echo.

:: 1. Launch FastAPI Backend
echo [1/2] Launching Backend Server (FastAPI on Port 8000)...
start "DAIN Backend - FastAPI" cmd /k "cd /d D:\dain_demo\backend && uvicorn app.main:app --reload --port 8000"

:: 2. Launch Next.js Frontend
echo [2/2] Launching Frontend Server (Next.js on Port 3000)...
start "DAIN Frontend - Next.js" cmd /k "cd /d D:\dain_demo\frontend && npm run dev"

echo.
echo ===================================================
echo   All servers launched!
echo   - Backend:  http://127.0.0.1:8000/health
echo   - API Docs: http://127.0.0.1:8000/docs
echo   - Frontend: http://127.0.0.1:3000
echo ===================================================
echo.
echo Press any key to exit this loader.
pause > nul
exit
