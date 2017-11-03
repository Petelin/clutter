#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/10/31 19:55
#   Desc    :   用asynic实现的
import socket
import selfayncio

import asyncio
asyncio.get_event_loop()
loop = selfayncio.get_event_loop()


async def create_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', port))
    server.listen()
    server.setblocking(False)
    while True:
        client, info = await loop.sock_accept(server)
        print("connect from", info, flush=True)
        loop.create_task(http_handler(client))


async def http_handler(client):
    with client:
        try:
            while True:
                data = await loop.sock_recv(client, 1024)
                if data == b'' or data[-4:] == b'\r\n\r\n':
                    break
            await loop.sock_sendall(client, b"""HTTP/1.1 200 OK
    Content-Type: text/html
    Connection: Closed

    <h1>Hello, World!</h1>
    """)
        except:
            pass

async def echo_handler(client):
    with client:
        while True:
            data = await loop.sock_recv(client, 1024)
            if not data:
                break
            await loop.sock_sendall(client, data)
    print("connection closed")


loop.create_task(create_server(8080))
print('start server...')
loop.run_forever()
