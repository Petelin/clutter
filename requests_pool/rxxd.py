#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/9/22 18:33
#   Desc    :   ...

import logging

import requests

logging.basicConfig(level=logging.DEBUG)

url_list = [
    'http://baidu.com'
]
if __name__ == '__main__':
    s = requests.session()
    for i in range(10):
        print(i, end=',')
        s.get('http://httpbin.org/')


