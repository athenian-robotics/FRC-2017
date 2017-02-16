import logging

import cli_args as cli
from blinkt import set_pixel, set_all, show, set_clear_on_exit
from cli_args import setup_cli_args
from constants import CAMERA_NAME, MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)

# blinkt functions
set_clear_on_exit(False)


# set all leds red
def set_red():
    set_all(255, 0, 0, 0.1)
    show()


# set all leds blue
def set_blue():
    set_all(0, 0, 255, 1)
    show()


# set left 4 leds blue
def left_blue():
    set_pixel(0, 0, 0, 255)
    set_pixel(1, 0, 0, 255)
    set_pixel(2, 0, 0, 255)
    set_pixel(3, 0, 0, 255)
    show()


# set left 4 leds blue
def right_blue():
    set_pixel(4, 0, 0, 255)
    set_pixel(5, 0, 0, 255)
    set_pixel(6, 0, 0, 255)
    set_pixel(7, 0, 0, 255)
    show()


# set all green
def set_green():
    set_all(0, 255, 0, 1)
    show()


if __name__ == "__main__":
    # Parse CLI args
    args = setup_cli_args(cli.grpc_host, cli.mqtt_host, cli.camera_name, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        logger.info("Connected with result code: {0}".format(rc))
        client.subscribe("{0}/#".format(userdata[CAMERA_NAME]))


    def on_message(client, userdata, msg):
        if msg.payload == "out of range":
            set_red()
        if msg.payload == "left":
            left_blue()
        if msg.payload == "right":
            right_blue()
        if msg.payload == "in threshold":
            set_green()
        logger.info("{0} {1}".format(msg.topic, msg.payload))


    # Setup MQTT client
    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               userdata={CAMERA_NAME: args[CAMERA_NAME]},
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
