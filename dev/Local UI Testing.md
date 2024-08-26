# Running the Dashboard Application Locally

This guide will walk you through the process of setting up and running the dashboard application on your local machine.

## Prerequisites

- Podman installed on your system
- Python installed (for running the stubber application)
- Access to the project files and containers

## Steps

### 1. Create a Podman Network

First, create a Podman network named `container-net`:

```bash
podman network create container-net
```

### 2. Start the MQTT Container

Start the MQTT container using the following command:

```bash
podman run -it --rm -d --name mqtt --network container-net -p 1883:1883 -p 9001:9001 -v /dev/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

This command:
- Creates a container named `mqtt`
- Connects it to the `container-net` network
- Maps ports 1883 and 9001
- Mounts the `mosquitto.conf` file from your local machine to the container

### 3. Add Stub Data to MQTT Queue

Run the stubber application to add test data to your MQTT queue:

```bash
python ./dev/mqtt-stubber.py
```

### 4. Build the Dashboard Container

Navigate to the `./images/dashboard` folder and build the dashboard container:

```bash
cd ./images/dashboard
podman build -t dashboard:v0.1 .
```

This creates a container image tagged as `dashboard:v0.1`.

### 5. Run the Dashboard Application

Start the dashboard application with the following command:

```bash
podman run --rm --name dashboard --network container-net -p 8080:8000 -e MQTT_BROKER=mqtt dashboard:v0.1
```

This command:
- Creates a container named `dashboard`
- Connects it to the `container-net` network
- Maps port 8080 on your local machine to port 8000 in the container
- Sets the MQTT_BROKER environment variable to 'mqtt', which is the name of the MQTT container in the network

## Accessing the Dashboard

Once all steps are completed, you can access the dashboard application by opening a web browser and navigating to:

```
http://localhost:8080
```

## Troubleshooting

If you encounter any issues:
- Ensure all required ports are available on your local machine
- Check that the `mosquitto.conf` file path is correct
- Verify that all containers are running and connected to the `container-net` network
- Make sure the MQTT_BROKER environment variable is correctly set to 'mqtt'

For further assistance, please contact the development team.