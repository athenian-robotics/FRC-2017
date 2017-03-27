import argparse
import datetime
import logging

import cli_args as cli
from constants import MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import setup_logging, waitForKeyboardInterrupt

DIR = "dir"
LOG = "log"

logger = logging.getLogger(__name__)

topics = ["logging/camera/gear/alignment",
          "logging/lidar/gear/distance",
          "logging/lidar/long/distance",
          "logging/heading/degrees"]


def on_connect(client, userdata, flags, rc):
    global topics
    logger.info("Connected with result code: {0}".format(rc))

    for topic in topics:
        client.subscribe(topic)


def on_message(client, userdata, msg):
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    logger.info("{0} : {1}".format(msg.topic, val))


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser)
    parser.add_argument("-d", "--dir", dest=DIR, required=True, help="Log directory")
    cli.verbose(parser)
    args = vars(parser.parse_args())

    # Setup logging
    filename = "{0}/robot-{1}.log".format(args[DIR], datetime.datetime.now().strftime("%a-%b-%d-%Y-%H-%M-%S"))
    print("Writing log data to {0}".format(filename))
    setup_logging(filename=filename, level=args[LOG_LEVEL])

    # Setup MQTT client
    with MqttConnection(args[MQTT_HOST],
                        userdata={},
                        on_connect=on_connect,
                        on_message=on_message):
        waitForKeyboardInterrupt()

    logger.info("Exiting...")
