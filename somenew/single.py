# coding=utf-8
# 测试utf-8编码
import os
import sys
import signal
import functools
from multiprocessing import Pool
from multiprocessing import Process, Pipe, Queue
import threading
import time
import subprocess


# class TimeoutError(Exception):
#     pass
#
#
# def timeout(seconds, error_message="time out"):
#     def decorated(func):
#         def _handle_timeout(signum, frame):
#             raise TimeoutError(error_message)
#
#         def wrapper(*args, **kwargs):
#             def son(conn):
#                 signal.signal(signal.SIGALRM, _handle_timeout)
#                 signal.alarm(seconds)
#                 result = func(*args, **kwargs)
#                 conn.put(result)
#             q = Queue()
#             p = Process(target=son, args=(q,))
#             p.daemon = True
#             p.start()
#             p.join()
#             return q.get(block=False)
#         return functools.wraps(func)(wrapper)
#     return decorated

from timeout_decorator import timeout

@timeout(1, use_signals=False)
def processNum(num):
    print(os.getpid())
    num_add = num + 1
    time.sleep(1)
    # return time.sleep
    # return str(threading.current_thread()) + ": " + str(num) + " → " + str(num_add)
    return 1


def main():
    pool = Pool(4)
    results = pool.map(processNum, range(4))
    pool.close()
    pool.join()
    # results = processNum(1)
    print(results)


if __name__ == "__main__":
    main()
