#!/usr/bin/env bash

# Reboot robot Raspis
echo "Rebooting robot Raspis"
ssh pi@camera-gear.local sudo reboot now
ssh pi@lidar-gear-left.local sudo reboot now
ssh pi@lidar-gear-right.local sudo reboot now
ssh pi@mqtt-turtle.local sudo reboot now
