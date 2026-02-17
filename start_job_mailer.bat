@echo off
title Automated Job Notification System
echo.
echo 🤖 Starting Automated Job Notification System...
echo.

cd /d "%~dp0"

echo 📍 Current directory: %CD%
echo.

echo 🔍 Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo.
echo 🚀 Starting job mailer...
echo Press Ctrl+C to stop the system
echo.

python job_mailer.py

echo.
echo 📧 Job mailer stopped.
pause
