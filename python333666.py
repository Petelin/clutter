#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   16/11/29 15:08
#   Desc    :   python 3.6 体验

name = "zhang"


# print(f"my name is {name}")

class p():
    def __get__(self, instance, owner):
        print("get", instance, owner)
        return self.name

    def __set__(self, instance, value):
        print("set", instance, value)
        self.name = "append___" + value

    def __set_name__(self, instance, name):
        print("set_name", id(self), instance, name)
        self.name = name


# class User():
#     name2 = name = p()
#     age = p()


# u = User()
# u.name = "zhang san"
# print(u.name)
# u.age = "19"
# print(u.age)



class QuestBase():
    def __init_subclass__(self, *args, **kwargs):
        print("init subclass", args, kwargs)

        super(QuestBase, self).__init_subclass__()


class Quest(QuestBase, haha=2):
    pass


from pathlib import Path

p = Path("type_class.py")
with open(p) as f:
    print(f.readline())
