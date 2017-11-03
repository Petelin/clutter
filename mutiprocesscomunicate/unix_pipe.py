#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/17 12:08
#   Desc    :   ...
import multiprocessing

from mutiprocesscomunicate import gen_data, data_size


def send_data_task(pipe_out):
    for i in range(data_size):
        pipe_out.send(gen_data(1))
    # end EOF
    pipe_out.send("")
    print('send done.')


def get_data_task(pipe_in):
    while True:
        data = pipe_in.recv()
        if not data:
            break
    print("recv done.")


if __name__ == '__main__':
    pipe_in, pipe_out = multiprocessing.Pipe(False)
    p = multiprocessing.Process(target=send_data_task, args=(pipe_out,), kwargs=())
    p1 = multiprocessing.Process(target=get_data_task, args=(pipe_in,), kwargs=())

    p.daemon = True
    p1.daemon = True
    import time

    start_time = time.time()
    p1.start()
    p.start()
    p.join()
    p1.join()
    print('through pipe', data_size / (time.time() - start_time), 'KB/s')
