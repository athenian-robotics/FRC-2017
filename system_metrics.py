"""Track total message throughput over mqtt"""

import argparse
import logging
import time
from threading import Thread, Lock

import cli_args as cli
from constants import MQTT_HOST
from mqtt_connection import MqttConnection
from utils import sleep

messages = 0

lock = Lock()

logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    client.subscribe("#")
    Thread(target=average_publisher, args=(client,)).start()


def on_message(client, userdata, msg):
    global messages, lock
    with lock:
        messages += 1


def average_publisher(client):
    global messages, lock
    while True:
        try:
            time.sleep(1)
            payload = str(messages).encode("utf-8")
            client.publish("metrics/msg_rate", payload=payload, qos=0)
            client.publish("logging/metrics/msg_rate", payload=payload, qos=0)
            with lock:
                messages = 0
        except BaseException as e:
            logger.error("Failure in publish_locations() [e]".format(e), exc_info=True)
            time.sleep(1)

if __name__ == "__main__":
    # Parse CLI args
    parser = argparse.ArgumentParser()
    cli.mqtt_host(parser)
    args = vars(parser.parse_args())

    # Setup MQTT client
    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               userdata={},
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
