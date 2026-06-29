@echo off
echo ==================================================
echo       Chiusura dei Servizi - AcquaSmart
echo ==================================================
echo.

echo Chiusura del Backend (uvicorn) e Simulatore (python)...
taskkill /F /IM python.exe /T > NUL 2>&1

echo.
echo Tutti i processi Python relativi al progetto sono stati terminati.
pause
