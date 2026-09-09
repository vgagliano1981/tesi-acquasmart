import paho.mqtt.client as mqtt
import time
import sys

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to EMQX")
    client.subscribe("tesi/catania/scuole/#")
    print("Subscribed!")

def on_message(client, userdata, msg):
    print(f"RECEIVED FROM RENDER: {msg.topic} {msg.payload}")
    sys.stdout.flush()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Test_EMQX_Sub")
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.emqx.io", 1883, 60)
client.loop_start()

print("Listening for 100 seconds...")
time.sleep(100)
client.loop_stop()
client.disconnect()
print("Done listening.")
