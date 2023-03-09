# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/2 16:56 
# @Author  : mtl
# @Desc    : ***
# @File    : logging.py
# @Software: PyCharm

import logging
import logging.handlers
import multiprocessing


class DtuLogger:
    def __init__(self, name=__name__, level=logging.DEBUG, file='internet.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s')
        if file:
            handler = logging.FileHandler(file)
        else:
            handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # self.queue = multiprocessing.Queue(-1)
        #
        # queue_handler = logging.handlers.QueueHandler(self.queue)
        # self.logger.addHandler(queue_handler)
        #
        # queue_listener = logging.handlers.QueueListener(self.queue, handler)
        # queue_listener.start()

    @classmethod
    def handle_watch_output(cls, record):
        # 处理日志事件的代码
        self.logger.debug(f"cls-{cls}-record->{record}")

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)