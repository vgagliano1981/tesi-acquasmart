import paho.mqtt.client as mqtt
import time
import json

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Test_Agent_Publisher_EMQX")
client.connect("broker.emqx.io", 1883, 60)
client.loop_start()

payload = {
    "valore": 99.9,
    "timestamp": time.time(),
    "is_ground_truth_anomaly": True,
    "ground_truth_type": "TestAgent"
}

client.publish("tesi/catania/scuole/1/sensore_acqua_main", json.dumps(payload))
print("Payload published to EMQX!")
time.sleep(2)
client.loop_stop()
client.disconnect()
