#!/usr/bin/env bash

source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/dual-tape-tracker.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/dual_object_filter.py --bgr "172, 220, 14"  --draw_contour --draw_box --width 500 --delay 0.25 --flipy --usb_port 1 --camera "Gear Camera" --http "camera-gear.local:8082" --vertical &> ~pi/git/FRC-2017/logs/2nd-camera.out &

