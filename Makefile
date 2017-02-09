default: help

help:
	echo "Try make github, make robot or make reboot"
robot:
	./bin/push-to-robot.sh

github:
	./bin/pull-from-github.sh

reboot:
	./bin/reboot-robot.sh
