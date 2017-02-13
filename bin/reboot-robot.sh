#!/usr/bin/env bash

# Reboot Robot Raspis
echo "Rebooting Robot Raspis"
ssh -o StrictHostKeyChecking=no pi@camera-gear.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@lidar-gear-left.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@lidar-gear-right.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@mqtt-turtle.local sudo reboot now
ssh -o StrictHostKeyChecking=no pi@lcd1.local sudo reboot now
