#!/usr/bin/env python
class Type(object):
    print("运行到", "Type")

    def __init__(self, type_):
        print("set type", type_)

        self.type_class = type_

    def vaild(self, value):
        return isinstance(value, self.type_class)


class TypeCheckMeta(type):
    print("运行到", "TypeCheckMeta")

    def __new__(cls, name, bases, dict, **kwargs):
        print("元类 __new__", name, bases, dict, kwargs)
        inst = super(TypeCheckMeta, cls).__new__(cls, name, bases, dict)
        inst._fileds = {}
        for k, v in dict.items():
            if isinstance(v, Type):
                inst._fileds.setdefault(k, v)
        return inst

    def __init__(cls, *args, **kwargs):
        print("元类 __init__")
        super(TypeCheckMeta, cls).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print("元类 __call__")
        return super(TypeCheckMeta, self).__call__(*args, **kwargs)


class Test(metaclass=TypeCheckMeta):
    print("运行到", "Test")
    name = Type(str)
    age = Type(int)

    def __init_subclass__(self, p, **kwargs):
        print("__init_subclass__", **kwargs)
        super(Test, self).__init_subclass__(**kwargs)

    def __new__(cls, *args, **kwargs):
        print("类 __new__")
        print(args, kwargs)
        return super(Test, cls).__new__(cls, *args, **kwargs)

    def __setattr__(self, key, value):
        print("类 __setattr__")
        if key in self._fileds:
            if not self._fileds[key].vaild(value):
                raise TypeError("invaild...")
        super(Test, self).__setattr__(key, value)

    def __init__(self, a):
        print("类 __init__")

    def __call__(self, *args, **kwargs):
        print("类 __call__")


class SubTest(Test, p=2):
    pass

# t = SubTest(1)
# print(t)
