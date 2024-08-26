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

# Global variable to store the latest MQTT messages for each camera
latest_data = {}

# MQTT Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'mqtt-broker.trafficcounter.svc.cluster.local')
MQTT_PORT = 1883
MQTT_TOPIC = "traffic/density/#"  # Subscribe to all camera topics

# MQTT Client Setup
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    global latest_data
    topic_parts = msg.topic.split('/')
    camera_id = topic_parts[-1]  # Assuming topic format is traffic/density/{camera_id}
    message = msg.payload.decode()
    try:
        data = json.loads(message)
        if "image" in data and data["image"]:
            image_path = os.path.join("static/images", f"latest_image_{camera_id}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(data["image"]))
            data["image"] = f"/static/images/latest_image_{camera_id}.jpg?{os.path.getmtime(image_path)}"
        
        if "plot" in data and data["plot"]:
            plot_path = os.path.join("static/images", f"latest_plot_{camera_id}.png")
            with open(plot_path, "wb") as plot_file:
                plot_file.write(base64.b64decode(data["plot"]))
            data["plot"] = f"/static/images/latest_plot_{camera_id}.png?{os.path.getmtime(plot_path)}"
        
        latest_data[camera_id] = data
    except json.JSONDecodeError:
        print(f"Failed to decode JSON message for camera {camera_id}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/camera/{camera_id}", response_class=HTMLResponse)
async def read_camera(request: Request, camera_id: str):
    camera_data = latest_data.get("density", {})
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "camera_id": camera_id,
        "location": camera_data.get("location", "Unknown"),
        "frame": camera_data.get("frame", "N/A"),
        "second": camera_data.get("second", "N/A"),
        "density": camera_data.get("density", "N/A"),
        "image": camera_data.get("image", None),
        "plot": camera_data.get("plot", None)
    })

@app.get("/api/camera/{camera_id}/latest", response_class=JSONResponse)
async def get_latest_camera_data(camera_id: str):
    print(latest_data)
    return JSONResponse(content=latest_data.get("density", {})) #Using 0 here because I don't have multiple topics or cameras

@app.on_event("shutdown")
def shutdown_event():
    client.loop_stop()
