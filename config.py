# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/2 15:23 
# @Author  : mtl
# @Desc    : ***
# @File    : Config.py
# @Software: PyCharm

class Config:
    host = "27.188.73.44"
    port = 19196

    # 心跳
    heartbeat_data = "bbb"
    heartbeat_interval = 60

    # serial
    serial_device = "/dev/ttyUSB3"
    serial_bandrate = 115200
    serial_timeout = 0.1

    watch_list = [
        ('quectel-CM', '/usr/sbin/quectel-CM &')
    ]

    retry_interval = 0.5