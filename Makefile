default: help

help:
	echo "Try make github, make robot or make reboot"

robot:
	./bin/push-to-robot.sh

github:
	./bin/pull-from-github.sh

reboot:
	./bin/reboot-robot.sh

shutdown:
	./bin/shutdown-robot.sh


camera-logs:
	echo "********** Camera Gear Last Reboot Time **********"
	ssh camera-gear last reboot | head -1
	echo "********** Camera Gear Object Tracker **********"
	ssh camera-gear cat /home/pi/git/FRC-2017/logs/dual-tape-tracker.out
	echo "********** Camera Gear Publisher **********"
	ssh camera-gear cat /home/pi/git/FRC-2017/logs/gear-front-publisher.out

lidar-logs:
	echo "********** Lidar Gear Last Reboot Time **********"
	ssh lidar-gear last reboot | head -1
	echo "********** Left Lidar Publisher **********"
	ssh lidar-gear cat /home/pi/git/FRC-2017/logs/lidar-left-publisher.out
	echo "********** Right Lidar Publisher **********"
	ssh lidar-gear cat /home/pi/git/FRC-2017/logs/lidar-right-publisher.out
	echo "********** Heading Publisher **********"
	ssh lidar-gear cat /home/pi/git/FRC-2017/logs/heading_publisher.out

lcd1-logs:
	echo "********** LCD1 Last Reboot Time **********"
	ssh lcd1 last reboot | head -1
	echo "********** Left Lidar Publisher **********"
	ssh lcd1 cat /home/pi/git/FRC-2017/logs/lidar_display.out.out
