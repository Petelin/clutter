#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/14 13:55
#   Desc    :   ...

nes_file = "./Super Mario Bros (J).nes"


def read_nes():
    a = []
    with open(nes_file, 'rb') as fd:
        raw_bytes = fd.read(1024)
        while raw_bytes:
            a.append(raw_bytes)
            raw_bytes = fd.read(1024)

    return b''.join(a)


def draw_pixel(data):
    for i in range(8):
        left = data[i]
        right = data[i + 8]
        for j in range(8):
            c1 = (left >> (7 - j)) & 0x01
            c2 = (right >> (7 - j)) & 0x01
            pixel = (c1 << 1) + c2
            if pixel > 0:
                print('*', end='')
            else:
                print(' ', end='')


def draw_block(data, offset=0):
    for j in range(8):
        for i in range(8):
            slice = offset + (j * 8 + i) * 16
            draw_pixel(data[slice:slice + 16])


if __name__ == '__main__':
    raw_bytes = read_nes()
    # draw_block(raw_bytes, 32784)
