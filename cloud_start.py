import threading
import time
import uvicorn
import sqlite3
import os

from backend.database import engine
from backend import models

print("Creazione tabelle DB se non esistono...")
models.Base.metadata.create_all(bind=engine)

def populate_if_empty():
    try:
        conn = sqlite3.connect('iot_platform.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM scuole")
        if cursor.fetchone()[0] == 0:
            print("Database vuoto, avvio script di popolamento automatico...")
            # Importandoli, il loro codice globale verrà eseguito, popolando il db
            import backend.populate_db
            try:
                import backend.add_quality_sensors
            except ImportError:
                pass
            try:
                import backend.add_pressure_sensors
            except ImportError:
                pass
        else:
            print("Il database contiene già i dati.")
        conn.close()
    except Exception as e:
        print("Errore nel popolamento:", e)

def run_simulator():
    print("Avvio del simulatore in background...")
    import iot_simulator.simulator
    iot_simulator.simulator.start_simulation()

if __name__ == "__main__":
    populate_if_empty()
    
    # Avvia il simulatore in un thread separato in background
    sim_thread = threading.Thread(target=run_simulator, daemon=True)
    sim_thread.start()
    
    # Avvia il server web FastAPI
    port = int(os.environ.get("PORT", 10000))
    print(f"Avvio server Web sulla porta {port}...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
