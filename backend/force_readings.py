import sys
import os
import time
import json
import paho.mqtt.client as mqtt

# Aggiungi il path principale
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Sensore

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

def force_readings():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Simulator_Force")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    db = SessionLocal()
    sensori = db.query(Sensore).all()
    
    for s in sensori:
        valore = 0.0
        if s.tipo == "Acqua":
            import random
            valore = random.uniform(3.0, 8.0)
            if s.is_main:
                valore = random.uniform(15.0, 25.0)
        elif s.tipo == "Pressione":
            import random
            valore = random.uniform(2.0, 2.5)
        elif s.tipo == "Torbidità":
            import random
            valore = random.uniform(0.1, 0.5)
        elif s.tipo == "Conducibilità":
            import random
            valore = random.uniform(300.0, 800.0)
            
        payload = {"valore": valore, "timestamp": time.time()}
        client.publish(s.topic_mqtt, json.dumps(payload))
        
    db.close()
    
    time.sleep(2)
    client.loop_stop()
    print("Letture inviate forzatamente per tutti i sensori!")

if __name__ == "__main__":
    force_readings()
