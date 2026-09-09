import paho.mqtt.client as mqtt
import time
import json

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Test_Agent_Publisher")
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start()

payload = {
    "valore": 55.5,
    "timestamp": time.time(),
    "is_ground_truth_anomaly": False,
    "ground_truth_type": None
}

client.publish("tesi/catania/scuole/1/sensore_acqua_main", json.dumps(payload))
print("Payload published!")
time.sleep(2)
client.loop_stop()
client.disconnect()
