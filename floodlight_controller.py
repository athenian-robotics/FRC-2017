#!/usr/bin/env python3

import json
import logging
import sys

import cli_args as cli
from constants import MQTT_HOST, LOG_LEVEL
from mqtt_connection import MqttConnection
from utils import is_python3
from utils import setup_logging

logger = logging.getLogger(__name__)

if is_python3():
    import tkinter as tk
else:
    import Tkinter as tk

COMMAND_TOPIC = "roborio/status/floodlight"

if __name__ == "__main__":
    # Parse CLI args
    args = cli.setup_cli_args(cli.mqtt_host, cli.verbose)

    # Setup logging
    setup_logging(level=args[LOG_LEVEL])


    # Define MQTT callbacks
    def on_connect(client, userdata, flags, rc):
        logger.info("Connected with result code: {0}".format(rc))


    def on_disconnect(client, userdata, rc):
        logger.info("Disconnected with result code: {0}".format(rc))


    def on_publish(client, userdata, mid):
        logger.debug("Published value to {0} with message id {1}".format(COMMAND_TOPIC, mid))


    # Create MQTT connection
    mqtt_conn = MqttConnection(args[MQTT_HOST],
                               on_connect=on_connect,
                               on_disconnect=on_disconnect,
                               on_publish=on_publish)
    mqtt_conn.connect()


    # Define TK callbacks
    def update_display():
        global color, duration, duty_cycle, intensity


    def publish_value():
        global color, duration, duty_cycle, intensity
        # Encode payload into json object
        json_val = json.dumps({"color": color, "duration": duration, "duty_cycle": duty_cycle, "intensity": intensity})
        result, mid = mqtt_conn.client.publish(COMMAND_TOPIC, payload=json_val.encode('utf-8'))


    def set_direction(cmd):
        global direction
        direction = cmd
        publish_value()


    def on_key(event):
        global direction, speed
        key_clicked = eval(repr(event.char))
        if key_clicked == "+" or key_clicked == "=":
            if speed < 10:
                speed += 1
                publish_value()
        elif key_clicked == "-" or key_clicked == "_":
            if speed > 0:
                speed -= 1
                publish_value()
        elif key_clicked == " ":
            direction = STOP
            speed = 0
            publish_value()
        elif key_clicked == "q":
            mqtt_conn.disconnect()
            sys.exit()
        else:
            logger.info("Pressed {0}".format(key_clicked))


    def on_click(event):
        root.focus_set()
        logger.info("Clicked at {0},{1}".format(event.x, event.y))
        update_display()


    color = {"r": 127, "g": 0, "b": 0}
    duration = 0.5
    duty_cycle = 0.5
    intensity = 0.5

    root = tk.Tk()
    root.title("Floodlight Controller")
    root.focus()
    # For bind() details, see: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    root.bind("<Button-1>", on_click)

    canvas = tk.Canvas(root, bg="white", width=200, height=150)
    canvas.pack()

    selector_args = {"text": "", "bg": "gray", "height": 2, "font": ('courier', 14, 'bold')}
    title_args = {"text": "", "bg": "gray", "height": 2, "font": ('courier', 28, 'bold')}
    selectors = {"color": {}, "duration": {}, "duty_cycle": {}, "intensity": {}}
    settings = {"color": ("red", "green", "blue", "white"), "duration": ("0.25", "0.5", "1", "2"),
                "duty_cycle": ("0", "0.25", "0.5", "0.75", "1"), "intensity": ("0", "0.1", "0.2", "0.5")}

    tk.Label(root, text="Color", **title_args).grid(row=0).pack()
    selectors["color"]["red"] = tk.Label(root, text="")

    settings = ("red", "green", "blue", "white")
    for i, setting in enumerate(settings):
        selectors["color"][setting] = tk.Label(root, text=setting, **title_args)
        selectors["color"].grid(row=0, column=i).pack()

    selectors["duty_cycle"]["0.25"] = tk.Label(root, text="Color", **title_args).grid(row=0).pack()

    selectors["color"]["0.2"] = tk.Label(root, text="Color", **title_args).grid(row=0).pack()

    update_display()

    root.mainloop()
