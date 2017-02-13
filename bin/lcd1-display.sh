#!/usr/bin/env bash

export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics
python3 ~pi/git/FRC-2017/lidarDisplay.py --mqtt mqtt-turtle.local &> ~pi/git/FRC-2017/logs/lidarDisplay.out &