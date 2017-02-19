#!/usr/bin/env python3

import argparse
import logging
import sys

import cli_args as cli
from constants import MQTT_HOST, LOG_FILE, MQTT_TOPIC
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code: {0}".format(rc))
    # Subscribe to all broker messages
    global topic
    client.subscribe(topic)
    logger.info("Connected, subscribing to topic {0}".format(topic))
    print("Connected, subscribing to topic {0}".format(topic))


def on_message(client, userdata, msg):
    logger.info("{0} : {1}".format(msg.topic, msg.payload))
    print("{0} : {1}".format(msg.topic, msg.payload))


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser)
    cli.log_file(parser)
    cli.mqtt_topic(parser)
    args = vars(parser.parse_args())

    global topic
    topic = args[MQTT_TOPIC]

    # Setup logging
    setup_logging(filename=args[LOG_FILE],
                  format="%(asctime)s %(levelname)-6s %(message)s",
                  level=logging.DEBUG)

    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               on_connect=on_connect,
                               on_message=on_message)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    logger.info("Exiting...")
    print("Exiting...")
