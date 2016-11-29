#!/bin/sh

IP=$(ifconfig eth|grep -w 'inet' | awk '{print $2}')
echo 'you are in '$IP>/var/www/html/index.html
python /opt/reg.py
