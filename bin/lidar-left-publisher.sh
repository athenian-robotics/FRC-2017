#!/usr/bin/env bash
date > ~pi/git/FRC-2017/logs/lidar-left-publisher.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/lidar_publisher.py --mqtt mqtt-turtle.local --device left --pid 2341:0043 --baud 115200 &> ~pi/git/FRC-2017/logs/lidar-left-publisher.out &
