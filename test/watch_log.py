# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/9 11:19 
# @Author  : mtl
# @Desc    : ***
# @File    : watch_log.py
# @Software: PyCharm


import queue
from utils.myLogging import DtuLogger

logger = DtuLogger(name='watchlogger', file='at.log')

while True:
    # 获取日志信息
    try:
        record = logger.queue.get(timeout=1)
    except queue.Empty:
        continue

    # 处理日志事件的代码
    logger.handle_watch_output(record)