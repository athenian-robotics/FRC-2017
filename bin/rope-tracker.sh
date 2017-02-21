#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/rope-tracker.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/single_object_filter.py --bgr "59, 66, 197"  --sleep 60 --width 500 --draw_contour --draw_box --delay 0.25 --flipy --usb --camera "Rear Rope" --http "camera-rope.local:5800" --vertical &> ~pi/git/FRC-2017/logs/rope-tracker.out &

