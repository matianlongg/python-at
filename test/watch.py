# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/6 15:02 
# @Author  : mtl
# @Desc    : ***
# @File    : watch.py
# @Software: PyCharm
import os
from config import Config
from utils.myLogging import DtuLogger
import subprocess


logger = DtuLogger(name='watchlogger', file='at.log')


def is_process_running(process_name):
    cmd = 'ps aux | grep ' + process_name + ' | grep -v grep | wc -l'
    output = os.popen(cmd).read()
    if int(output.strip()) > 0:
        return True
    else:
        return False


watch_list = Config.watch_list
for task in watch_list:
    process, instructions = task
    if not is_process_running(process):
        logger.error(f"{process}未运行！")
        result = subprocess.run(instructions, shell=True, text=True)
        logger.info(f"{process}执行完毕！")