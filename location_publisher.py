#!/usr/bin/env python2

import logging
import time
import traceback
from logging import info
from threading import Thread

import cli_args as cli
from cli_args import setup_cli_args
from constants import CAMERA_NAME
from location_client import LocationClient
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.grpc_host, cli.mqtt_host, cli.camera_name, cli.verbose)

    # Setup logging
    setup_logging(level=args["loglevel"])

    # Start location reader
    locations = LocationClient(args["grpc_host"]).start()


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        info("Connected to MQTT broker with result code: {0}".format(rc))
        Thread(target=publish_locations, args=(client, userdata)).start()


    def on_disconnect(client, userdata, rc):
        info("Disconnected from MQTT broker with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        info("Published message id: {0}".format(mid))


    def publish_locations(client, userdata):
        prev_value = -1
        while True:
            try:
                x_loc = locations.get_x()
                if x_loc is not None and abs(x_loc[0] - prev_value) > 1:
                    result, mid = client.publish("{0}/x".format(userdata[CAMERA_NAME]),
                                                 payload="{0}:{1}".format(x_loc[0], x_loc[1]).encode('utf-8'))
                    prev_value = x_loc[0]

            except BaseException as e:
                logging.error("Failure in publish_locations() [e]".format(e))
                traceback.print_exc()
                time.sleep(1)


    # Setup MQTT client
    mqtt_conn = MqttConnection(args["mqtt_host"],
                               userdata={CAMERA_NAME: args["camera_name"]},
                               on_connect=on_connect,
                               on_disconnect=on_disconnect,
                               on_publish=on_publish)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()
        locations.stop()

    print("Exiting...")
