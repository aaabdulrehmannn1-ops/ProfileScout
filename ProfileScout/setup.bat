@echo off
REM ===========================================================================
REM  ProfileScout Setup Script for Windows
REM  Complete installation and dependency setup
REM ===========================================================================

setlocal enabledelayedexpansion

echo.
echo ===========================================================================
echo         ProfileScout - OSINT Reconnaissance Tool Setup
echo ===========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed or not in PATH
    echo.
    echo Please install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo [+] Python found:
python --version
echo.

REM Install dependencies
echo [*] Installing dependencies...
echo     Installing: requests...
pip install requests
if errorlevel 1 (
    echo [X] Failed to install requests
    pause
    exit /b 1
)

echo     Installing: colorama...
pip install colorama
if errorlevel 1 (
    echo [X] Failed to install colorama
    pause
    exit /b 1
)

echo.
echo [+] All dependencies installed successfully!
echo.

REM Verify installation
echo [*] Verifying installation...
python -c "import requests; print('[+] requests version: ' + requests.__version__)"
python -c "import colorama; print('[+] colorama version: ' + colorama.__version__)"

echo.
echo ===========================================================================
echo         Setup Complete! You're ready to run ProfileScout
echo ===========================================================================
echo.
echo Quick Start:
echo   python profilescout.py
echo.
echo For more information, see:
echo   README.md - Comprehensive documentation
echo   QUICKSTART.md - Quick start guide
echo   examples.py - Usage examples
echo.
pause
