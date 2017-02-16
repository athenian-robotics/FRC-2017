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
|**heading/degrees**        | Heading degrees (String)                                |
|**heading/calibration**    | Calibration status (String)                             |


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


## Listening to MQTT traffic

Listen to all user msgs with:

```bash
$ mosquitto_sub -h mqtt-turtle.local -t "#"
```

Listen to all system msgs with:

```bash
$ mosquitto_sub -h mqtt-turtle.local -t "\$SYS/#"
```

