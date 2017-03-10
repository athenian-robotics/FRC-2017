#!/usr/bin/env bash

su - pi -c ~pi/git/FRC-2017/bin/rope-tracker.sh
#su - pi -c ~pi/git/FRC-2017/bin/rope-publisher.sh

# Publish heading data
su - pi -c ~pi/git/FRC-2017/bin/heading-publisher.sh
