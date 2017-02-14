#!/usr/bin/env bash
date > ~pi/git/FRC-2017/logs/heading_publisher.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python2 ~pi/git/FRC-2017/heading_publisher.py --mqtt mqtt-turtle.local --device left --serial /dev/ttyACM0 --baud 9600 &> ~pi/git/FRC-2017/logs/heading_publisher.out &
