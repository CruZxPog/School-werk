from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import random
import time
import json

load_dotenv()

USERNAME = "meowqtt"
PASSWORD = os.getenv("PASSWORD")
BROKER = os.getenv("IP")
PORT = int(os.getenv("MQTT_PORT"))

TOPICS = {
    "sensor/temperature": "temperature",
    "sensor/luchtvochtigheid": "luchtvochtigheid",
    "sensor/bodemvocht": "bodemvocht"
}

RANGES = {
    "temperature": (5, 35),
    "luchtvochtigheid": (40, 100),
    "bodemvocht": (10, 90)
}

client = mqtt.Client(protocol=mqtt.MQTTv5)
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)

print(f"Connected to {BROKER}:{PORT} as {USERNAME}")

try:
    while True:
        for topic, key in TOPICS.items():
            low, high = RANGES[key]
            value = round(random.uniform(low, high), 1)
            payload = json.dumps({key: value})
            client.publish(topic, payload)
            print(f"Sent {payload} → {topic}")
            time.sleep(2)  
        time.sleep(5) 
except KeyboardInterrupt:
    print("\nStopped.")
    client.disconnect()
