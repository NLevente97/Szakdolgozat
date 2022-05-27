#!/bin/sh

# shell script that launches the python application on boot up using crontab
# sudo crontab -e and add the following line:
# @reboot sh /home/pi/Desktop/szakdolgozat/launch.sh >/home/pi/Desktop/szakdolgozat/logs/robot.log 2>&1

cd /home/pi/Desktop/szakdolgozat/
python3 -u /home/pi/Desktop/szakdolgozat/robotcontroller.py
cd /