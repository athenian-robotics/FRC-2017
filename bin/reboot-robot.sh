#!/usr/bin/env bash

# Reboot robot Raspis
echo "Rebooting robot Raspis"
ssh -o StrictHostKeyChecking=no pi@camera-gear.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@lidar-gear-left.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@lidar-gear-right.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@mqtt-turtle.local sudo reboot now
