@echo off
echo ==================================================
echo       Avvio dei Servizi - AcquaSmart
echo ==================================================
echo.

echo [1/2] Avvio del Backend Server (FastAPI su porta 8001)...
start "AcquaSmart - Backend" cmd /k ".\venv\Scripts\activate.bat && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8001"

timeout /t 3 /nobreak > NUL

echo [2/2] Avvio del Simulatore IoT (Sensori MQTT)...
start "AcquaSmart - Simulatore" cmd /k ".\venv\Scripts\activate.bat && python iot_simulator/simulator.py"

echo.
echo Tutti i servizi sono in esecuzione in finestre separate.
echo Puoi chiudere questa finestra.
pause
