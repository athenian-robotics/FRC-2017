#!/usr/bin/env bash
source ~pi/.profile
workon py2cv3
date > ~pi/git/FRC-2017/logs/gear-front-publisher-peg.reboot
sleep 5
export PYTHONPATH=${PYTHONPATH}:~pi/git/common-robotics:~pi/git/object-tracking
python2 ~pi/git/FRC-2017/location_publisher.py --grpc camera-gear.local:50052 --camera camera/gear/peg --mqtt mqtt-turtle.local &> ~pi/git/FRC-2017/logs/gear-front-publisher-peg.out &

