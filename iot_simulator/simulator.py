import paho.mqtt.client as mqtt
import time
import random
import json
import sqlite3
from collections import defaultdict

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

def get_scuole_sensori():
    try:
        conn = sqlite3.connect('iot_platform.db')
        cursor = conn.cursor()
        cursor.execute('SELECT scuola_id, topic_mqtt, is_main, nome, tipo FROM sensori')
        rows = cursor.fetchall()
        conn.close()
        
        scuole = defaultdict(list)
        for row in rows:
            scuole[row[0]].append({
                "topic": row[1],
                "is_main": bool(row[2]),
                "nome": row[3],
                "tipo": row[4]
            })
        return scuole
    except Exception as e:
        print(f"Errore lettura DB: {e}")
        return {}

def start_simulation():
    try:
        import ctypes
        # ES_CONTINUOUS = 0x80000000, ES_SYSTEM_REQUIRED = 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
        print("Sistema anti-sospensione attivato per il simulatore.")
    except Exception as e:
        print(f"Impossibile attivare l'anti-sospensione: {e}")

    while True:
        try:
            client_id = f"Simulator_Catania_Adv_{random.randint(100000, 999999)}"
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
            print("Connessione al broker MQTT in corso...")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            break
        except Exception as e:
            print(f"Errore connessione MQTT: {e}. Riprovo tra 10 secondi...")
            time.sleep(10)
            
    client.loop_start()
    
    print("Avvio simulazione invio dati per TUTTE le scuole (CTRL+C per fermare)")
    base_sub_consumption = 3.0 # litri al min per sotto-sensore
    
    while True:
        try:
            scuole = get_scuole_sensori()
            if not scuole:
                print("Nessun sensore trovato nel DB. Riprovo tra 5 secondi...")
                time.sleep(5)
                continue

            for scuola_id, sensori in scuole.items():
                water_sensors = [s for s in sensori if s["tipo"] == "Acqua"]
                pressure_sensors = [s for s in sensori if s["tipo"] == "Pressione"]
                turbidity_sensors = [s for s in sensori if s["tipo"] == "Torbidità"]
                conductivity_sensors = [s for s in sensori if s["tipo"] == "Conducibilità"]
                
                main_sensor = next((s for s in water_sensors if s["is_main"]), None)
                sub_sensors = [s for s in water_sensors if not s["is_main"]]
                
                sum_subs = 0.0
                
                # Generazione dati sotto-sensori
                for sub in sub_sensors:
                    valore = base_sub_consumption + random.uniform(-1.0, 1.0)
                    
                    # Anomalia Locale (2% prob)
                    if random.random() < 0.02:
                        valore = base_sub_consumption * random.uniform(3.0, 5.0)
                        print(f"!!! ANOMALIA LOCALE ({sub['nome']}): {valore:.2f} L/min !!!")
                    
                    sum_subs += valore
                    
                    payload = {"valore": round(valore, 2), "timestamp": time.time()}
                    client.publish(sub["topic"], json.dumps(payload))
                
                # Generazione Contatore Principale
                if main_sensor:
                    main_valore = sum_subs
                    
                    # Perdita Occulta nell'impianto generale (2% prob)
                    if random.random() < 0.02:
                        perdita = random.uniform(15.0, 30.0)
                        main_valore += perdita
                        print(f"!!! PERDITA OCCULTA RILEVATA (Scuola {scuola_id}): Mismatch di {perdita:.2f} L/min !!!")
                    
                    payload = {"valore": round(main_valore, 2), "timestamp": time.time()}
                    client.publish(main_sensor["topic"], json.dumps(payload))

                # Generazione sensori di Pressione
                for p_sensor in pressure_sensors:
                    # Normale tra 2.0 e 2.5 bar
                    p_valore = random.uniform(2.0, 2.5)
                    
                    # Anomalia di pressione (2% prob)
                    if random.random() < 0.02:
                        if random.random() < 0.5:
                            p_valore = random.uniform(0.5, 1.4) # Difetto
                        else:
                            p_valore = random.uniform(3.1, 4.5) # Esubero
                        print(f"!!! ANOMALIA PRESSIONE ({p_sensor['nome']}): {p_valore:.2f} bar !!!")
                        
                    payload = {"valore": round(p_valore, 2), "timestamp": time.time()}
                    client.publish(p_sensor["topic"], json.dumps(payload))

                # Generazione sensori di Torbidità
                for t_sensor in turbidity_sensors:
                    t_valore = random.uniform(0.1, 0.5)
                    if random.random() < 0.02:
                        t_valore = random.uniform(1.5, 5.0) # Anomalia > 1.0
                        print(f"!!! ANOMALIA TORBIDITA' ({t_sensor['nome']}): {t_valore:.2f} NTU !!!")
                    payload = {"valore": round(t_valore, 2), "timestamp": time.time()}
                    client.publish(t_sensor["topic"], json.dumps(payload))

                # Generazione sensori di Conducibilità
                for c_sensor in conductivity_sensors:
                    c_valore = random.uniform(300, 800)
                    if random.random() < 0.02:
                        c_valore = random.uniform(2600, 3000) # Anomalia > 2500
                        print(f"!!! ANOMALIA CONDUCIBILITA' ({c_sensor['nome']}): {c_valore:.2f} µS/cm !!!")
                    payload = {"valore": round(c_valore, 2), "timestamp": time.time()}
                    client.publish(c_sensor["topic"], json.dumps(payload))
            
            # Attende prima di un nuovo ciclo globale
            time.sleep(600)
        except Exception as e:
            print(f"Errore nel ciclo di simulazione: {e}")
            time.sleep(10)

if __name__ == "__main__":
    start_simulation()
