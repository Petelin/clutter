#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/3/10 15:41
#   Desc    :   ...

# -*- coding=utf-8 -*-
from gevent import monkey; monkey.patch_all()
import requests
from multiprocessing import Process
import gevent
import time
import os

pids = []


def fetch(url):
    try:
        s = requests.Session()
        r = s.get(url, timeout=6)  # 在这里抓取页面
        pid = os.getpid()
        print(pid, 'done', url)
    except Exception as e:
        print(e)


def process_start(tasks):
    gevent.joinall(tasks, timeout=10)  # 使用协程来执行


def task_start(filepath, flag=2):  # 每10W条url启动一个进程
    with open(filepath, 'r') as reader:  # 从给定的文件中读取url
        url = reader.readline().strip()
        task_list = []  # 这个list用于存放协程任务
        i = 0  # 计数器，记录添加了多少个url到协程队列
        while url != '':
            i += 1
            task_list.append(gevent.spawn(fetch, url))  # 每次读取出url，将任务添加到协程队列
            if i == flag:  # 一定数量的url就启动一个进程并执行
                print(task_list)
                p = Process(target=process_start, args=(task_list,))
                p.start()
                p.join()
                print('--*-- start process id: %d --*--' % p.pid)
                pids.append(p.pid)
                task_list = []  # 重置协程队列
                i = 0  # 重置计数器
            url = reader.readline().strip()


if __name__ == '__main__':
    task_start('./testData.txt')  # 读取指定文件
    print(pids)
    print('done all----------------')

