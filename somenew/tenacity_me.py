#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/7/27 13:29
import random

import requests
from tenacity import retry, stop_after_delay

total = 1


@retry
def do_something_unreliable():
    global total
    while 1:
        if total > 3:
            break
        total += 1
        raise IOError("Broken sauce, everything is hosed!!!111one")
    return "Awesome sauce!"


@retry(stop=stop_after_delay(1))
# @retry
def stop_after_3_s():
    print('start')
    r = requests.get('https://google.com', timeout=3)
    return r.status

print(stop_after_3_s())


