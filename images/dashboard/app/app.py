from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import paho.mqtt.client as mqtt
import json
import asyncio

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variable to store the latest MQTT message
latest_data = {
    "frame": None,
    "second": None,
    "density": None,
    "image": None
}

# MQTT Configuration
MQTT_BROKER = "mqtt-broker.trafficcounter.svc.cluster.local"  # Use your MQTT broker
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/density"

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_data
    message = msg.payload.decode()
    try:
        latest_data = json.loads(message)
    except json.JSONDecodeError:
        print("Failed to decode JSON message")

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    global latest_data
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "frame": latest_data["frame"], 
        "second": latest_data["second"], 
        "density": latest_data["density"], 
        "image": latest_data["image"]
    })

@app.get("/latest-message", response_class=HTMLResponse)
async def get_latest_message():
    global latest_data
    return latest_data

@app.on_event("shutdown")
def shutdown_event():
    client.loop_stop()
