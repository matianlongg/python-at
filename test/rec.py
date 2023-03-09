# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2023/3/6 11:40 
# @Author  : mtl
# @Desc    : ***
# @File    : rec.py
# @Software: PyCharm


# -*- coding:utf-8 -*-
import gevent
import sys
sys.path.append('../')
from gevent import socket, monkey
monkey.patch_all()

def server(port):
    try:
        s = socket.socket()
        s.bind(('0.0.0.0', port))
        s.listen(600)
        while True:
            cli, addr = s.accept()
            gevent.spawn(handle_request, cli)
    except KeyboardInterrupt as e:
        print(e)

'''
数据接收
'''

def handle_request(conn):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("client has been closed...")
                conn.shutdown(socket.SHUT_RD)
                conn.close()
            else:
                conn.send("接收到数据返回".encode())
                print('success ->',data)
    except OSError as e:
        print("client has been closed")
    except Exception as ex:
        print(ex)
    finally:
        '''
        释放资源
        '''
        conn.close()
        r.connection_pool.disconnect()
        r.close()

'''
程序入口
'''
if __name__ == '__main__':
    server(13384)
