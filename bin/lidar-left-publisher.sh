#!/usr/bin/env bash
date > ~pi/git/FRC-2017/logs/lidar-left-publisher.reboot
sleep 5
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/short_lidar_publisher.py --mqtt mqtt-turtle.local --device left --did 7543331373935160E190 --baud 115200 &> ~pi/git/FRC-2017/logs/lidar-left-publisher.out &
