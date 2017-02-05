#! /bin/bash

source ~pi/.profile
workon py2cv3
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/single_object_tracker.py --bgr "174, 56, 5" --width 400 --flipy --usb --http "raspi11.local:8080" &> ~pi/git/FRC-2017/logs/object-tracker.out &


# 174, 56, 5 is blue
# 46, 43, 144 is red box