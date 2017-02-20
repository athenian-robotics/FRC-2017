#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/dual-tape-tracker.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/dual_object_filter.py --bgr "214, 201, 172"  -- countours --box --sleep 90 --width 500 --delay 0.25 --flipy --usb --camera "Front Gear" --http "camera-gear.local:5800" --vertical &> ~pi/git/FRC-2017/logs/dual-tape-tracker.out &

