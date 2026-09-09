import paho.mqtt.client as mqtt
import time
import json

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Test_Agent_Publisher_EMQX2")
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()

payload = {
    "valore": 2.5,
    "timestamp": time.time(),
    "is_ground_truth_anomaly": False,
    "ground_truth_type": None
}

client.publish("tesi/catania/scuole/1/pressione_2309", json.dumps(payload))
print("Payload pressione published to EMQX!")
time.sleep(2)
client.loop_stop()
client.disconnect()
