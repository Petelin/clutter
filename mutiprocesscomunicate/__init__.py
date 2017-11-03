#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/17 12:08
#   Desc    :   ...
# through pipe 269667.7903995848 KB/s

data_size = 8 * 1024  # KB


def gen_data(size):
    onekb = "a" * 1024
    return (onekb * size).encode('ascii')
