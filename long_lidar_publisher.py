#!/usr/bin/env python3

import argparse
import logging

import cli_args as cli
from constants import SERIAL_PORT, BAUD_RATE, MQTT_HOST, LOG_LEVEL, TOPIC, DEVICE_ID, OOR_SIZE, OOR_TIME
from moving_average import MovingAverage
from mqtt_connection import MqttConnection, PAHO_CLIENT
from out_of_range_values import OutOfRangeValues
from serial_reader import SerialReader
from utils import setup_logging
from utils import sleep

from short_lidar_publisher import OOR_VALUES

logger = logging.getLogger(__name__)

SERIAL_READER = "serial_reader"
MOVING_AVERAGE = "moving_average"
DEVICE = "device"
AVG_SIZE = "avg_size"
OUT_OF_RANGE = "-1".encode("utf-8")
TOLERANCE_THRESH = 2.5

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    serial_reader = userdata[SERIAL_READER]
    serial_reader.start(func=fetch_data,
                        userdata=userdata,
                        port=userdata[SERIAL_PORT],
                        baudrate=userdata[BAUD_RATE])


def fetch_data(cm_str, userdata):
    topic = userdata[TOPIC]
    client = userdata[PAHO_CLIENT]
    moving_avg = userdata[MOVING_AVERAGE]
    oor_values = userdata[OOR_VALUES]

    cm = int(cm_str)

    if cm <= 0:
        return

    moving_avg.add(cm)
    avg = moving_avg.average()

    # if abs(cm - avg) > TOLERANCE_THRESH:
    #    client.publish(topic, payload=str(cm).encode("utf-8"), qos=0)

    if len(moving_avg) == moving_avg.max_size():
        client.publish(topic, payload=str(int(avg)).encode("utf-8"), qos=0)
        moving_avg.clear()


if __name__ == "__main__":

    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.device_id(parser),
    cli.serial_port(parser)
    cli.baud_rate(parser)
    cli.oor_size(parser),
    cli.oor_time(parser),
    parser.add_argument("-d", "--device", dest=DEVICE, required=True, help="Device ('front' or 'rear'")
    parser.add_argument("--avg_size", dest=AVG_SIZE, default=10, type=int, help="Moving average size [10]")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])
    port = SerialReader.lookup_port(args[DEVICE_ID]) if args.get(DEVICE_ID) else args[SERIAL_PORT]

    serial_reader = SerialReader()

    mqtt_client = MqttConnection(hostname=args[MQTT_HOST],
                                 userdata={TOPIC: "lidar/{0}/cm".format(args[DEVICE]),
                                           SERIAL_PORT: port,
                                           BAUD_RATE: args[BAUD_RATE],
                                           SERIAL_READER: serial_reader,
                                           MOVING_AVERAGE: MovingAverage(args[AVG_SIZE]),
                                           OOR_VALUES: OutOfRangeValues(size=args[OOR_SIZE]),
                                           OOR_TIME: args[OOR_TIME]},
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
