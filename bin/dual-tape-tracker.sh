#!/usr/bin/env bash

source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/dual-tape-tracker.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/dual_object_filter.py  --bgr "172, 220, 14"  --mask_y 0  --draw_contour --draw_box --sleep 0 --width 500 --delay 0.25 --flipy --usb --camera "Gear Dual Tape" --http "127.0.0.1:8080" --vertical &> ~pi/git/FRC-2017/logs/dual-tape-tracker.out &

# --file /home/pi/git/FRC-2017/html/2-image.html