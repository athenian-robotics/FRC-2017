# FRC-2017 Notes

## RoboRio

The RoboRio hostname is *roborio-852-frc.local*.  The configuration page is at: *roborio-852-frc.local:80*
## Raspi Names

| #   | Name                       | Repos                                              |
|:---:|:---------------------------|:---------------------------------------------------|
| 11  | **camera-gear.local**      | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017), [object-tracker](https://github.com/athenian-robotics/object-tracking)          |
| 18  | **camera-rope.local**      | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017), [object-tracker](https://github.com/athenian-robotics/object-tracking)          |
| 10  | **lidar-gear.local**       | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017)                          |
| 24  | **lcd1.local**             | [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017) |
| 12  | **mqtt-turtle.local**      | none                                               |

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
|Heading (Metro)            | 00FEBA85                                                |
|Left lidar                 | 7543331373935160E190                                    |
|Right lidar                | 95538333535351019130                                    |
|Front lidar                | 00FEBA8B                                                |
|Rear lidar                 | 00FEBA73                                                |


## Heading Sensor

The heading sensor calibration is described [here](https://learn.adafruit.com/bno055-absolute-orientation-sensor-with-raspberry-pi-and-beaglebone-black/webgl-example?embeds=allow#sensor-calibration)

## Metro Mini SNs

Metro Minis do not report their SN via the Arduin IDE. Use:
```bash
$ cd git/common-robotcs
$ ./metro_minis.py
```
 
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

## Camera Image Requirements

* Repos: [common-robotics](https://github.com/athenian-robotics/common-robotics), [FRC-2017](https://github.com/athenian-robotics/FRC-2017), [object-tracker](https://github.com/athenian-robotics/object-tracking)  

### PIP requirements


Raspbian with the *pysearchimages* distro (has OpenCV 3.2 package):

```bash
$ source start_py2cv3.sh
$
$ pip install --upgrade pip
$ pip install imutils
$ pip install grpcio
$ pip install paho-mqtt
$ pip install flask
$ pip install requests
$ pip install blinkt
$ pip install numpy
$ pip install pyserial
```

Vanilla Raspbian:

```bash
$ source start_py2cv3.sh
$
$ sudo pip install --upgrade pip
$ sudo pip install imutils
$ sudo pip install grpcio
$ sudo pip install paho-mqtt
$ sudo pip install flask
$ sudo pip install requests
$ sudo pip install blinkt
$ sudo pip install numpy
$ sudo pip install pyserial
```



### apt-get requirements
```bash
$ sudo apt-get install git
$ sudo apt-get install python
$ sudo apt-get install python-dev
$ sudo apt-get install python-blinkt
$ sudo apt-get install nginx
```

## /etc/rc.local scripts (append above `exit 0`)

lidar-gear:

```bash
~pi/git/FRC-2017/boot/lidar-gear-startup.sh
```
camera-gear:
  
```bash
~pi/git/FRC-2017/boot/camera-gear-startup.sh
```

camera-rope:
  
```bash
~pi/git/FRC-2017/boot/camera-rope-startup.sh
```

lcd1:

```bash
~pi/git/FRC-2017/boot/lcd1-startup.sh
```


