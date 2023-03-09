# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/2 15:46 
# @Author  : mtl
# @Desc    : ***
# @File    : at.py
# @Software: PyCharm
import functools
import threading
import time

import serial
from config import Config
from utils.myLogging import DtuLogger

logger = DtuLogger(name='atlogger', file='at.log')
output = DtuLogger(name='output', file='output.log')

command = {
    "pdd": "AT+CGACT=1,1",
    "qiopen": f'AT+QIOPEN=1,0,"TCP","{Config.host}",{Config.port},0,0',
    "qistate": "AT+QISTATE=?",
    "qisend": "AT+QISEND=0,%s",
    "qiclose": "AT+QICLOSE=0",
    "qird": "at+qird=0,%s"
}


class AT:
    _instance_lock = threading.Lock()

    def __new__(cls):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super().__new__(cls)
                    cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.conn = None
        self.serial = None
        self.heart_data = Config.heartbeat_data
        self.heart_data_length = len(self.heart_data)

    def connect(self):
        if self.serial and not self.serial.is_open:
            logger.error("连接关闭，重新连接！")
            self.serial = None
        if not self.serial:
            try:
                self.serial = serial.Serial(Config.serial_device, Config.serial_bandrate, timeout=Config.serial_timeout)
                logger.info("连接成功")
                self.__send_command(command["pdd"])
            except Exception as e:
                logger.error(e)
        while True:
            r = self.__send_command("AT+CPIN?\r\n")
            logger.debug(f"检查SIM卡状态->{r}")
            if "+CPIN: READY" in r:
                break
            logger.error("未检测到SIM卡或SIM卡未就绪，请检查！")
            time.sleep(5)

        while True:
            r = self.__send_command("AT+CREG?\r\n")
            logger.debug(f"检查网络状态->{r}")
            if "+CREG: 0,1" in r or "+CREG: 0,5" in r:
                break
            logger.error("未检测到网络，请检查SIM卡和网络状态！")
            time.sleep(5)

        self.__connect_socket()

    def __connect_socket(self):
        r = self.__send_command(command["qistate"])
        logger.debug(f"qistate->{r}")
        if "OK" == r:
            return
        self.__send_command(command["qiopen"])

    @staticmethod
    @functools.lru_cache()
    def __get_instance():
        return AT()

    def __send_command2(self, command, ln=True, retry_max=3):
        with self.__get_instance()._instance_lock:
            if not command:
                return "ERROR"
            if ln:
                command += "\r\n"
            self.serial.flushInput()  # 清空缓冲区
            self.serial.write(str(command).encode('utf-8'))
            start_time = time.time()
            response = ""
            data = "1"
            while not response and data and time.time() - start_time < 5:
                logger.debug(f"发送命令-> {str(command).encode('utf-8')},等待回复中！")
                data = self.serial.readline().decode('utf-8', errors='ignore').strip()
                response += data
                if response:
                    logger.debug(f"发送命令-> {str(command).encode('utf-8')},回复-> {response}")
            if "ERROR" in response:
                logger.debug(f"发送命令-> {str(command).encode('utf-8')},ERROR！")
                self.connect()
            output.info(f"指令->{command},输出->{response}")
            return response

    def __send_command(self, command, ln=True, retry_max=3):
        with self.__get_instance()._instance_lock:
            if not command:
                return "ERROR"
            if ln:
                command += "\r\n"
            retry_count = 0
            response = []
            while retry_count < retry_max and not response:
                self.serial.flushInput()  # 清空缓冲
                self.serial.write(command.encode())
                while True:
                    line = self.serial.readline().decode().strip()
                    if line:
                        response.append(line)
                    else:
                        break
                retry_count += 1
                time.sleep(Config.retry_interval)
            result = '\n'.join(response)
            logger.info(f"{command.strip()} -> {result}")
            output.info(f"{command.strip()} -> {result}")
            return result

    def send_heart(self):
        result = self.__send_command(command["qisend"] % self.heart_data_length)
        if "ERROR" in result:
            self.connect()
        self.__send_command(self.heart_data, ln=False)

    def send_data(self, data=""):
        self.__send_command(command["qisend"] % len(data))
        if "ERROR" in result:
            self.connect()
        return self.__send_command(data, ln=False)

    def get_data(self, length=100):
        return self.__send_command(command["qird"] % length)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with self.__get_instance()._instance_lock:
            if self.serial:
                self.serial.close()
                self.serial = None

    def __del__(self):
        with self.__get_instance()._instance_lock:
            if self.serial:
                self.serial.close()
                self.serial = None


def send_data(data):
    at = get_at()
    return at.send_data(data)


def send_heart():
    at = get_at()
    return at.send_heart()


def get_data():
    at = get_at()
    return at.get_data()


@functools.lru_cache()
def get_at():
    at_inst = AT()
    at_inst.connect()
    return at_inst
