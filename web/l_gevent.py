from gevent import monkey
monkey.patch_all()
from timeit import Timer
from urllib import request
import time
import gevent
import requests
url = "http://www.taobao.com"


def run1():
    for i in range(100):
        requests.get(url).status_code

def run2():
    def download():
        requests.get(url).status_code

    ls = [gevent.spawn(download) for i in range(100)]
    gevent.joinall(ls)

if __name__ == '__main__':
    t = Timer(stmt="run1();", setup="from __main__ import run1")
    print('for loop', t.timeit(2))

    t = Timer(stmt="run2();", setup="from __main__ import run2")
    print('requests', t.timeit(2))
