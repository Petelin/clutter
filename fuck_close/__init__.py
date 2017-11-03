#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/10/27 10:30
#   Desc    :   ...


class Container(object):
    def __init__(self, n=100):
        from bitarray import bitarray
        self.plant = bitarray(n)
        print(self.plant.buffer_info())
        self.total = n

    def append(self, value):
        self.plant.append(value)

    def pop(self):
        self.plant.pop(0)

    def save_record(self, value):
        self.plant.append(value)
        self.plant.pop(0)

    def get_rate(self):
        return self.plant.count(0) / self.total


class FuseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.container = Container()
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if self.container.get_rate() > 0.5:
            return ""
        try:
            response = self.get_response(request)
            self.container.save_record(1)
        except:
            self.container.save_record(0)
            raise
        return response
