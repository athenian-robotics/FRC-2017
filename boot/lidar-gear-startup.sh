#!/usr/bin/env bash

# Publish lidar data
su - pi -c ~pi/git/FRC-2017/bin/lidar-right-publisher.sh
su - pi -c ~pi/git/FRC-2017/bin/lidar-left-publisher.sh

# Publish heading data
su - pi -c ~pi/git/FRC-2017/bin/heading-publisher.sh
