#!/usr/bin/env bash

date > ~pi/git/FRC-2017/logs/heading_publisher.reboot
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/heading_publisher.py --mqtt mqtt-turtle.local --mpt 1 --calib --cpt 2 --did 95530343235351A0E0A2 --baud 115200 &> ~pi/git/FRC-2017/logs/heading_publisher.out &

# Arduino with 9-DOF DID is 95530343235351A0E0A2
# Metro mini with 9-DOF DID is 00FEBABC