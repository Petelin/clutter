#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/16 11:16
#   Desc    :   ...
import socket
import signal
from time import sleep


def handler(signum, frame):
    print('Signal handler called with signal', signum)


def client(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client.connect(('localhost', port))
    # sleep(10)
    print('try to send')
    r = client.send(b'sdffffffffffffffffffffffffffffff')
    print(r)
    r = client.send(b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(r)
    client.close()
    print('close...')
    # client.shutdown(socket.SHUT_RDWR)
    # print(client.recv(1024))

if __name__ == '__main__':
    signal.signal(signal.SIGPIPE, handler)
    # signal.signal(signal.SIGKILL, handler=handler)
    client(5554)
    # signal.alarm(0)

