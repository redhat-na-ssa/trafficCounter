
# TrafficCounter

TrafficCounter is a project that monitors and processes traffic data, providing insights and analytics on traffic patterns. It includes components for data collection, processing, and visualization.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

The TrafficCounter project is designed to help monitor traffic data using a modular and scalable architecture. The system can collect data from various sources, process it in real-time, and visualize the results through dashboards or other analytics tools.

## Features

- **Data Collection**: Supports multiple data sources for collecting traffic data.
- **Real-Time Processing**: Processes data in real-time to provide immediate insights.
- **Visualization**: Integrates with visualization tools to present traffic data in an intuitive manner.
- **Scalability**: Designed to handle large volumes of data.

## Prerequisites

Before installing and running TrafficCounter, ensure you have the following prerequisites:

- Python 3.8+
- Docker (optional for containerized deployment)
- Node.js and npm (optional for frontend development)
- MQTT broker (for real-time data collection)

## Installation

### Clone the Repository

To get started, clone this repository to your local machine:

\`\`\`bash
git clone https://github.com/redhat-na-ssa/trafficCounter.git
cd trafficCounter
\`\`\`

### Set Up the Environment

1. **Create a Python virtual environment:**

    \`\`\`bash
    python3 -m venv venv
    source venv/bin/activate
    \`\`\`

2. **Install the required Python packages:**

    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

### Set Up the MQTT Broker

If you're using an MQTT broker for real-time data collection, ensure it's configured correctly and that the necessary topics are subscribed to within the application.

## Usage

### Running the Application

To run the TrafficCounter application, execute the following command:

\`\`\`bash
python app.py
\`\`\`

If you're using Docker, you can build and run the application with:

\`\`\`bash
docker build -t traffic-counter .
docker run -p 8000:8000 traffic-counter
\`\`\`

### Accessing the Dashboard

Once the application is running, you can access the dashboard via a web browser:

\`\`\`bash
http://localhost:8000
\`\`\`

### Monitoring Data

The application will start collecting and processing traffic data. You can view the processed data and insights on the dashboard.

## Configuration

### Environment Variables

TrafficCounter uses several environment variables for configuration. You can set these in your environment or in a \`.env\` file:

- \`MQTT_BROKER\`: The address of the MQTT broker.
- \`MQTT_PORT\`: The port of the MQTT broker.
- \`MQTT_TOPIC\`: The topic to subscribe to for receiving traffic data.

### Custom Configuration

You can customize the application's behavior by modifying the \`config.py\` file, which includes settings for data processing, logging, and other options.

## Deployment

### Deploying to OpenShift

To deploy TrafficCounter to OpenShift, follow these steps:

1. **Build and Push the Docker Image:**

    \`\`\`bash
    docker build -t your-dockerhub-username/traffic-counter .
    docker push your-dockerhub-username/traffic-counter
    \`\`\`

2. **Deploy to OpenShift:**

    \`\`\`bash
    oc new-app your-dockerhub-username/traffic-counter --name=traffic-counter
    oc expose svc/traffic-counter
    \`\`\`

3. **Access the Application:**

    Once deployed, access the application using the route provided by OpenShift:

    \`\`\`bash
    oc get route
    \`\`\`

## Contributing

We welcome contributions from the community! To contribute to TrafficCounter:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

Please make sure to follow the Contributor's Guide and ensure all tests pass before submitting your PR.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

