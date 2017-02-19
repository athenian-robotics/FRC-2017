#!/usr/bin/env bash
date > ~pi/git/FRC-2017/logs/lidar-rear-publisher.reboot
sleep 5
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/long-lidar_publisher.py --mqtt mqtt-turtle.local --avg_size 10 --device rear --did 2341:0043 --baud 115200 &> ~pi/git/FRC-2017/logs/lidar-rear-publisher.out &
