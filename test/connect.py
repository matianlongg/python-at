# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/2 15:43 
# @Author  : mtl
# @Desc    : ***
# @File    : connect.py
# @Software: PyCharm
import time

from Internet.at import send_heart, get_data
from utils.myLogging import DtuLogger

logger = DtuLogger(name='connectLogger', file='connect.log')

while True:
    send_heart()
    time.sleep(3)
    # logger.debug(get_data())