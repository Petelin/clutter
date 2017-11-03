#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   16/11/4 14:06
#   Desc    :   ...

import inspect

_EMPTY_OBJECT = object()


def get_instance_name(self):
    rs = []
    lcs = inspect.currentframe().f_back.f_back.f_locals
    for k, v in lcs.items():
        if v is self:
            rs.append(k)
    return rs


class LazyAttrDict(dict):
    def __init__(self, query_dict, configs):
        self._configs = configs
        self._query_dict = query_dict

    def __getattr__(self, attr):
        config = self._configs.get(attr)
        if config is None:  # 若是没有写config直接返回值
            return self._query_dict.get(attr)
        default = config.get('default', _EMPTY_OBJECT)
        raw = self._query_dict.get(attr, default)
        if raw is _EMPTY_OBJECT:
            raise RuntimeError("fuckk")
        if raw is default:
            return default
        else:
            try:
                raw = config.get('access', str)(raw)
                return raw
            except:
                raise RuntimeError()

    def __getattribute__(self, item):
        print("getattribute:", item)
        caller_attribute = get_instance_name(self)
        print(caller_attribute)
        names = ("arg_post", "arg_get")
        if [n for n in names if n in caller_attribute]:
            return self.__getattr__(item)
        else:
            return object.__getattribute__(self, item)


    def __len__(self):
        return len(self._query_dict)

    def __iter__(self):
        return iter(self._query_dict)

    def some_method(self):
        print(self.get_instance_name())


def f1(): f2()


def f2():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print('caller name:', calframe[1][3])


POST = {
    "name": {
        "default": "hang"
    }
}

arg_post = LazyAttrDict({}, POST)
print(arg_post.copy)



asyncio