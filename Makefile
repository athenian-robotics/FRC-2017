default: help

help:
	echo "Try make github, make robot or make reboot"

robot:
	./bin/push-to-robot.sh

github:
	./bin/pull-from-github.sh

reboot:
	./bin/reboot-robot.sh


camera-gear:
	echo "********** Camera Gear Front Last Reboot Time **********"
	ssh camera-gear last reboot | head -1
	echo "********** Camera Gear Front Object Tracker **********"
	ssh camera-gear cat /home/pi/git/FRC-2017/logs/object-tracker.out
	echo "********** Camera Gear Front Publisher **********"
	ssh camera-gear cat /home/pi/git/FRC-2017/logs/gear-front-publisher.out
