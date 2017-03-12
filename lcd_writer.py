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
CAMERA_VALUE_TOPIC = "camera/gear/x"
CAMERA_ALIGNMENT_TOPIC = "camera/gear/alignment"
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

lidar_left_val = ""
lidar_right_val = ""
lidar_front_val = ""
lidar_rear_val = ""
camera_v_val = ""
camera_a_val = ""
heading_calib_val = ""
heading_degrees_val = ""


class SensorInfo(object):
    def __init__(self, sensor_id, topic, desc):
        self.sensor_id = sensor_id
        self.topic = topic
        self.desc = desc
        self.value = ""


sensor_dict = {LIDAR_LEFT: SensorInfo(LIDAR_LEFT, LIDAR_LEFT_TOPIC, "Lidar Left"),
               LIDAR_RIGHT: SensorInfo(LIDAR_RIGHT, LIDAR_RIGHT_TOPIC, "Lidar Right"),
               LIDAR_FRONT: SensorInfo(LIDAR_FRONT, LIDAR_FRONT_TOPIC, "Lidar Front"),
               LIDAR_REAR: SensorInfo(LIDAR_REAR, LIDAR_REAR_TOPIC, "Lidar Rear"),
               CAMERA: SensorInfo(CAMERA, CAMERA_VALUE_TOPIC, "Camera"),
               HEADING_CALIB: SensorInfo(HEADING_CALIB, HEADING_CALIBRATION_TOPIC, "Calibration"),
               HEADING_DEGREES: SensorInfo(HEADING_DEGREES, HEADING_DEGREES_TOPIC, "Degrees")}

sensors = deque([sensor_dict[LIDAR_LEFT],
                 sensor_dict[LIDAR_RIGHT],
                 sensor_dict[LIDAR_FRONT],
                 sensor_dict[LIDAR_REAR],
                 sensor_dict[CAMERA],
                 sensor_dict[HEADING_CALIB],
                 sensor_dict[HEADING_DEGREES]])

# default sensor
selected_sensor = sensors[0].sensor_id

# lcd initialization
lcd.clear()
backlight.rgb(255, 255, 255)
lcd.set_contrast(45)
lcd.clear()


def on_connect(client, userdata, flags, rc):
    global sensor_dict
    logger.info("Connected with result code: {0}".format(rc))

    for sensor in sensor_dict:
        client.subscribe(sensor.topic)
    client.subscribe(CAMERA_ALIGNMENT_TOPIC)


def on_message(client, userdata, msg):
    global lidar_right_val, lidar_left_val, lidar_front_val, lidar_rear_val, camera_a_val, camera_v_val, heading_degrees_val, heading_calib_val
    # Payload is a string byte array
    val = bytes.decode(msg.payload)
    logger.info("{0} : {1}".format(msg.topic, val))

    if msg.topic == LIDAR_LEFT_TOPIC:
        logger.info("LCD Lidar Left: " + val)
        lidar_left_val = val

    elif msg.topic == LIDAR_RIGHT_TOPIC:
        logger.info("LCD Lidar Right: " + val)
        lidar_right_val = val

    if msg.topic == LIDAR_FRONT_TOPIC:
        logger.info("LCD Lidar Front: " + val)
        lidar_front_val = val

    elif msg.topic == LIDAR_REAR_TOPIC:
        logger.info("LCD Lidar Rear: " + val)
        lidar_rear_val = val

    elif msg.topic == CAMERA_VALUE_TOPIC:
        logger.info("LCD Camera Value: " + val)
        camera_v_val = val

    elif msg.topic == CAMERA_ALIGNMENT_TOPIC:
        logger.info("LCD Camera Alignment: " + val)
        camera_a_val = val

    elif msg.topic == HEADING_CALIBRATION_TOPIC:
        logger.info("LCD Calibration: " + val)
        heading_calib_val = val.replace(" ", "", 10)

    elif msg.topic == HEADING_DEGREES_TOPIC:
        logger.info("LCD Degrees: " + val)
        heading_degrees_val = val


def lcd_display(delay=0.1):
    global lidar_right_val, lidar_left_val, lidar_front_val, lidar_rear_val, camera_a_val, camera_v_val, heading_degrees_val, heading_calib_val
    while True:
        if selected_sensor == LIDAR_LEFT:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Left")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_left_val + " mm")
            if lidar_left_val == "-1" and lidar_right_val == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDAR_RIGHT:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Right")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_right_val + " mm")
            if lidar_left_val == "-1" and lidar_right_val == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDAR_FRONT:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Front")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_front_val + " cm")
            if lidar_front_val == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == LIDAR_REAR:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Lidar Rear")
            lcd.set_cursor_position(0, 2)
            lcd.write(lidar_rear_val + " cm")
            if lidar_rear_val == "-1":
                backlight.rgb(255, 0, 0)
            else:
                backlight.rgb(255, 255, 255)


        elif selected_sensor == CAMERA:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Camera")
            lcd.set_cursor_position(0, 2)
            lcd.write(camera_v_val)
            if camera_a_val == NOT_SEEN:
                backlight.rgb(255, 0, 0)
            elif camera_a_val == NOT_ALIGNED:
                backlight.rgb(0, 0, 255)
            elif camera_a_val == ALIGNED:
                backlight.rgb(0, 255, 0)

        elif selected_sensor == HEADING_CALIB:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Calibration")
            lcd.set_cursor_position(0, 2)
            lcd.write(heading_calib_val)
            if heading_calib_val == CALIBRATION_BY_VALUES:
                backlight.rgb(0, 255, 0)
            else:
                backlight.rgb(255, 255, 255)

        elif selected_sensor == HEADING_DEGREES:
            lcd.clear()
            lcd.set_cursor_position(0, 0)
            lcd.write("Degrees")
            lcd.set_cursor_position(0, 2)
            lcd.write(heading_degrees_val)

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
