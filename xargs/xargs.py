#!/usr/bin/env python
import argparse

from multiprocessing import pool, cpu_count
import sys
import queue
import subprocess

task_queue = queue.Queue()
working_task = 0
stdin_close = False

def excute_task(bin_name, total_args, process_num):
    global working_task
    working_task += 1
    task_queue.put(bin_name + total_args)


def excute_xargs(command, args_num, process_num):
    total_args = []
    while True:
        line = sys.stdin.readline()
        if not line:
            if len(total_args) > 0:
                excute_task(command, total_args, process_num)
            global stdin_close
            stdin_close = True
            break
        total_args += line.split()
        if args_num == -1:
            excute_task(command, total_args, process_num)
            total_args = []
        elif len(total_args) >= args_num:
            for i in range(0, (len(total_args) // args_num) * args_num, args_num):
                excute_task(command, total_args[:args_num], process_num)
                total_args = total_args[args_num:]
    stop = True


def worker():
    while True:
        item = task_queue.get()
        r = subprocess.Popen(item)
        while r.poll() != 0:
            pass
        global working_task
        working_task -= 1


def create_wroker(pool):
    p1 = pool.Process(None, target=worker)
    p1.setDaemon(True)
    p1.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='xargs in python')
    parser.add_argument('x', metavar='X', type=str, nargs='+',
                        help='the argue')
    parser.add_argument('-n', type=int, dest='args_num', default=-1,
                        help='how many args')
    parser.add_argument('-P', type=int, dest='process_num', default=1,
                        help='process num run')

    args = parser.parse_args()

    worker_count = args.process_num if args.process_num != 0 else cpu_count() * 2

    pool = pool.ThreadPool(worker_count + 1)
    p = pool.Process(None, target=excute_xargs, args=(args.x, args.args_num, args.process_num))
    p.setDaemon(True)
    p.start()
    for i in range(worker_count):
        create_wroker(pool)
    while working_task != 0 or not stdin_close:
        pass
    exit(0)
