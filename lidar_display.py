#!/usr/bin/env python2

import logging

import cli_args as cli
import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from constants import MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

logger = logging.getLogger(__name__)

# default sensor
selected_sensor = "camera"

# Constants
LIDAR_FRONT_LEFT = "lidar/left/mm"
LIDAR_FRONT_RIGHT = "lidar/right/mm"
CAMERA_1_VALUE = "camera/gear/x"
CAMERA_1_ALIGNMENT = "camera/gear/alignment"
HEADING_CALIBRATION = "heading/calibration"
HEADING_DEGREES = "heading/degrees"
NOT_SEEN = "not_seen"
NOT_ALIGNED = "not_aligned"
ALIGNED = "aligned"

lidar_l = ""
lidar_r = ""

# lcd initialization
lcd.clear()
backlight.rgb(255, 255, 255)
lcd.set_contrast(45)
lcd.clear()
lcd.set_cursor_position(0, 0)
lcd.write("Camera")
lcd.set_cursor_position(0, 2)
lcd.write("null")


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    client.subscribe(LIDAR_FRONT_LEFT)
    client.subscribe(LIDAR_FRONT_RIGHT)
    client.subscribe(CAMERA_1_VALUE)
    client.subscribe(CAMERA_1_ALIGNMENT)


def on_message(client, userdata, msg):
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    logger.info("{0} : {1}".format(msg.topic, val))

    if msg.topic == LIDAR_FRONT_LEFT:
        logger.info("Lidar L: " + val)
        lidar_l = val
        if selected_sensor == "lidar_left":
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Left")
            lcd.set_cursor_position(0, 2)
            lcd.write(val + " mm")
            if val == "-1" and lidar_l == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

    elif msg.topic == LIDAR_FRONT_RIGHT:
        logger.info("Lidar R: " + val)
        lidar_r = val
        if selected_sensor == "lidar_right":
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Right")
            lcd.set_cursor_position(0, 2)
            lcd.write(val + " mm")
            if val == "-1" and lidar_r == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

    elif msg.topic == CAMERA_1_VALUE:
        logger.info("Camera Value: " + val)
        if selected_sensor == "camera":
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Camera")
            lcd.set_cursor_position(0, 2)
            lcd.write(val)

    elif msg.topic == CAMERA_1_ALIGNMENT:
        logger.info("Camera Alignment: " + val)
        if selected_sensor == "camera":
            if val == NOT_SEEN:
                backlight.rgb(255, 0, 0)
            elif val == NOT_ALIGNED:
                backlight.rgb(0, 0, 255)
            elif val == ALIGNED:
                backlight.rgb(0, 255, 0)

    elif msg.topic == HEADING_CALIBRATION:
        logger.info("Calibration: " + val)
        if selected_sensor == "calibration":
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Calibration")
            lcd.set_cursor_position(0, 2)
            lcd.write(val)
            if val == "Sys:3 G:3 A:3 M:3":
                backlight.rgb(0, 255, 0)
            else:
                backlight.rgb(255, 255, 255)

    elif msg.topic == HEADING_DEGREES:
        logger.info("degrees: " + val)
        if selected_sensor == "degrees":
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Degrees")
            lcd.set_cursor_position(0, 2)
            lcd.write(val)



            # If payload is an int byte array, use: int.from_bytes(msg.payload, byteorder="big"))
            # int.from_bytes() requires python3: https://docs.python.org/3/library/stdtypes.html#int.from_bytes


@nav.on(nav.LEFT)
def handle_left(ch, evt):
    global selected_sensor
    selected_sensor = "lidar_left"
    logger.info("Left Lidar Display")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)

    lcd.write("Left Lidar")
    lcd.set_cursor_position(0, 2)


@nav.on(nav.RIGHT)
def handle_right(ch, evt):
    global selected_sensor
    selected_sensor = "lidar_right"
    logger.info("Right Lidar")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Right Lidar")

    lcd.set_cursor_position(0, 2)


@nav.on(nav.BUTTON)
def handle_button(ch, evt):
    global selected_sensor
    selected_sensor = "camera"
    logger.info("Camera")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Camera")

    lcd.set_cursor_position(0, 2)


@nav.on(nav.UP)
def handle_button(ch, evt):
    global selected_sensor
    selected_sensor = "calibration"
    logger.info("Calibration")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Calibration")

    lcd.set_cursor_position(0, 2)


@nav.on(nav.DOWN)
def handle_button(ch, evt):
    global selected_sensor
    selected_sensor = "degrees"
    logger.info("Degrees")
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write("Degrees")

    lcd.set_cursor_position(0, 2)


if __name__ == "__main__":
    # Parse CLI args
    args = cli.setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])

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
