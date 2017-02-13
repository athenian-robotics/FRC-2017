#!/usr/bin/env python3

import argparse

import cli_args  as cli
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep


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
    cli.mqtt_host(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging()

    mqtt_conn = MqttConnection(args["mqtt_host"],
                               on_connect=on_connect,
                               on_disconnect=on_disconnect,
                               on_message=on_message)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    print("Exiting...")
