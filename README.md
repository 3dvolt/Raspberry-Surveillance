# Raspberry-Surveillance
<img src="https://raw.githubusercontent.com/3dvolt/Raspberry-Surveillance/master/Render/2.png"/>
Raspberry camera Surveillance is a portal with opencv and MYSQL

I use HackerShackOfficial's project as starting point
https://github.com/HackerShackOfficial/Smart-Security-Camera

The Bootstrap Template used is: SB Admin 2
https://github.com/BlackrockDigital/startbootstrap-sb-admin-2

## Features:

* Database access(credential,login page and access tracking)
* Live Streaming 
* 2 axis (Pan Tilt) movement 
* small and light, only one cable needed (power)
* Computer Vision (Identification and notify)
* Email and password stored in database
* Web Pages responsive and Mobile friendly

## ToDo:

* Autonomous movement(with 2 servo, when OpenCV detected a person, the camera move autonomously)
* Add box with the last image captured
* stored all the image captured in the database



## Getting Started

Hardware required:

* Raspberry pi 3 or higher
* 2 servo 9g
* Raspberry Camera
* 3d printed parts
* power supply 5V 2A

Software used:

* Python 3
* Mysql server
* Flask
* OpenCV


## Install OpenCV
follow this 
https://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/

```
source ~/.profile
workon cv
```
## Assembly

<img src="https://raw.githubusercontent.com/3dvolt/Raspberry-Surveillance/master/Render/1.png"/>

## Create Database

install mysql
```

```

## Start Program
Write inside the folder
```
sudo python3 START.py
```

