#!/usr/bin/env bash
date > ~pi/git/FRC-2017/logs/lidar-right-publisher.reboot
sleep 5
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/short_lidar_publisher.py --mqtt mqtt-turtle.local --device right --did 95538333535351019130 --baud 115200 &> ~pi/git/FRC-2017/logs/lidar-right-publisher.out &
