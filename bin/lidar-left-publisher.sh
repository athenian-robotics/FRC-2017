#! /bin/bash

source ~pi/.profile
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python3 ~pi/git/FRC-2017/lidar_publisher.py --mqtt mqtt-turtle.local --device lidar_l --serial ttyACM0 &> ~pi/git/FRC-2017/logs/lidar-left-publisher.out &

