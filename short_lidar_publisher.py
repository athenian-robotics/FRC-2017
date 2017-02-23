#!/usr/bin/env python3

import argparse
import logging

import cli_args as cli
from constants import SERIAL_PORT, BAUD_RATE, MQTT_HOST, LOG_LEVEL, TOPIC, DEVICE_ID
from moving_average import MovingAverage
from mqtt_connection import MqttConnection, PAHO_CLIENT
from out_of_range_values import OutOfRangeValues
from serial_reader import SerialReader
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)

SERIAL_READER = "serial_reader"
MOVING_AVERAGE = "moving_average"
OOR_VALUES = "oor_values"
DEVICE = "device"
TOLERANCE_THRESH = 5
OUT_OF_RANGE = "-1".encode("utf-8")


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    serial_reader = userdata[SERIAL_READER]
    serial_reader.start(func=fetch_data,
                        userdata=userdata,
                        port=userdata[SERIAL_PORT],
                        baudrate=userdata[BAUD_RATE])


def fetch_data(mm_str, userdata):
    topic = userdata[TOPIC]
    client = userdata[PAHO_CLIENT]
    moving_avg = userdata[MOVING_AVERAGE]
    oor_values = userdata[OOR_VALUES]

    # Values sometimes get compacted together, take the later value if that happens since it's newer
    if "\r" in mm_str:
        mm_str = mm_str.split("\r")[1]

    mm = int(mm_str)

    if mm <= 155 or mm > 2000:
        # Filter out bad data
        oor_values.mark()
        if oor_values.is_out_of_range(1000):
            client.publish(topic, payload=OUT_OF_RANGE, qos=0)
            oor_values.clear()
    else:
        ## Deal with good data
        moving_avg.add(mm)
        avg = moving_avg.average()
        if not avg or abs(mm - avg) > TOLERANCE_THRESH:
            client.publish(topic, payload=str(mm).encode("utf-8"), qos=0)


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.device_id(parser),
    cli.serial_port(parser)
    cli.baud_rate(parser)
    parser.add_argument("-d", "--device", dest=DEVICE, required=True, help="Device ('left' or 'right'")
    cli.verbose(parser),
    args = vars(parser.parse_args())

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    serial_reader = SerialReader(debug=True)
    port = SerialReader.lookup_port(args[DEVICE_ID]) if args.get(DEVICE_ID) else args[SERIAL_PORT]

    mqtt_client = MqttConnection(hostname=args[MQTT_HOST],
                                 userdata={TOPIC: "lidar/{0}/mm".format(args[DEVICE]),
                                           SERIAL_PORT: port,
                                           BAUD_RATE: args[BAUD_RATE],
                                           SERIAL_READER: serial_reader,
                                           MOVING_AVERAGE: (MovingAverage(size=3)),
                                           OOR_VALUES: (OutOfRangeValues(size=10))},
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
