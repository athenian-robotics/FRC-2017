#!/usr/bin/env python3

import argparse
import logging
import socket

import paho.mqtt.client as paho
from utils import mqtt_broker_info
from utils import setup_logging


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {0}".format(rc))
    # Subscribe to all broker messages
    client.subscribe("#")


def on_disconnect(client, userdata, rc):
    print("Disconnected with result code: {0}".format(rc))


def on_message(client, userdata, msg):
    print("{0} : {1}".format(msg.topic, msg.payload))


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", default="mqtt-turtle.local", help="MQTT broker hostname [mqtt-turtle.local]")
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(args["loglevel"])

    # Determine MQTT broker details
    mqtt_hostname, mqtt_port = mqtt_broker_info(args["mqtt"])

    # Initialize MQTT client
    client = paho.Client()

    # Setup MQTT callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    try:
        # Connect to MQTT broker
        logging.info("Connecting to MQTT broker {0}:{1}...".format(mqtt_hostname, mqtt_port))
        client.connect(mqtt_hostname, port=mqtt_port, keepalive=60)
        client.loop_forever()
    except socket.error:
        logging.error("Cannot connect to MQTT broker {0}:{1}".format(mqtt_hostname, mqtt_port))
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()

    print("Exiting...")
