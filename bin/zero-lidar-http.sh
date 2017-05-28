#!/usr/bin/env bash

date > ~pi/git/FRC-2017/logs/zero-lidar-http.reboot
export PYTHONWARNINGS="ignore"
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics

python ~pi/git/distance-tracking/simple_distance_server.py --did 00FEBABC --baud 115200 &> ~pi/git/FRC-2017/logs/distance_server.out &

