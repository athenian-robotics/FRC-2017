#!/usr/bin/env python2

import signal
from threading import Lock

import cli_args  as cli
import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

val_lidar_front_left = None
val_lidar_front_right = None
val_camera_1 = None

selected_sensor = "camera"
lcd.clear()
lcd.set_cursor_position(0, 0)
lcd.write("Camera")
lcd.set_cursor_position(0, 2)
lcd.write("null")

LIDAR_FRONT_LEFT = "Lidar-Front-Left/data"
LIDAR_FRONT_RIGHT = "Lidar-Front-Right/data"
CAMERA_1 = "Camera-1/value"

lock = Lock()

lcd.clear()
backlight.rgb(255, 255, 255)
lcd.set_contrast(45)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: {0}".format(rc))
    client.subscribe("Lidar-Front-Left/data")
    client.subscribe("Lidar-Front-Right/data")
    client.subscribe("Camera-1/value")


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with message id: {0} QOS: {1}".format(mid, granted_qos))


def on_message(client, userdata, msg):
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    print("{0} : {1}".format(msg.topic, val))
    if msg.topic == LIDAR_FRONT_LEFT:
        with lock:
            val_lidar_front_left = val

    elif msg.topic == LIDAR_FRONT_RIGHT:
        with lock:
            val_lidar_front_right = val

    elif msg.topic == CAMERA_1:
        with lock:
            val_camera_1 = val

    if selected_sensor == "camera":
        lcd.set_cursor_position(0, 2)
        lcd.write(val_camera_1)
    elif selected_sensor == "lidar_left":
        lcd.set_cursor_position(0, 2)
        lcd.write(val_lidar_front_left + " mm")
    else:
        lcd.set_cursor_position(0, 2)
        lcd.write(val_lidar_front_right + " mm")

        # If payload is an int byte array, use: int.from_bytes(msg.payload, byteorder="big"))
        # int.from_bytes() requires python3: https://docs.python.org/3/library/stdtypes.html#int.from_bytes


if __name__ == "__main__":
    # Parse CLI args
    args = cli.setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args["loglevel"])

    # Setup MQTT client
    mqtt_conn = MqttConnection(args["mqtt_host"],
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

    print("Exiting...")


@nav.on(nav.LEFT)
def handle_left(ch, evt):
    selected_sensor = "lidar_left"
    print("Left Lidar Display")
    lcd.clear()
    lcd.set_cursor_position(0, 0)

    lcd.write("Left Lidar")
    lcd.set_cursor_position(0, 2)

    lcd.write("null")


@nav.on(nav.RIGHT)
def handle_right(ch, evt):
    selected_sensor = "lidar_right"
    print("Right Lidar")
    lcd.clear()
    lcd.set_cursor_position(0, 0)
    lcd.write("Right Lidar")

    lcd.set_cursor_position(0, 2)
    lcd.write("null")


@nav.on(nav.BUTTON)
def handle_button(ch, evt):
    selected_sensor = "camera"
    print("Camera")
    lcd.clear()
    lcd.set_cursor_position(0, 0)
    lcd.write("Camera")

    lcd.set_cursor_position(0, 2)

    lcd.write("null")


signal.pause()
