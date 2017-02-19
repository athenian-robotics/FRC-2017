#!/usr/bin/env bash
date > ~pi/git/FRC-2017/logs/lidar_display.reboot
sleep 5
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/lidar_display.py --mqtt mqtt-turtle.local &> ~pi/git/FRC-2017/logs/lidar_display.out &
