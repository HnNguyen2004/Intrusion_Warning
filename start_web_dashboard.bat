@echo off
title Web Dashboard
color 0B

echo ========================================
echo   🌐 WEB DASHBOARD SYSTEM  
echo ========================================
echo.
echo 🚀 Starting web management interface...
echo.

REM Cài đặt Flask dependencies
echo 📦 Installing Flask dependencies...
pip install flask flask-cors flask-restful

echo.
echo 🌐 DASHBOARD FEATURES:
echo    📊 Real-time statistics
echo    📋 Event management
echo    📷 Image gallery
echo    📈 Analytics charts
echo.
echo 🔗 ACCESS URLS:
echo    Web UI: http://localhost:5000/web
echo    API:    http://localhost:5000/
echo.
echo ⚡ Starting web server...

python web_api.py

echo.
echo 🛑 Web dashboard stopped.
pause
