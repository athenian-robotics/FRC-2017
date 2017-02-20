#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/object-filter.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/single_object_filter.py --bgr "174, 56, 5"  --sleep 60 --width 400 --delay 0.25 --flipy --usb --camera "Front Gear" --http "camera-gear.local:5800" --vertical &> ~pi/git/FRC-2017/logs/object-filter.out &

# 59, 66, 197 is orange
# 174, 56, 5 is blue
# 46, 43, 144 is red box