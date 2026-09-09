import paho.mqtt.client as mqtt
import time
import json

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe("tesi/catania/scuole/#")
    print("Subscribed!")

def on_message(client, userdata, msg):
    print(f"MSG RECEIVED: {msg.topic} {msg.payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect("broker.hivemq.com", 1883, 60)
    print("Connected in try block")
except Exception as e:
    print("Error:", e)

client.loop_start()

time.sleep(5)
client.publish("tesi/catania/scuole/1/sensore_acqua_main", json.dumps({"valore": 55.5}))
print("Published test msg")

time.sleep(10)
client.loop_stop()
client.disconnect()
