@echo off
echo ========================================
echo   Assistant Etudiant Intelligent
echo ========================================
echo.

echo [1/3] Demarrage du backend FastAPI...
start "Backend API" cmd /k "cd /d %~dp0 && python api.py"

echo [2/3] Attente du demarrage du backend...
timeout /t 5 /nobreak >nul

echo [3/3] Demarrage du frontend Next.js...
start "Frontend Next.js" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo.
echo ========================================
echo   Projet demarre avec succes !
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend:    http://localhost:3000
echo.
echo Appuyez sur une touche pour fermer...
pause >nul

