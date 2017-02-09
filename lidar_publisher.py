#!/usr/bin/env python3

import argparse
import logging

from mqtt_connection import MqttConnection
from serial_reader import SerialReader
from utils import mqtt_broker_info, sleep
from utils import setup_logging

global total_sum
global total_count


TOLERANCE_THRESH = 5

serial_reader = SerialReader()


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code: {0}".format(rc))
    global total_sum
    global total_count
    total_sum = 0
    total_count = 0
    serial_reader.start(fetch_data, userdata["port"])


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: {0}".format(rc))


def on_publish(client, userdata, mid):
    logging.debug("Published value to {0} with message id {1}".format(userdata["topic"], mid))


OUT_OF_RANGE = "-1".encode("utf-8")

def fetch_data(mm_str):
    # Using globals to keep running averages in check
    global total_count
    global total_sum
    global userdata

    TOPIC = "{}/mm".format(userdata["topic"])

    # Values sometimes get compacted together, take the later value if that happens since it's newer
    if "\r" in mm_str:
        mm_str = mm_str.split("\r")[1]

    mm = int(mm_str)

    if mm < 0 or mm > 2000:  # out of range, get fresh data so it doesn't mess with averages
        total_sum = 0
        total_count = 0
        client.publish(TOPIC, payload=OUT_OF_RANGE, qos=0)
    elif (total_sum + total_count == 0) or abs((total_sum / total_count) - mm) < TOLERANCE_THRESH:
        total_sum += mm
        total_count += 1
    else:
        client.publish(TOPIC, payload=str(mm).encode("utf-8"), qos=0)
        total_sum = 0 + mm
        total_count = 1



if __name__ == "__main__":

    global userdata
    global client

    # Parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mqtt", required=True, help="MQTT broker hostname")
    parser.add_argument("-s", "--serial", required=True, help="Serial port", default="/dev/ttyACM0")
    parser.add_argument("-d", "--device", required=True, help="Device ('left' or 'right'")
    args = vars(parser.parse_args())

    port = args["serial"]

    # Setup logging
    setup_logging()

    # Create userdata dictionary
    userdata = {"topic": "lidar/" + args["device"], "port": port}

    # Determine MQTT broker details
    hostname, port = mqtt_broker_info(args["mqtt"])

    mqtt_client = MqttConnection(hostname, port, userdata=userdata)
    mqtt_client.client.on_connect = on_connect
    mqtt_client.client.on_disconnect = on_disconnect
    mqtt_client.client.on_publish = on_publish
    mqtt_client.connect()

    client = mqtt_client.client
    userdata["client"] = client

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
        serial_reader.stop()

    print("Exiting...")
