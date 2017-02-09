#!/usr/bin/env python3

import argparse

from mqtt_connection import MqttConnection
from utils import mqtt_broker_info, sleep
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
    setup_logging()

    # Determine MQTT broker details
    hostname, port = mqtt_broker_info(args["mqtt"])

    mqtt_conn = MqttConnection(hostname, port)
    mqtt_conn.client.on_connect = on_connect
    mqtt_conn.client.on_disconnect = on_disconnect
    mqtt_conn.client.on_message = on_message
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    print("Exiting...")
