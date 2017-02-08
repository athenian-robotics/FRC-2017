#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python3 ~pi/git/FRC-2017/lidar_publisher.py --mqtt mqtt-turtle.local --device left --serial /dev/ttyACM0 &> ~pi/git/FRC-2017/logs/lidar-left-publisher.out &
