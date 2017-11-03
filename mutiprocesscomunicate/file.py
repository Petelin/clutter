#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import os
from mutiprocesscomunicate import gen_data, data_size


def send_data_task(file_name):
    # 是否同步写入磁盘, 如果同步写进去, 慢的一 b, 牛逼的是, 不同步写进去, 也可以读.操作系统厉害了.
    # os.sync()
    with open(file_name, 'wb+') as fd:
        for i in range(data_size):
            fd.write(gen_data(1))
            fd.write('\n'.encode('ascii'))
            # end EOF
        fd.write('EOF'.encode('ascii'))
    print('send done.')


def get_data_task(file_name):
    offset = 0
    fd = open(file_name, 'r+')
    i = 0
    while True:
        data = fd.read(1024)
        offset += len(data)
        if 'EOF' in data:
            fd.truncate()
            break
        if not data:
            fd.close()
            fd = None
            fd = open(file_name, 'r+')
            fd.seek(offset)
            continue
    print("recv done.")


if __name__ == '__main__':
    import multiprocessing

    pipe_out = pipe_in = 'throught_file'
    p = multiprocessing.Process(target=send_data_task, args=(pipe_out,), kwargs=())
    p1 = multiprocessing.Process(target=get_data_task, args=(pipe_in,), kwargs=())

    p.daemon = True
    p1.daemon = True
    import time

    start_time = time.time()
    p1.start()
    import time

    time.sleep(0.5)
    p.start()
    p.join()
    p1.join()
    import os
    print('through file', data_size / (time.time() - start_time), 'KB/s')
    open(pipe_in, 'w+').truncate()
