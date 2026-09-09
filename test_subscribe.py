import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, msg):
    print(f"Received from Render (maybe?): {msg.topic} {msg.payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Test_Agent_Sub")
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.subscribe("tesi/catania/scuole/#")
client.loop_start()

print("Listening for 15 seconds...")
time.sleep(15)
client.loop_stop()
client.disconnect()
print("Done listening.")
