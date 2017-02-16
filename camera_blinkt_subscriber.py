from logging import info

import cli_args as cli
from blinkt import set_pixel, set_all, show, set_clear_on_exit
from cli_args import CAMERA_NAME, LOG_LEVEL, MQTT_HOST
from cli_args import setup_cli_args
from mqtt_connection import MqttConnection
from utils import mqtt_broker_info
from utils import setup_logging
from utils import sleep

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
    args = setup_cli_args(cli.grpc_host, cli.mqtt_host, cli.camera_name)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

    # Determine MQTT server details
    mqtt_hostname, mqtt_port = mqtt_broker_info(args[MQTT_HOST])


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        info("Connected with result code: {0}".format(rc))
        client.subscribe("camera/{0}/status".format(userdata[CAMERA_NAME]))


    def on_disconnect(client, userdata, rc):
        info("Disconnected with result code: {0}".format(rc))


    def on_message(client, userdata, msg):
        if msg.payload == "out of range":
            set_red()
        if msg.payload == "left":
            left_blue()
        if msg.payload == "right":
            right_blue()
        if msg.payload == "in threshold":
            set_green()
        print("{0} {1}".format(msg.topic, msg.payload))


    # Setup MQTT client
    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               userdata={CAMERA_NAME: args[CAMERA_NAME]},
                               on_connect=on_connect,
                               on_disconnect=on_disconnect,
                               on_message=on_message)
    mqtt_conn.connect()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    print("Exiting...")