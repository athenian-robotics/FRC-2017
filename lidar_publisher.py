#!/usr/bin/env python3

import argparse
import logging

import cli_args  as cli
from mqtt_connection import MqttConnection
from serial_reader import SerialReader
from utils import setup_logging
from utils import sleep

global total_sum
global total_count

TOLERANCE_THRESH = 5


def on_connect(client, userdata, flags, rc):
    global total_sum
    global total_count
    logging.info("Connected with result code: {0}".format(rc))
    total_sum = 0
    total_count = 0
    serial_reader = userdata["serial_reader"]
    serial_reader.start(func=fetch_data,
                        userdata=userdata,
                        port=userdata["serial_port"],
                        baudrate=userdata["baud_rate"])


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: {0}".format(rc))


def on_publish(client, userdata, mid):
    logging.debug("Published value to {0} with message id {1}".format(userdata["topic"], mid))


OUT_OF_RANGE = "-1".encode("utf-8")


def fetch_data(mm_str, userdata):
    # Using globals to keep running averages in check
    global total_count
    global total_sum

    topic = userdata["topic"]
    client = userdata["paho.client"]

    # Values sometimes get compacted together, take the later value if that happens since it's newer
    if "\r" in mm_str:
        mm_str = mm_str.split("\r")[1]

    mm = int(mm_str)

    if mm < 0 or mm > 2000:  # out of range, get fresh data so it doesn't mess with averages
        total_sum = 0
        total_count = 0
        client.publish(topic, payload=OUT_OF_RANGE, qos=0)
    elif (total_sum + total_count == 0) or abs((total_sum / total_count) - mm) < TOLERANCE_THRESH:
        total_sum += mm
        total_count += 1
    else:
        client.publish(topic, payload=str(mm).encode("utf-8"), qos=0)
        total_sum = 0 + mm
        total_count = 1


if __name__ == "__main__":

    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.serial_port(parser)
    cli.baud_rate(parser)
    parser.add_argument("-d", "--device", required=True, help="Device ('left' or 'right'")
    parser.add_argument("-p", "--pid", help="USB device PID.")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args["loglevel"])
    port = SerialReader.lookup_port(args["pid"]) if args.get("pid") else args["serial_port"]

    serial_reader = SerialReader()

    mqtt_client = MqttConnection(hostname=(args["mqtt_host"]),
                                 userdata={"topic": "lidar/{0}/mm".format(args["device"]),
                                           "serial_port": port,
                                           "baud_rate": args["baud_rate"],
                                           "serial_reader": serial_reader},
                                 on_connect=on_connect,
                                 on_disconnect=on_disconnect,
                                 on_publish=on_publish)
    mqtt_client.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.disconnect()
        serial_reader.stop()

    print("Exiting...")
