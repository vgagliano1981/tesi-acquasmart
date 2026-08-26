import paho.mqtt.client as mqtt
import json
from .database import SessionLocal
from .models import Sensore, Lettura, Scuola
from .ml_module import detector
from datetime import datetime

MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "tesi/catania/scuole/#"

last_debug_info = {"msg": None, "error": None, "connected": False}

def on_connect(client, userdata, flags, rc, properties=None):
    global last_debug_info
    last_debug_info["connected"] = True
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global last_debug_info
    last_debug_info["msg"] = msg.topic
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        valore = payload.get("valore", 0.0)
        is_gt_anomaly = payload.get("is_ground_truth_anomaly", False)
        gt_type = payload.get("ground_truth_type", None)
        
        # Save to DB
        db = SessionLocal()
        try:
            # Trova il sensore o crealo
            sensore = db.query(Sensore).filter(Sensore.topic_mqtt == topic).first()
            if not sensore:
                # Estrai dinamicamente l'ID della scuola dal topic (es. tesi/catania/scuole/2/...)
                scuola_id_estratto = 1
                tipo_sensore = "Acqua"
                try:
                    parti = topic.split("/")
                    if len(parti) > 3 and parti[2] == "scuole":
                        scuola_id_estratto = int(parti[3])
                    
                    ultimo = parti[-1].lower()
                    if "pressione" in ultimo:
                        tipo_sensore = "Pressione"
                    elif "torbidita" in ultimo:
                        tipo_sensore = "Torbidità"
                    elif "conducibilita" in ultimo:
                        tipo_sensore = "Conducibilità"
                except Exception:
                    pass
                
                sensore = Sensore(scuola_id=scuola_id_estratto, tipo=tipo_sensore, topic_mqtt=topic)
                db.add(sensore)
                db.commit()
                db.refresh(sensore)
                
            now = datetime.now()
            
            # Analyze Anomaly based on sensor type
            if sensore.tipo == "Pressione":
                is_anomalia = bool(valore < 1.5 or valore > 3.0)
                score = 1.0 if is_anomalia else 0.0
            elif sensore.tipo == "Torbidità":
                is_anomalia = bool(valore > 1.0)
                score = 1.0 if is_anomalia else 0.0
            elif sensore.tipo == "Conducibilità":
                is_anomalia = bool(valore > 2500)
                score = 1.0 if is_anomalia else 0.0
            else:
                # Per l'acqua usiamo il machine learning
                is_anomalia, score = detector.predict(valore, now)
                is_anomalia = bool(is_anomalia)
                score = float(score)
                
            lettura = Lettura(
                sensore_id=sensore.id,
                timestamp=now,
                valore_litri=valore,
                is_anomalia=is_anomalia,
                anomaly_score=score,
                is_ground_truth_anomaly=is_gt_anomaly,
                ground_truth_type=gt_type
            )
            db.add(lettura)
            db.commit()
            last_debug_info["error"] = "No error (Success)"
            
            # Simulated Email Sending
            if is_anomalia:
                scuola_nome = "Sconosciuta"
                scuola = db.query(Scuola).filter(Scuola.id == sensore.scuola_id).first()
                if scuola:
                    scuola_nome = scuola.nome
                print("\n" + "="*50)
                print("🔔 ALLARME ANOMALIA RILEVATA!")
                print(f"Scuola: {scuola_nome}")
                print(f"Sensore: {sensore.nome} ({sensore.tipo})")
                if sensore.tipo == "Pressione":
                    print(f"Valore Pressione: {valore:.2f} bar (Fuori limite 1.5 - 3.0 bar)")
                elif sensore.tipo == "Torbidità":
                    print(f"Valore Torbidità: {valore:.2f} NTU (Fuori limite > 1.0 NTU)")
                elif sensore.tipo == "Conducibilità":
                    print(f"Valore Conducibilità: {valore:.2f} µS/cm (Fuori limite > 2500 µS/cm)")
                else:
                    print(f"Consumo: {valore:.2f} L/min")
                print("📧 INVIO EMAIL DI NOTIFICA SIMULATO A: vitogagliano@gmail.com")
                print("="*50 + "\n")
                
        finally:
            db.close()
        
        print(f"Received {valore} on {topic} -> Anomaly: {is_anomalia}")
    except Exception as e:
        last_debug_info["error"] = str(e)
        print(f"Error processing MQTT message: {e}")

# Maintain global client reference
mqtt_client_instance = None

def start_mqtt():
    global mqtt_client_instance
    mqtt_client_instance = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client_instance.on_connect = on_connect
    mqtt_client_instance.on_message = on_message
    
    import time
    while True:
        try:
            mqtt_client_instance.connect(MQTT_BROKER, MQTT_PORT, 60)
            print("Client MQTT FastAPI connesso con successo!")
            break
        except Exception as e:
            print(f"Errore connessione MQTT backend: {e}. Riprovo tra 5 secondi...")
            time.sleep(5)
            
    mqtt_client_instance.loop_start() # Run in background
