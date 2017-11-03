import threading
import time

import os
import _thread

import multiprocessing

num = 0


def test1(*data):
    print(_thread.get_ident(), os.getpid(), os.getppid())
    num = data[0]
    while True:
        if num > 10:
            break
        time.sleep(1)
        num += 1
        print(num)


def test2(*data):
    print(data)
    i = data[0]
    t = threading.Thread(target=test1, args=(i,))
    t.start()
    # t.join()
    print("sub done", t.isDaemon())
    # return


pool = multiprocessing.Pool(processes=5)
results = []
for i in range(3):
    result = pool.apply_async(test2, (i,))
    print('send' + str(i))
    results.append(result)
pool.close()
pool.join()

# t = threading.Thread(target=test1, args=(1,))
# t.setDaemon(True)
# t.start()
# print('main_done', _thread.get_ident(), os.getpid(), os.getppid())
