#!/usr/bin/env python3

import argparse
import logging

import cli_args as cli
from constants import SERIAL_PORT, BAUD_RATE, MQTT_HOST, LOG_LEVEL, TOPIC, DEVICE_ID
from mqtt_connection import MqttConnection, PAHO_CLIENT
from serial_reader import SerialReader
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)

total_sum = 0
total_count = 0

SERIAL_READER = "serial_reader"
DEVICE = "device"
TOLERANCE_THRESH = 5
OUT_OF_RANGE = "-1".encode("utf-8")


def on_connect(client, userdata, flags, rc):
    global total_sum
    global total_count
    logger.info("Connected with result code: {0}".format(rc))
    total_sum = 0
    total_count = 0
    serial_reader = userdata[SERIAL_READER]
    serial_reader.start(func=fetch_data,
                        userdata=userdata,
                        port=userdata[SERIAL_PORT],
                        baudrate=userdata[BAUD_RATE])


def fetch_data(mm_str, userdata):
    # Using globals to keep running averages in check
    global total_count
    global total_sum

    topic = userdata[TOPIC]
    client = userdata[PAHO_CLIENT]

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
    parser.add_argument("-d", "--device", dest=DEVICE, required=True, help="Device ('left' or 'right'")
    cli.device_id(parser),
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])
    port = SerialReader.lookup_port(args[DEVICE_ID]) if args.get(DEVICE_ID) else args[SERIAL_PORT]

    serial_reader = SerialReader()

    mqtt_client = MqttConnection(hostname=args[MQTT_HOST],
                                 userdata={TOPIC: "lidar/{0}/mm".format(args[DEVICE]),
                                           SERIAL_PORT: port,
                                           BAUD_RATE: args[BAUD_RATE],
                                           SERIAL_READER: serial_reader},
                                 on_connect=on_connect)
    mqtt_client.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.disconnect()
        serial_reader.stop()

    logger.info("Exiting...")
