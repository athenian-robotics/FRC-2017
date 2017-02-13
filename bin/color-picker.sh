#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
~pi/git/object-tracking/color_picker.py --width 600 --flipy --path /home/pi/git/object-tracking/html
