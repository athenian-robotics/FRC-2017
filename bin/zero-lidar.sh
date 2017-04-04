#!/usr/bin/env bash

date > ~pi/git/FRC-2017/logs/zero-lidar.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics

python ~pi/git/distance-tracking/distance_server.py --did 00FEBA85 --baud 115200 &> ~pi/git/FRC-2017/logs/distance_server.out &
