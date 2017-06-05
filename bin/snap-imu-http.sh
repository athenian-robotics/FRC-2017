#!/usr/bin/env bash

date > ~pi/git/FRC-2017/logs/snap-lidar-http.reboot
export PYTHONWARNINGS="ignore"
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics

python ~pi/git/distance-tracking/snap_motion_server.py --did 00FEBABC --baud 115200 &> ~pi/git/FRC-2017/logs/snap_motion_server.out &

