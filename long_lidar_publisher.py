#!/usr/bin/env python3

import argparse
import logging

import cli_args as cli
from constants import SERIAL_PORT, BAUD_RATE, MQTT_HOST, LOG_LEVEL, TOPIC
from mqtt_connection import MqttConnection, PAHO_CLIENT
from serial_reader import SerialReader
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)

SERIAL_READER = "serial_reader"
PID = "pid"
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


def on_publish(client, userdata, mid):
    logger.debug("Published value to {0} with message id {1}".format(userdata[TOPIC], mid))


def fetch_data(cm_str, userdata):
    topic = userdata[TOPIC]
    client = userdata[PAHO_CLIENT]

    cm = int(cm_str)
    client.publish(topic, payload=str(cm).encode("utf-8"), qos=0)


if __name__ == "__main__":

    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.serial_port(parser)
    cli.baud_rate(parser)
    parser.add_argument("-d", "--device", dest=DEVICE, required=True, help="Device ('front' or 'rear'")
    parser.add_argument("-p", "--pid", dest=PID, help="USB device PID.")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])
    port = SerialReader.lookup_port(args[PID]) if args.get(PID) else args[SERIAL_PORT]

    serial_reader = SerialReader()

    mqtt_client = MqttConnection(hostname=args[MQTT_HOST],
                                 userdata={TOPIC: "lidar/{0}/cm".format(args[DEVICE]),
                                           SERIAL_PORT: port,
                                           BAUD_RATE: args[BAUD_RATE],
                                           SERIAL_READER: serial_reader},
                                 on_connect=on_connect,
                                 on_publish=on_publish)
    mqtt_client.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.disconnect()
        serial_reader.stop()

    logger.info("Exiting...")
