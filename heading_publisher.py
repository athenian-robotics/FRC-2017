#!/usr/bin/env python3

import argparse
import logging
import time
from threading import Thread

import cli_args  as cli
from mqtt_connection import MqttConnection
from serial_reader import SerialReader
from utils import current_time_millis
from utils import setup_logging
from utils import sleep

current_heading = -1
last_publish_time = -1
stopped = False


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code: {0}".format(rc))
    global total_sum
    global total_count
    total_sum = 0
    total_count = 0
    serial_reader = userdata["serial_reader"]
    serial_reader.start(func=fetch_data,
                        userdata=userdata,
                        port=userdata["serial_port"],
                        baudrate=userdata["baud_rate"])
    Thread(target=background_publisher, args=(userdata,)).start()


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: {0}".format(rc))


def on_publish(client, userdata, mid):
    logging.debug("Published value to {0} with message id {1}".format(userdata["topic"], mid))


def publish(userdata, heading):
    global last_publish_time

    topic = userdata["topic"]
    client = userdata["paho.client"]

    client.publish(topic, payload=(str(heading).encode("utf-8")), qos=0)
    last_publish_time = current_time_millis()


def fetch_data(val, userdata):
    global current_heading

    if "\t" not in val:
        return

    try:
        x_val = val.split("\t")
        heading = round(float(x_val[0].split(": ")[1]), 1)
    except IndexError:
        return

    if heading == current_heading:
        return

    current_heading = heading
    publish(userdata, heading)


def background_publisher(userdata):
    global current_heading, last_publish_time, stopped
    min_publish = userdata["min_publish"]
    while not stopped:
        time.sleep(.5)
        now = current_time_millis()
        elapsed_time = abs(now - last_publish_time)
        if elapsed_time > min_publish * 1000 and current_heading != -1:
            publish(userdata, current_heading)


if __name__ == "__main__":

    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.serial_port(parser)
    cli.baud_rate(parser)
    parser.add_argument("--minimum", dest="min_publish", default=5, type=int,
                        help="Minimum publishing time secs [5]")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args["loglevel"])

    serial_reader = SerialReader()

    mqtt_client = MqttConnection(hostname=(args["mqtt_host"]),
                                 userdata={"topic": "heading/degrees",
                                           "serial_port": args["serial_port"],
                                           "baud_rate": args["baud_rate"],
                                           "serial_reader": serial_reader,
                                           "min_publish": args["min_publish"]},
                                 on_connect=on_connect,
                                 on_disconnect=on_disconnect,
                                 on_publish=on_publish)
    mqtt_client.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        stopped = True
        mqtt_client.disconnect()
        serial_reader.stop()

    print("Exiting...")
