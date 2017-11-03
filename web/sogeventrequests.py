import gevent
from gevent import monkey
# monkey.patch_all()
import time

import requests
from urllib import request

def worker(url, use_urllib2=False):
    if use_urllib2:
        content = request.urlopen(url).read().lower()
    else:
        content = requests.get(url).content.lower()

urls = ['https://www.taobao.com']*5
def by_forloop():
    for url in urls:
        worker(url=url,use_urllib2=True)

def by_requests():
    jobs = [gevent.spawn(worker, url) for url in urls]
    gevent.joinall(jobs)

def by_urllib2():
    jobs = [gevent.spawn(worker, url, True) for url in urls]
    gevent.joinall(jobs)

if __name__=='__main__':
    from timeit import Timer
    t = Timer(stmt="by_forloop()", setup="from __main__ import by_forloop")
    print('by forloop(): %s seconds'%t.timeit(number=3))
    t = Timer(stmt="by_urllib2()", setup="from __main__ import by_urllib2")
    print('by urllib2: %s seconds'%t.timeit(number=3))
    t = Timer(stmt="by_requests()", setup="from __main__ import by_requests")
    print('by requests: %s seconds'%t.timeit(number=3))
