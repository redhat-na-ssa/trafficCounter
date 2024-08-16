from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import paho.mqtt.client as mqtt
import asyncio
import json
import base64

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables to store the latest data
latest_image = ""
latest_frame = 0
latest_seconds = 0
latest_los = ""

# MQTT Configuration
MQTT_BROKER = "mqtt-broker.trafficcounter.svc.cluster.local"  # Use your MQTT broker
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/los"

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_image, latest_frame, latest_seconds, latest_los
    payload = json.loads(msg.payload.decode())
    if 'image' in payload:
        latest_image = "data:image/jpeg;base64," + base64.b64encode(payload['image'].encode('latin1')).decode('utf-8')
    latest_frame = payload.get('frame', 0)
    latest_seconds = payload.get('second', 0)
    latest_los = payload.get('los', '')

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    global latest_image, latest_frame, latest_seconds, latest_los
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "image": latest_image, 
        "frame": latest_frame,
        "seconds": latest_seconds,
        "los": latest_los
    })

@app.get("/latest-data", response_class=HTMLResponse)
async def get_latest_data():
    global latest_image, latest_frame, latest_seconds, latest_los
    return {
        "image": latest_image,
        "frame": latest_frame,
        "seconds": latest_seconds,
        "los": latest_los
    }

@app.on_event("shutdown")
def shutdown_event():
    client.loop_stop()
