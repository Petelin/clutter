#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/9/27 11:18
#   Desc    :   ...
ctx = []

def bind():
    def inner(f):
        ctx.append(f)
        return f
    return inner

@bind()
def hello(a):
    print('a' + a)

@bind()
def hello(a):
    print('b' + a)

if __name__ == '__main__':
    hello('0000000')
    print(ctx)
