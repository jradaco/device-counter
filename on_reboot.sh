#!/bin/bash
source /home/pi/.profile 
workon cv 

sudo date 07070819.59
cd /home/pi/Desktop
python3 ESP32_Serial_1.py &
python3 ESP32_Serial_2.py

