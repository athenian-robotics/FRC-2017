#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/dualtape-peg-object-tracker.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/multi_object_tracker.py --dualbgr "172, 220, 14" --singlebgr "126, 113, 116" --draw_contour --draw_box --sleep 60 --width 500 --delay 0.25 --flipy --usb --http "camera-gear.local:8080" --vertical &> ~pi/git/FRC-2017/logs/dualtape-peg-object-tracker.out &


# 174, 56, 5 is blue
# 46, 43, 144 is red box