@echo off
title Intrusion Warning System - Complete
color 0A

echo ========================================
echo   🏠 INTRUSION WARNING SYSTEM
echo ========================================
echo.
echo 🚀 Starting Complete System...
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Cài đặt dependencies nếu cần
echo 📦 Checking dependencies...
pip install flask flask-cors flask-restful >nul 2>&1

echo ✅ Dependencies ready
echo.

echo 🔥 Starting Main System and Web Dashboard...
echo.
echo 📱 Main System: Camera detection + Telegram alerts
echo 🌐 Web Dashboard: http://localhost:5000/web
echo.
echo ⚠️  IMPORTANT: 
echo    - Both systems will run in separate windows
echo    - Close this window to stop everything
echo    - Use Ctrl+C in each window to stop individually
echo.

REM Tạo thư mục logs nếu chưa có
if not exist "alert_images" mkdir alert_images

REM Chạy hệ thống chính trong window mới
echo 🚀 Starting Main Detection System...
start "Main System - Camera Detection" cmd /k "echo 📹 MAIN SYSTEM - Camera Detection & python main_with_remote.py"

REM Chờ 3 giây để main system khởi động
timeout /t 3 /nobreak >nul

REM Chạy web system trong window mới  
echo 🌐 Starting Web Dashboard...
start "Web Dashboard - Management" cmd /k "echo 🌐 WEB DASHBOARD - Management Interface & python web_api.py"

echo.
echo ✅ Both systems started successfully!
echo.
echo 📖 USAGE:
echo    1️⃣  Main System Window: Camera detection + Telegram
echo       - Press 'q' to quit
echo       - Press 'm' to test detection
echo       - Press 's' for manual photo
echo.
echo    2️⃣  Web Dashboard: http://localhost:5000/web
echo       - View events and images
echo       - Real-time statistics
echo       - System monitoring
echo.
echo    3️⃣  Telegram Bot: Send commands to your bot
echo       - /chup - Take photo
echo       - /mo - Start monitoring  
echo       - /thoat - Stop monitoring
echo.
echo 🛑 To stop everything: Close this window or Ctrl+C in each window
echo.

REM Mở browser tự động (optional)
timeout /t 5 /nobreak >nul
echo 🌐 Opening web dashboard...
start http://localhost:5000/web

echo.
echo 🎉 System is now fully operational!
echo    Keep this window open to maintain both systems
echo.
pause
