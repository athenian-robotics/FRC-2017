#! /bin/bash

source ~pi/.profile
workon py2cv3
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/object-tracking/single_object_tracker.py --bgr "174, 56, 5" --width 500 --usb --http --host raspi11.local &> ~pi/git/FRC-2017/logs/object-tracker.out &
