#!/usr/bin/env bash

# Push common-robotics repo
echo "Pushing common-robotics to robot"
cd ~/git/common-robotics
git push camera-gear master
git push lidar-gear-left master
git push lidar-gear-right master

# Push FRC-2017 repo
echo "Pushing FRC-2017 to robot"
cd ~/git/FRC-2017
git push camera-gear dev
git push lidar-gear-left dev
git push lidar-gear-right dev

# Push object-tracking repo
echo "Pushing object-tracking to robot"
cd ~/git/object-tracking
git push camera-gear master


