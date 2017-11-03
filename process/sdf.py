#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/4/6 18:38
#   Desc    :   ...

from multiprocessing import Process
import os

def slow():
    os.system('''curl 'http://doctor.hotfix2.gmei.com/api/web/account/websocket/connect_string' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: Hm_lvt_9f7d89f8caa3b383d3bcea7e151135da=1488860274,1489982418,1490773078; _ga=GA1.2.1233465539.1482991127; sessionid=meogvw91nionvp3p90ck9iwtiqcbn4o6; ascle_session_key=k2039ycl10b2jpoiavoc3bq9i10ms2hw; csrftoken=AZ2gXd9xfc71VMN0Zd8A68y0F0EDgzEf' -H 'Connection: keep-alive' -H 'Referer: http://doctor.hotfix2.gmei.com/' --compressed''')


def fast():
    os.system('''curl 'http://doctor.hotfix2.gengmei.cc/api/web/ad/quick' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: _ga=GA1.2.1535577474.1469622791; ascle_session_key=zvji2nxplvfyfhnwhf6j3cyip7kjxdda; sessionid=t1s2ieavwv9xjpm4y67qj2j0gzarfbrm; csrftoken=5eJsMOV726W7yYo1SAZBsfrf89IQDrPG' -H 'Connection: keep-alive' -H 'Referer: http://doctor.hotfix2.gengmei.cc/' --compressed''')

r = []
for i in range(5):
    p = Process(target=slow)
    p.start()
    r.append(p)

for i in range(4):
    p = Process(target=fast)
    p.start()
    r.append(p)
[p.join() for p in r]



