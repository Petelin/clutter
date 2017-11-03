# coding: utf-8
import gevent
import os
from io import BytesIO
import urllib

import requests
from PIL import Image
from gevent import monkey;monkey.patch_all()



class BaseCode():
    # 验证码中，单个元素的图片名字
    BASEIDCODES = ["1", "2", "3", "b", "c", "m", "n", "v", "x", "z"]

    def __init__(self, absfilelocation):
        self.pixel_count = [[0] * 10 for x in range(12)]
        self.base_image = Image.open(absfilelocation)
        self.init_pixel_count()

    def init_pixel_count(self):
        for y in range(0, 12):
            for x in range(0, 9):
                self.pixel_count[y][x] = self.base_image.getpixel((x, y))

    def getpixel(self, x, y):
        return self.pixel_count[y][x]


class BaseCodeStore():
    pool = None

    @staticmethod
    def setup_basecode():
        path = os.path.dirname(__file__)
        BaseCodeStore.pool = {str(index): BaseCode(os.path.join(path, 'yzm', index) + '.bmp')
                              for index in
                              BaseCode.BASEIDCODES}

    @staticmethod
    def get_basecode(index):
        return BaseCodeStore.pool[index]


def get_idcode(**kwargs):
    """
        切图,和本地图片挨个像素对比,找出错误最少的.
    :param img_url: 验证码的路径
    :return:验证码字符串
    """
    #img_urs = "http://jwgl.btbu.edu.cn/verifycode.servlet"
    img_url = "http://jwgl.btbu.edu.cn"
    #content = urllib.request.urlopen(img_url, **kwargs).read()
    content = requests.get(img_url,**kwargs).content
    id_code = ""
    # 切图识别验证码中的数字
    return id_code

def run():
    for i in range(100):
        get_idcode()

def run2():
    ls = [gevent.spawn(get_idcode) for i in range(100)]
    gevent.joinall(ls)

BaseCodeStore.setup_basecode()
from timeit import Timer
if __name__ == "__main__":
    t = Timer('run()',setup='from __main__ import run')
    print(t.timeit(1))

    t = Timer('run2()',setup='from __main__ import run2')
    print("good",t.timeit(1))
