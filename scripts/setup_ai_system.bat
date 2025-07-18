@echo off
echo ====================================
echo   AI INTRUSION DETECTION SYSTEM
echo   Setup and Installation Script
echo ====================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python found

echo.
echo [2/4] Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)
echo ✅ Packages installed

echo.
echo [3/4] Creating necessary directories...
if not exist "alert_images" mkdir alert_images
if not exist "__pycache__" mkdir __pycache__
echo ✅ Directories created

echo.
echo [4/4] Testing AI detection...
echo This will download YOLO model (~6MB) on first run...
echo.
python test_ai_integration.py
if errorlevel 1 (
    echo WARNING: AI test failed, but system can still run without AI
) else (
    echo ✅ AI detection working
)

echo.
echo ====================================
echo   INSTALLATION COMPLETE!
echo ====================================
echo.
echo Available commands:
echo   scripts\start_main_system.bat     - Start main system
echo   scripts\start_web_dashboard.bat   - Start web dashboard  
echo   scripts\start_complete_system.bat - Start everything
echo.
echo Controls in main system:
echo   Press 'a' - Toggle AI Detection
echo   Press '+'/'-' - Adjust motion threshold
echo   Press 'q' - Quit
echo.
echo For detailed documentation, see how_it_works\ folder
echo.
pause
