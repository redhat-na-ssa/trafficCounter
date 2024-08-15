FROM eclipse-mosquitto:2.0.14

# Copy custom Mosquitto configuration
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Expose the default MQTT port
EXPOSE 1883

CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]

