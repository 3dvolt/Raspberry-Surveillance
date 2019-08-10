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

## Hardware required:

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


## Install OpenCV:
follow this 
https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/


## 3d Print and Assembly

<img src="https://raw.githubusercontent.com/3dvolt/Raspberry-Surveillance/master/Render/1.png"/>

print the .stl file
## Camera

enable the raspicamera

```
sudo raspi-config
interface camera enable

```

## pip dependencies

pip install

```
imutils
flask
picamera[array]
Flask-BasicAuth==0.2.0
pip install mysql-connector
flask_mysqldb
RPi.GPIO
```

## Create Database

install mysql
```
sudo apt-get install mariadb-server-10.0 --fix-missing
sudo mysql
```
create database and table using .sql file

Edit the email and password.

## Start Program

```
source ~/.profile
workon cv
```

Write inside the main folder
```
sudo python3 START.py
```
default password root root

