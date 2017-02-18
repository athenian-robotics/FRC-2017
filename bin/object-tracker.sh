#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/object-tracker.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/single_object_filter.py --bgr "59, 66, 197"  --width 400 --delay 0.25 --flipy --usb --http "camera-gear.local:5800" &> ~pi/git/FRC-2017/logs/object-filter.out &

# 174, 56, 5 is blue
# 46, 43, 144 is red box