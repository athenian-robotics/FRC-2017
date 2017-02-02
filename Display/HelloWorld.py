#!/usr/bin/env python2

import dothat.lcd as lcd
from dothat import backlight

lcd.clear()
backlight.rgb(100, 100, 100)
lcd.set_cursor_position(0, 1)
lcd.set_contrast(45)
lcd.write("     23 mm      ")
lcd.create_char(1, 1)
