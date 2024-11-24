import paho.mqtt.client as mqtt
import json
import os
import dotenv

dotenv.load_dotenv()

# MQTT broker details
BROKER = str(os.getenv('MQTT_BROKER'))
PORT = 8883
USERNAME = str(os.getenv('MQTT_USER'))
PASSWORD = str(os.getenv('MQTT_PASSWORD'))

def publish_to_mqtt(topic, payload):
    """
    Publish a payload to the specified MQTT topic.

    :param topic: MQTT topic as a string
    :param payload: Payload as a dictionary
    :raises Exception: If publishing to the MQTT broker fails
    """
    try:
        client = mqtt.Client()
        client.username_pw_set(USERNAME, PASSWORD)
        client.tls_set()  # Enable TLS for secure connection
        client.connect(BROKER, PORT)
        client.loop_start()

        # Convert payload to JSON string
        message = json.dumps(payload)
        result = client.publish(topic, message)

        # Check if the message was published successfully
        result.wait_for_publish()
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise Exception("Failed to publish message to MQTT broker")

        client.loop_stop()
    except Exception as e:
        raise Exception(f"Error in MQTT publishing: {str(e)}")
