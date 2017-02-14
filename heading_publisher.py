#!/usr/bin/env python3

import argparse
import logging
import time
from threading import Lock
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
publish_lock = Lock()


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
    Thread(target=background_publisher, args=(userdata, userdata["min_publish"])).start()


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: {0}".format(rc))


def on_publish(client, userdata, mid):
    logging.debug("Published value to {0} with message id {1}".format(userdata["topic"], mid))


# SerialReader calls this for every line read from Arduino
def fetch_data(val, userdata):
    global current_heading
    if "\t" in val:
        try:
            x_val = val.split("\t")
            heading = round(float(x_val[0].split(": ")[1]), 1)
            if heading != current_heading:
                current_heading = heading
                publish_heading(userdata["paho.client"], userdata["topic"], heading)
        except IndexError:
            pass


def background_publisher(userdata, min_publish_secs):
    global current_heading, last_publish_time, stopped
    client = userdata["paho.client"]
    topic = userdata["topic"]
    while not stopped:
        time.sleep(.5)
        elapsed_time = current_time_millis() - last_publish_time
        if elapsed_time > min_publish_secs * 1000 and current_heading != -1:
            publish_heading(client, topic, current_heading)


def publish_heading(client, topic, heading):
    global publish_lock, last_publish_time
    with publish_lock:
        client.publish(topic, payload=(str(heading).encode("utf-8")), qos=0)
        last_publish_time = current_time_millis()


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
