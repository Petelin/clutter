#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/10/25 15:28
#   Desc    :   use two stack to sort


def sort(stack_a:list):
    buffer = []
    while 1:
        try:
            tmp = stack_a.pop()
            while 1:
                if len(buffer) > 0 and buffer[-1] < tmp:
                    stack_a.append(buffer.pop())
                else:
                    break
            buffer.append(tmp)
        except:
            break
    return buffer
import random
wait_sort_arr = list(range(10))
random.shuffle(wait_sort_arr)
print(wait_sort_arr)
print(sort(wait_sort_arr))
