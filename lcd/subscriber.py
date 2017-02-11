#!/usr/bin/env python

import argparse
from threading import Lock

import cli_args  as cli
from constants import TOPIC
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

val_lidar_front_left = None
val_lidar_front_right = None
val_camera_1 = None

LIDAR_FRONT_LEFT = "Lidar-Front-Left/data"
LIDAR_FRONT_RIGHT = "Lidar-Front-Right/data"
CAMERA_1 = "Camera-1/value"

lock = Lock()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {0}".format(rc))
    client.subscribe("Lidar-Front-Left/data")
    client.subscribe("Lidar-Front-Right/data")
    client.subscribe("Camera-1/value")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(client, userdata, msg):
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    print("{0} : {1}".format(msg.topic, val))
    if msg.topic == LIDAR_FRONT_LEFT:
        with lock:
            val_lidar_front_left = val

    elif msg.topic == LIDAR_FRONT_RIGHT:
        with lock:
            val_lidar_front_right = val

    elif msg.topic == CAMERA_1:
        with lock:
            val_camera_1 = val


            # If payload is an int byte array, use: int.from_bytes(msg.payload, byteorder="big"))
            # int.from_bytes() requires python3: https://docs.python.org/3/library/stdtypes.html#int.from_bytes


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    parser.add_argument("-t", "--topic", required=True, help="MQTT topic")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args["loglevel"])

    # Setup MQTT client
    mqtt_conn = MqttConnection(args["mqtt_host"],
                               userdata={TOPIC: args["topic"]},
                               on_connect=on_connect,
                               on_message=on_message)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    print("Exiting...")
