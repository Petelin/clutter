#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/17 12:08
#   Desc    :   ...
import multiprocessing
import os
import socket

from mutiprocesscomunicate import gen_data, data_size


minissdpdSocket = '/tmp/m.sock'  # The socket for talking to minissdpd


def send_data_task():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            os.remove(minissdpdSocket)
        except OSError:
            pass

        server.bind(minissdpdSocket)

        server.listen(1)

        conn, _ = server.accept()
        with conn:
            for i in range(data_size):
                conn.send(gen_data(1))
            conn.shutdown(socket.SHUT_WR)
            print('send done.')


def get_data_task():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(minissdpdSocket)
        client.shutdown(socket.SHUT_WR)
        while True:
            data = client.recv(1024)
            if not data:
                break
        print("recv done.")


if __name__ == '__main__':
    p = multiprocessing.Process(target=send_data_task, args=(), kwargs=())
    p1 = multiprocessing.Process(target=get_data_task, args=(), kwargs=())

    p.daemon = True
    p1.daemon = True
    import time

    start_time = time.time()
    p.start()

    p1.start()
    p.join()
    p1.join()
    print('through socket', data_size / (time.time() - start_time), 'KB/s')
