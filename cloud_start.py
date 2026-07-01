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
        
        # Crea le tabelle in SQLite se non esistono (necessario per il simulatore in cloud)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scuole (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                indirizzo TEXT,
                numero_studenti INTEGER,
                codice_meccanografico TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scuola_id INTEGER,
                tipo TEXT,
                topic_mqtt TEXT,
                nome TEXT,
                is_main INTEGER,
                FOREIGN KEY (scuola_id) REFERENCES scuole (id)
            )
        ''')
        conn.commit()
        
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

def run_simulator(port):
    print("Attendiamo che il server web sia online (Polling locale) prima di avviare il simulatore...")
    import time
    import urllib.request
    
    server_pronto = False
    for _ in range(60): # Aspetta massimo 2 minuti (60 * 2s)
        try:
            req = urllib.request.urlopen(f"http://127.0.0.1:{port}/")
            if req.getcode() == 200:
                server_pronto = True
                break
        except Exception:
            pass
        time.sleep(2)
        
    if server_pronto:
        print("Server web online! Attendo altri 5 secondi per garantire la connessione MQTT...")
        time.sleep(5)
    else:
        print("Timeout attesa server web. Avvio comunque il simulatore.")
        
    import iot_simulator.simulator
    iot_simulator.simulator.start_simulation()

def keep_awake():
    import urllib.request
    import time
    url = "https://tesi-acquasmart.onrender.com/"
    while True:
        time.sleep(600) # Attendi 10 minuti
        try:
            req = urllib.request.urlopen(url)
            print(f"Keep-awake ping a {url}: Status {req.getcode()}")
        except Exception as e:
            print(f"Keep-awake ping fallito: {e}")

if __name__ == "__main__":
    populate_if_empty()
    
    port = int(os.environ.get("PORT", 10000))
    
    # Avvia il simulatore in un thread separato in background
    sim_thread = threading.Thread(target=run_simulator, args=(port,), daemon=True)
    sim_thread.start()
    
    # Avvia il keep-awake per impedire la sospensione su Render
    awake_thread = threading.Thread(target=keep_awake, daemon=True)
    awake_thread.start()
    
    # Avvia il server web FastAPI
    print(f"Avvio server Web sulla porta {port}...")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
