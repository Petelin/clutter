#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/11/1 20:00
#   Desc    :   ...
import types
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
from collections import deque


@types.coroutine
def wait_write(socket):
    yield 'wait_write', socket


@types.coroutine
def wait_read(socket):
    yield 'wait_read', socket


class Loop(object):
    def __init__(self):
        self.current_task = None
        self.ready = deque()
        self.selector = DefaultSelector()

    async def sock_recv(self, socket, n):
        await wait_read(socket)
        return socket.recv(n)

    async def sock_sendall(self, socket, data):
        try:
            n = socket.send(data)
        except:
            await wait_write(socket)
            n = 0
        while True:
            n = socket.send(data[n:])
            if not data[n:]:
                break

    async def sock_accept(self, socket):
        await wait_read(socket)
        return socket.accept()

    def run_forever(self):
        while True:
            while not self.ready:
                events = self.selector.select()
                _temp_server = None
                for key, _ in events:
                    if key.data.__name__ == 'create_server':
                        _temp_server = key.data
                    else:
                        self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)
                if _temp_server:
                    self.ready.append(_temp_server)
            print(self.ready)
            while self.ready:
                self.current_task = self.ready.popleft()
                try:
                    op, *args = self.current_task.send(None)
                    getattr(self, op)(*args)
                except StopIteration:
                    pass

    def wait_write(self, socket):
        self.selector.register(socket, EVENT_WRITE, self.current_task)

    def wait_read(self, socket):
        self.selector.register(socket, EVENT_READ, self.current_task)

    def create_task(self, co):
        self.ready.append(co)

__loop = Loop()


def get_event_loop():
    return __loop
