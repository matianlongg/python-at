# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/2 15:20 
# @Author  : mtl
# @Desc    : ***
# @File    : __init__.py.py
# @Software: PyCharm
# import serial
import time
import socket
# from Config import Config
for i in b"AT+CFUN=1,1\r\n":
    print(i)

# print(Config.heartbeat)
# Configure serial port
# ser = serial.Serial('/dev/ttyUSB3', 115200, timeout=1)
#
# class AtJob():
