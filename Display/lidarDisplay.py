#!/usr/bin/env python2

import signal

import dothat.backlight as backlight
import dothat.lcd as lcd
import dothat.touch as nav

lcd.clear()
backlight.rgb(255, 255, 255)
lcd.set_contrast(45)


@nav.on(nav.LEFT)
def handle_left(ch, evt):
    print("Left Lidar Display")
    lcd.clear()
    lcd.set_cursor_position(0, 0)
    lcd.write("Left Lidar")
    lcd.set_cursor_position(0, 2)

    lcd.write("       23 mm")


@nav.on(nav.RIGHT)
def handle_right(ch, evt):
    print("Right Lidar")
    lcd.clear()
    lcd.set_cursor_position(0, 0)
    lcd.write("Right Lidar")
    lcd.set_cursor_position(0, 2)

    lcd.write("       23 mm")


@nav.on(nav.BUTTON)
def handle_button(ch, evt):
    print("Camera")
    lcd.clear()
    lcd.set_cursor_position(0, 0)
    lcd.write("Camera")
    lcd.set_cursor_position(0, 2)

    lcd.write("     Objects: 2")


signal.pause()
