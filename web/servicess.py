#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   16/11/1 19:10
#   Desc    :   ...


import select
import socket
from time import sleep


def send(s, keep_alive=True):
    status = "keep-alive" if keep_alive else "Close"
    body = "<h1> hello world </h1>"
    header = ["HTTP/1.1 200 OK",
              "Content-Length: {}".format(len(body)),
              "Connection: {}".format(status)]
    msg = "{}\r\n\r\n{}".format("\r\n".join(header), body)
    # print("\t发送数据：到", s.getpeername(), sep="")
    s.send(msg.encode())
    sleep(0)


def normal_service():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8080)
    server.bind(server_address)
    server.listen(10000)
    while True:
        s, client_address = server.accept()
        s.settimeout(5)
        print("新连接： ", client_address)
        while 1:
            try:
                data = s.recv(1024)
            except socket.timeout:
                print("改链接超时主动关闭,开启下一个")
                s.close()
                break
            if data:
                print("\t收到数据", data, "客户端：", s.getpeername())
                if data.decode().endswith("\r\n"):
                    send(s, True)
            else:
                print("\t关闭连接", s.getpeername())
                s.close()
                break


def select_service():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8080)
    server.bind(server_address)
    server.listen(10000)

    # select轮询发现有东西可以读出
    inputs = [server]
    # select轮询发现有东西可以写进去
    outputs = []
    message_queues = {}
    # select超时时间
    timeout = 0

    online_count = 0
    while True:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
        print("一次处理-----------------------")

        if not (readable or writable or exceptional):
            for s in inputs:
                if s is not server:
                    s.close()
                    inputs.remove(s)
            outputs.clear()
            continue
        # 循环可读事件
        for i, s in enumerate(readable):
            # 如果是server监听的socket
            print("readable序号 %d" % i)
            if s is server:
                # 同意连接
                connection, client_address = s.accept()
                print("\t新连接： ", client_address)
                connection.setblocking(0)
                # 将连接加入到select可读事件队列
                inputs.append(connection)
                # 新建连接为key的字典，写回读取到的消息
                online_count += 1
                print("\tonline_count:", online_count)
            else:
                # 不是本机监听就是客户端发来的消息
                data = s.recv(1024)
                if data:
                    print("\t收到数据：", data, "客户端：", s.getpeername())
                    if s not in outputs:
                        # 将读取到的socket加入到可写事件队列
                        outputs.append(s)
                else:
                    # 客户端会主动
                    # 不在从该socket输出东西
                    if s in outputs:
                        outputs.remove(s)
                    # 不在监听该socket
                    print("\t关闭连接", s.getpeername())
                    inputs.remove(s)
                    s.close()
                    online_count -= 1
        for i, s in enumerate(writable):
            print("writable序号 %d" % i)
            send(s, True)
            outputs.remove(s)

        for s in exceptional:
            print("异常连接：", s.getpeername())
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()


def epoll_service():
    EOL1 = b'\n\n'
    EOL2 = b'\n\r\n'
    response = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
    response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
    response += b'Hello, world!'

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('0.0.0.0', 8080))
    serversocket.listen(1)
    serversocket.setblocking(0)

    epoll = select.epoll()
    epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

    try:
        connections = {};
        requests = {};
        responses = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    try:
                        while True:
                            connection, address = serversocket.accept()
                            connection.setblocking(0)
                            epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                            connections[connection.fileno()] = connection
                            requests[connection.fileno()] = b''
                            responses[connection.fileno()] = response
                    except socket.error:
                        pass
                elif event & select.EPOLLIN:
                    try:
                        while True:
                            requests[fileno] += connections[fileno].recv(1024)
                    except socket.error:
                        pass
                    if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                        epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
                        print('-' * 40 + '\n' + requests[fileno].decode()[:-2])
                elif event & select.EPOLLOUT:
                    try:
                        while len(responses[fileno]) > 0:
                            byteswritten = connections[fileno].send(responses[fileno])
                            responses[fileno] = responses[fileno][byteswritten:]
                    except socket.error:
                        pass
                    if len(responses[fileno]) == 0:
                        epoll.modify(fileno, select.EPOLLET)
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                elif event & select.EPOLLHUP:
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
    finally:
        epoll.unregister(serversocket.fileno())
        epoll.close()
        serversocket.close()



if __name__ == "__main__":
    # normal_service()

    # select_service()

    epoll_service()
