from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import paho.mqtt.client as mqtt
import json
import os
import base64

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
    "image": None,
    "plot": None
}

# MQTT Configuration
#MQTT_BROKER = "mqtt-broker.trafficcounter.svc.cluster.local"
MQTT_BROKER = "mqtt"
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

        if latest_data["image"]:
            image_path = os.path.join("static", "latest_image.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(latest_data["image"]))
            latest_data["image"] = f"/static/latest_image.jpg?{os.path.getmtime(image_path)}"

        if latest_data["plot"]:
            plot_path = os.path.join("static", "latest_plot.png")
            with open(plot_path, "wb") as plot_file:
                plot_file.write(base64.b64decode(latest_data["plot"]))
            latest_data["plot"] = f"/static/latest_plot.png?{os.path.getmtime(plot_path)}"

    except json.JSONDecodeError:
        print("Failed to decode JSON message")

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    print("Connected successfully")
except Exception as e:
    print(f"Connection failed: {e}")



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    global latest_data
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "frame": latest_data["frame"], 
        "second": latest_data["second"], 
        "density": latest_data["density"], 
        "image": latest_data["image"],
        "plot": latest_data["plot"]
    })

@app.get("/latest-message", response_class=JSONResponse)
async def get_latest_message():
    global latest_data
    return JSONResponse(content=latest_data)

@app.on_event("shutdown")
def shutdown_event():
    client.loop_stop()
