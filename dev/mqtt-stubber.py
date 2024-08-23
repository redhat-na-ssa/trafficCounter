import paho.mqtt.client as mqtt
import json
import time
import random
import base64
import os

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_stub_data(image_path, plot_image_path):
    return {
        "frame": random.randint(1000, 9999),
        "second": round(random.uniform(0, 59), 1),
        "density": round(random.uniform(0.00, 0.04), 2),
        "image": get_base64_encoded_image(image_path),
        "plot": get_base64_encoded_image(plot_image_path)  # You can add a base64 encoded plot image here if needed
    }

# MQTT Configuration
MQTT_BROKER = "localhost"  # Change this to your MQTT broker address if different
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/density"

# Path to your sample image
IMAGE_PATH = "./latest_image.jpg"  # Update this path
PLOT_IMAGE_PATH="./latest_plot.png"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

try:
    while True:
        message = json.dumps(generate_stub_data(IMAGE_PATH, PLOT_IMAGE_PATH))
        client.publish(MQTT_TOPIC, message)
        print(f"Published message to {MQTT_TOPIC}")
        time.sleep(5)  # Publish every 5 seconds
except KeyboardInterrupt:
    print("Stopping the publisher")
finally:
    client.disconnect()