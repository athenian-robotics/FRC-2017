#!/usr/bin/env python2

import logging
import time
from collections import deque
from threading import Thread

import cli_args as cli
import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav
from constants import MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import setup_logging
from utils import sleep

from heading_publisher import CALIBRATION_BY_VALUES

logger = logging.getLogger(__name__)

# Constants
LIDAR_LEFT_TOPIC = "lidar/left/mm"
LIDAR_RIGHT_TOPIC = "lidar/right/mm"
LIDAR_FRONT_TOPIC = "lidar/front/cm"
LIDAR_REAR_TOPIC = "lidar/rear/cm"
CAMERA_1_VALUE_TOPIC = "camera/gear/x"
CAMERA_1_ALIGNMENT_TOPIC = "camera/gear/alignment"
HEADING_CALIBRATION_TOPIC = "heading/calibration"
HEADING_DEGREES_TOPIC = "heading/degrees"
NOT_SEEN = "not_seen"
NOT_ALIGNED = "not_aligned"
ALIGNED = "aligned"

CAMERA = "camera"
LIDAR_LEFT = "lidarleft"
LIDAR_RIGHT = "lidarright"
LIDAR_FRONT = "lidarfront"
LIDAR_REAR = "lidarrear"
HEADING_DEGREES = "headingd"
HEADING_CALIB = "headingc"

lidar_left = ""
lidar_right = ""
lidar_front = ""
lidar_rear = ""
camera_v = ""
camera_a = ""
heading_calib = ""
heading_degrees = ""


#
class SensorInfo(object):
    def __init__(self, sensor_id, desc):
        self.sensor_id = sensor_id
        self.desc = desc


sensors = deque([SensorInfo(LIDAR_LEFT, "Lidar Left"),
                 SensorInfo(LIDAR_RIGHT, "Lidar Right"),
                 SensorInfo(LIDAR_FRONT, "Lidar Front"),
                 SensorInfo(LIDAR_REAR, "Lidar Rear"),
                 SensorInfo(CAMERA, "Camera"),
                 SensorInfo(HEADING_CALIB, "Calibration"),
                 SensorInfo(HEADING_DEGREES, "Degrees")])

# default sensor
selected_sensor = sensors[0].sensor_id

# lcd initialization
lcd.clear()
backlight.rgb(255, 255, 255)
lcd.set_contrast(45)
lcd.clear()


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code: {0}".format(rc))
    client.subscribe(LIDAR_LEFT_TOPIC)
    client.subscribe(LIDAR_RIGHT_TOPIC)
    client.subscribe(LIDAR_FRONT_TOPIC)
    client.subscribe(LIDAR_REAR_TOPIC)
    client.subscribe(CAMERA_1_VALUE_TOPIC)
    client.subscribe(CAMERA_1_ALIGNMENT_TOPIC)
    client.subscribe(HEADING_DEGREES_TOPIC)
    client.subscribe(HEADING_CALIBRATION_TOPIC)


def on_message(client, userdata, msg):
    global lidar_right, lidar_left, lidar_front, lidar_rear, camera_a, camera_v, heading_degrees, heading_calib
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    logger.info("{0} : {1}".format(msg.topic, val))

    if msg.topic == LIDAR_LEFT_TOPIC:
        logger.info("LCD Lidar Left: " + val)
        lidar_left = val

    elif msg.topic == LIDAR_RIGHT_TOPIC:
        logger.info("LCD Lidar Right: " + val)
        lidar_right = val

    if msg.topic == LIDAR_FRONT_TOPIC:
        logger.info("LCD Lidar Front: " + val)
        lidar_front = val

    elif msg.topic == LIDAR_REAR_TOPIC:
        logger.info("LCD Lidar Rear: " + val)
        lidar_rear = val


    elif msg.topic == CAMERA_1_VALUE_TOPIC:
        logger.info("LCD Camera Value: " + val)
        camera_v = val

    elif msg.topic == CAMERA_1_ALIGNMENT_TOPIC:
        logger.info("LCD Camera Alignment: " + val)
        camera_a = val

    elif msg.topic == HEADING_CALIBRATION_TOPIC:
        logger.info("LCD Calibration: " + val)
        val = val.replace(" ", "", 10)
        heading_calib = val

    elif msg.topic == HEADING_DEGREES_TOPIC:
        logger.info("LCD Degrees: " + val)
        heading_degrees = val


def lcd_display(delay=0.1):
    global lidar_right, lidar_left, lidar_front, lidar_rear, camera_a, camera_v, heading_degrees, heading_calib
    while True:
        if selected_sensor == LIDAR_LEFT:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Left")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_left + " mm")
            if lidar_left == "-1" and lidar_right == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDAR_RIGHT:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Right")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_right + " mm")
            if lidar_left == "-1" and lidar_right == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDAR_FRONT:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Front")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_front + " cm")
            if lidar_front == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDAR_REAR:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Rear")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_rear + " cm")
            if lidar_rear == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)


        elif selected_sensor == CAMERA:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Camera")
            lcd.set_cursor_position(0, 2)
            lcd.write(camera_v)
            if camera_a == NOT_SEEN:
                backlight.rgb(255, 0, 0)
            elif camera_a == NOT_ALIGNED:
                backlight.rgb(0, 0, 255)
            elif camera_a == ALIGNED:
                backlight.rgb(0, 255, 0)

        elif selected_sensor == HEADING_CALIB:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Calibration")
            lcd.set_cursor_position(0, 2)
            lcd.write(heading_calib)
            if heading_calib == CALIBRATION_BY_VALUES:
                backlight.rgb(0, 255, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == HEADING_DEGREES:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Degrees")
            lcd.set_cursor_position(0, 2)
            lcd.write(heading_degrees)

        time.sleep(delay)


@nav.on(nav.UP)
def handle_button(ch, evt):
    global sensors, selected_sensor
    sensors.rotate(1)
    selected_sensor = sensors[0].sensor_id
    logger.info(sensors[0].desc)
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write(sensors[0].desc)
    lcd.set_cursor_position(0, 2)


@nav.on(nav.DOWN)
def handle_button(ch, evt):
    global sensors, selected_sensor
    sensors.rotate(-1)
    selected_sensor = sensors[0].sensor_id
    logger.info(sensors[0].desc)
    lcd.clear()
    backlight.rgb(255, 255, 255)
    lcd.set_cursor_position(0, 0)
    lcd.write(sensors[0].desc)
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

    Thread(target=lcd_display, args=(0.1,)).start()

    try:
        sleep()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_conn.disconnect()

    logger.info("Exiting...")
