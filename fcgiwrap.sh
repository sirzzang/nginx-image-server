#!/bin/sh

spawn-fcgi -s /var/run/fcgiwrap.socket -a "0.0.0.0" -u 102 -g 102 -U 102 -G 102 -M 766 /usr/sbin/fcgiwrap
