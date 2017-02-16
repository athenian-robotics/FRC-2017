#!/usr/bin/env python3

import json
import time
from logging import info

import blinkt
import cli_args as cli
from cli_args import setup_cli_args
from constants import MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import setup_logging

HOSTNAME = "paho.hostname"
PORT = "paho.port"


def on_connect(client, userdata, flags, rc):
    info("{0} connecting to {1}:{2}".format("Success" if rc == 0 else "Failure", userdata[HOSTNAME], userdata[PORT]))
    client.subscribe("roborio/status/floodlight")


def on_disconnect(client, userdata, rc):
    info("Disconnected with result code: {0}".format(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    info("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(client, userdata, msg):
    # Decode json object payload
    json_val = json.loads(bytes.decode(msg.payload))
    info("{0} : {1}".format(msg.topic, json_val))
    global color, duration, duty_cycle, intensity
    color = json_val["color"]
    duration = json_val["duration"]
    duty_cycle = json_val["duty_cycle"]
    intensity = json_val["intensity"]


def run_display():
    global color, duration, duty_cycle, intensity
    color = {"r": 127, "g": 0, "b": 0}
    duration = 0.5
    duty_cycle = 0.5
    intensity = 0.5
    while True:
        for n in range(8):
            blinkt.set_pixel(n, color["r"], color["g"], color["b"], intensity)
        blinkt.show()
        time.sleep(duration * duty_cycle)
        for n in range(8):
            blinkt.set_pixel(n, 0, 0, 0, intensity)
        blinkt.show()
        time.sleep(duration * (1 - duty_cycle))


if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               userdata={},
                               on_connect=on_connect,
                               on_disconnect=on_disconnect,
                               on_subscribe=on_subscribe,
                               on_message=on_message)
    mqtt_conn.connect()

    try:
        run_display()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    print("Exiting...")
