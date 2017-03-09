import argparse
import logging
import time
from threading import Thread

import cli_args as cli
from constants import MQTT_HOST
from mqtt_connection import MqttConnection

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    Thread(target=enable_disable, args=(client,)).start()


def enable_disable(client):
    while True:
        client.publish("lidar/#/command", payload="OFF", qos=0)
        time.sleep(3)
        client.publish("lidar/#/command", payload="ON", qos=0)
        time.sleep(3)


if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser),
    cli.verbose(parser),
    args = vars(parser.parse_args())

    mqtt_client = MqttConnection(hostname=args[MQTT_HOST],
                                 userdata={},
                                 on_connect=on_connect)
    mqtt_client.connect()
