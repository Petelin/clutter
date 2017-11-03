#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/10/31 18:03
#   Desc    :   ...o


class A():
    def do(self, *args, **kwargs):
        self.operate(*args, **kwargs)

    def operate(self, *args, **kwargs):
        print(*args, **kwargs)


class B(A):
    def operate(self):
        print('done')

A().do('sdaf')
