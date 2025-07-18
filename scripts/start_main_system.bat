@echo off
title Main Detection System
color 0C

echo ========================================
echo   📹 MAIN DETECTION SYSTEM
echo ========================================
echo.
echo 🚀 Starting camera detection and Telegram alerts...
echo.

echo 🎮 CONTROLS:
echo    [q] - Quit system
echo    [s] - Take manual photo  
echo    [r] - Reset background
echo    [m] - Test detection
echo.
echo 📱 TELEGRAM COMMANDS:
echo    /chup - Take remote photo
echo    /mo - Start monitoring
echo    /thoat - Stop monitoring
echo.
echo ⚡ Starting system in 3 seconds...
timeout /t 3 /nobreak >nul

python main_with_remote.py

echo.
echo 👋 Main system stopped.
pause
