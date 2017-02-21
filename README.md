# FRC-2017 Notes

## Raspi Names

| #   | Name                       | Repos                                              |
|:---:|:---------------------------|:---------------------------------------------------|
| 12  | **mqtt-turtle.local**      | none                                               |
| 11  | **camera-gear.local**      | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017), [object-tracker](https://github.com/athenian-robotics/object-tracking)          |
| 10  | **lidar-gear.local**       | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017)                          |
| 24  | **lcd1.local**             | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017) |

## MQTT Topics 
| Name                      | Description                                             |
|:--------------------------|:--------------------------------------------------------|
|**camera/gear/x**          | Camera center position and screen width (String:String) |
|**camera/gear/peg/x**      | Peg position and screen width (String:String)           |
|**camera/gear/dualtape/x** | Avg dual tape position and screen width (String:String) |
|**camera/gear/alignment**  | Camera relative to object (String)                      |
|**lidar/left/mm**          | Left lidar distance (String)                            |
|**lidar/right/mm**         | Right lidar distance (String)                           |
|**lidar/front/cm**         | Front lidar distance (String)                           |
|**lidar/rear/cm**          | Rear lidar distance (String)                            |
|**heading/degrees**        | Heading degrees (String)                                |
|**heading/calibration**    | Calibration status (String)                             |

## Arduino Device IDs
| Location                  | ID                                                      |
|:--------------------------|:--------------------------------------------------------|
|Heading (Arduino)          | 95530343235351A0E0A2                                    |
|Heading (Metro)            | 00FEBABC                                                |
|Left lidar                 | 7543331373935160E190                                    |
|Right lidar                | 95538333535351019130                                    |
|Forward lidar              |                                                         |
|Rear lidar                 |                                                         |


## Heading Sensor

The heading sensor calibration is described [here](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/webgl-example?embeds=allow#sensor-calibration)

## SSH Setup

* [SSH Configuration](https://github.com/athenian-robotics/FRC-2017/wiki/SSH-configuration-file)
* [Using SSH without a password](https://github.com/athenian-robotics/FRC-2017/wiki/Using-SSH-without-a-password)


## Remote repo setup for Raspis

Setting up remote repos on Raspis will allow you to push changes to Raspis without the Raspis
have access to github.

* [OSX Configuration](https://github.com/athenian-robotics/FRC-2017/wiki/OSX-configuration-for-remote-repos)
* [Raspi Configuration](https://github.com/athenian-robotics/FRC-2017/wiki/Raspi-configuration-for-remote-repos)


## Raspi launch scripts

* [Makefile commands](https://github.com/athenian-robotics/FRC-2017/wiki/Makefile-commands)
* [Raspi boot scripts](https://github.com/athenian-robotics/FRC-2017/wiki/Raspi-boot-scripts)

## rc.local edits (append above ```exit 0```)

lidar-gear:

```bash
su - pi -c ~pi/git/FRC-2017/bin/lidar-right-publisher.sh
su - pi -c ~pi/git/FRC-2017/bin/lidar-left-publisher.sh
su - pi -c ~pi/git/FRC-2017/bin/heading-publisher.sh
```
camera-gear:
  
```bash# Tune exposure on camera
v4l2-ctl -d /dev/video0 -c exposure_auto=1 -c exposure_absolute=20
\# We have two configurations: object tracking and color picking
\# They both need exclusive camera access, so if one of the two is enabled,
\# the other needs to be commented out.
```
 Object tracking
```bash
#su - pi -c ~pi/git/FRC-2017/bin/dual-tape-tracker.sh
su - pi -c ~pi/git/FRC-2017/bin/dual-tape-peg-tracker.sh
su - pi -c ~pi/git/FRC-2017/bin/gear-front-publisher.sh
```
 Color picking
```bash
#su - pi -c ~pi/git/FRC-2017/bin/color-picker.sh
```

lcd1:

```bash
su - pi -c ~pi/git/FRC-2017/bin/clear-logs.sh
su - pi -c ~pi/git/FRC-2017/bin/lcd1-display.sh
```

## Listening to MQTT traffic

Listen to all user msgs with:

```bash
$ mosquitto_sub -h mqtt-turtle.local -t "#"
```

Listen to all system msgs with:

```bash
$ mosquitto_sub -h mqtt-turtle.local -t "\$SYS/#"
```

