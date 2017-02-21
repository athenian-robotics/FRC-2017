#!/usr/bin/env python2

import logging
import time
from threading import Thread

import cli_args as cli
from cli_args import setup_cli_args
from constants import MQTT_HOST, LOG_LEVEL, GRPC_HOST, TOPIC, MQTT_TOPIC
from location_client import LocationClient
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.grpc_host, cli.mqtt_host, cli.mqtt_topic, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    # Start location reader
    locations = LocationClient(args[GRPC_HOST]).start()


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        logger.info("Connected to MQTT broker with result code: {0}".format(rc))
        Thread(target=publish_locations, args=(client, userdata)).start()


    def publish_locations(client, userdata):
        prev_value = -1
        while True:
            try:
                x_loc = locations.get_x()
                if x_loc is not None and abs(x_loc[0] - prev_value) > 1:
                    result, mid = client.publish("{0}/x".format(userdata[MQTT_TOPIC]),
                                                 payload="{0}:{1}".format(x_loc[0], x_loc[1]).encode('utf-8'))
                    prev_value = x_loc[0]

            except BaseException as e:
                logger.error("Failure in publish_locations() [e]".format(e), exc_info=True)
                time.sleep(1)


    # Setup MQTT client
    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               userdata={TOPIC: args[MQTT_TOPIC]},
                               on_connect=on_connect)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()
        locations.stop()

    logger.info("Exiting...")
