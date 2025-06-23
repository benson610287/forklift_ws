# github使用教學
### 第一次使用
```base
#回到根目錄
$ cd $HOME
#clone工作區
$ git clone https://github.com/benson610287/forklift_ws.git --recursive
#進入工作區
$ cd forklift_ws/
#創建並進入分支
$ git checkout -b $your_brenchname
#加入新創的檔案
$ git add .
#提交檔案
$ git commit -m "version info"
#上傳至該分支的雲端
$ git push -u origin $your_brenchname
```
### 之後使用
```base
#進入分支
$ git chechout $your_brenchname
#加入新創的檔案
$ git add .
#提交檔案
$ git commit -m "version info"
#上傳至該分支的雲端
$ git push -u origin $your_brenchname
```
### shelf_pose_est package
```base
this node subscriber to '/camera/color/image_raw' topic for image.
Use "ros2 service call /toggle_aruco_detection interface/srv/Maincontroller '{enable: True}'" to activate aruco detection
Use "ros2 service call /toggle_aruco_detection interface/srv/Maincontroller '{enable: False}'" to deactivate aruco detection
```





# timda-mobile

2020 Designed
![Timda Mobile](https://i.imgur.com/93NvHtg.png)

## Hardwares Description
| Item          	| Item Model 	| Vendor        	| Description                                                                         	|
|---------------	|------------	|---------------	|-------------------------------------------------------------------------------------	|
| Motor         	| BLVM620KM  	| Orientalmotor 	| Weight: 6kg<br> Power: 200W<br> Constant Torque: 0.65Nm<br> Constant Speed: 3000rpm 	|
| Controller    	| BLVD20KM   	| Orientalmotor 	|                                                                                     	|
| Mecanum wheel 	|            	|               	| 6 inch

## Systems
OS: Ubuntu 18.04 bionic
ROS: noetic

## Installization and Setup
### Clone this repo and submodules
```base
$ cd $HOME
$ mkdir -p timda_mobile_ws/src && cd timda_mobile_ws
$ git clone https://github.com/benson610287/timda_mobile_noetic.git src/ --recursive
```
### Requirements
ROS Dependments:
```bash
$ sudo apt-get install ros-noetic-hector-sensors-description
$ sudo apt-get install ros-noetic-rosbridge-server ros-noetic-hector-slam ros-noetic-amcl ros-noetic-move-base ros-noetic-dwa-local-planner ros-noetic-map-server ros-noetic-teb-local-planner
## Hokuyo UTM30LX driver
$ sudo apt-get install ros-noetic-urg-node
```

Controller needs `libbmodbus`, please check out [mecanum](/src/mecanum)

Setup WoL client, we use raspberry pi 3 to send WoL signal to Intel NUC. Please check out [ping-pong client](/src/scripts) if needs.

There are udev files for hardware devices like Hokuyo lidar or RS485 adapter. Please check out [udev_rules](/src/udev_rules) and [systemd](/src/systemd) if needs.

We use nodeJS to setup http server. Please check out [webserver](/src/webserver) to install dependencies.

### Build
```base
$ cd $HOME/timda_mobile_ws
$ catkin_make
```
