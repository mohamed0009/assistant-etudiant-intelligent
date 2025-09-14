@echo off
echo ========================================
echo   Assistant Etudiant Intelligent
echo   Installation automatique
echo ========================================
echo.

echo [1/4] Verification de Python...
python --version
if %errorlevel% neq 0 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo.
echo [2/4] Installation des dependances...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERREUR: Echec de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo [3/4] Test du systeme...
python test_system.py
if %errorlevel% neq 0 (
    echo ATTENTION: Certains tests ont echoue, mais l'installation peut continuer
)

echo.
echo [4/4] Installation terminee !
echo.
echo Pour lancer l'application:
echo   streamlit run app.py
echo.
echo Pour tester le systeme:
echo   python test_system.py
echo.
echo N'oubliez pas d'ajouter vos documents PDF/Word dans le dossier data/
echo.
pause
