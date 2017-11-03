import gevent
from gevent import monkey, Greenlet
monkey.patch_all()

from gevent.pool import Pool
import requests


def down():
    url = 'http://www.sina.com.cn'
    print(len(requests.get(url).content))


def buildurl():
    while True:
        gevent.sleep(0)  # 添加这条后才可以切换到其它任务
        Greenlet.spawn(down)
        print(u"检测下载地址")  # 这里可以动态添加下载任务


Greenlet.spawn(buildurl)
loop = gevent.core.loop()
loop.run()
