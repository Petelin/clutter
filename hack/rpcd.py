#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   17/8/29 16:45
#   Desc    :   翻翻遗...
import functools
import weakref

_proxy_object_map = weakref.WeakKeyDictionary()


class DynamicScopeReleaseHandle(functools.partial):
    __slots__ = ()

    def __new__(cls, dynamic_scope_pop, key, handle):
        print('b')
        return functools.partial.__new__(cls, dynamic_scope_pop, key, handle)

    def __init__(self, *args, **kwargs):
        print('i')
        pass

    def __enter__(self):
        print('c')
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('exit')
        self()


def promis(new_f, *o_args, **o_kwargs):
    def __inner(*args, **kwargs):
        return new_f(*args, *kwargs, *o_args, **o_kwargs)

    return __inner



class ProxyObject(object):
    __slots__ = '__weakref__'

    def __init__(self, getter):
        assert callable(getter)
        _proxy_object_map[self] = getter

    def __getattribute__(self, item):
        if item[0] == '_':
            raise AttributeError('ProxyObject reject attribute: {}'.format(item))
        getter = _proxy_object_map[self]
        return getattr(getter(), item)

    def __iter__(self):
        getter = _proxy_object_map[self]
        return getter().__iter__()

    def __getitem__(self, item):
        getter = _proxy_object_map[self]
        return getter()[item]

    def __setitem__(self, key, value):
        getter = _proxy_object_map[self]
        getter()[key] = value

    def __delitem__(self, key):
        getter = _proxy_object_map[self]
        del getter()[key]


def unproxy(o):
    assert isinstance(o, ProxyObject)
    getter = _proxy_object_map[o]
    return getter()


if __name__ == '__main__':
    def pop(key, handler):
        print(key, handler)


    ProxyObject(pop)
    print(_proxy_object_map.keyrefs())
    promis(pop, handler='a')('b')
