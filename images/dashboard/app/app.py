from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import paho.mqtt.client as mqtt
import asyncio

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Global variable to store the latest MQTT message
latest_message = ""

# MQTT Configuration
MQTT_BROKER = "broker.hivemq.com"  # Use your MQTT broker
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/los"

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_message
    latest_message = msg.payload.decode()
    # Trigger WebSocket update here if needed

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    global latest_message
    return templates.TemplateResponse("dashboard.html", {"request": request, "message": latest_message})

@app.get("/latest-message", response_class=HTMLResponse)
async def get_latest_message():
    global latest_message
    return latest_message

@app.on_event("shutdown")
def shutdown_event():
    client.loop_stop()

