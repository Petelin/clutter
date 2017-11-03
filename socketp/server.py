#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/16 11:16
#   Desc    :   ...
import socket
from time import sleep


def server(port):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    srv.bind(("", port))
    srv.listen(5)
    while True:
        print("等待链接...")
        client, addr = srv.accept()
        sleep(10)
        # client.close()
        client.shutdown(socket.SHUT_RD)
        print('close')
        # client.shutdown(socket.SHUT_RD)
        # while True:
        #     data = client.recv(1024)
        #     if data is None or data == b'':  # remote user close
        #         # client.close()  # we also close
        #         client.send(b'sdfsd')
        #         print('done--')
        #         break
        #     else:
        #         print('recieve', data)

server(5554)
