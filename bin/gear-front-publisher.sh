#!/usr/bin/env bash

source ~pi/.profile
workon py2cv3
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/FRC-2017/location_publisher.py --grpc camera-gear.local --camera camera/gear --mqtt mqtt-turtle.local &> ~pi/git/FRC-2017/logs/gear-front-publisher.out &

