#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   zhangxiaolin
#   E-mail  :   petelin1120@gmail.com
#   Date    :   16/11/4 14:49
#   Desc    :   ...

"""
唯一一个限制字典:不能存以 `_` 开头的key

通过`_func`访问原生方法.
"""
from collections.abc import Mapping
import inspect

_EMPTY_OBJECT = object()


def get_instance_name(self):
    rs = []
    lcs = inspect.currentframe().f_back.f_back.f_locals
    for k, v in lcs.items():
        if v is self:
            rs.append(k)
    return rs


def get_code_line(self):
    lcs = inspect.currentframe()
    calframe = inspect.getouterframes(lcs, 1)
    codes = calframe[2][4][0].strip()
    return codes


class LazeAttrDict(Mapping):
    def __init__(self, query_dict=None, configs=None):
        self._query_dict = query_dict or {}
        self._configs = configs or {}

    def __getattribute__(self, attr):
        caller = get_instance_name(self)
        if "self" in caller:
            return super(LazeAttrDict, self).__getattribute__(attr)
        else:
            # 判断是否是**keys, 如果是**,那么是方法调用
            if attr == "keys":
                code_line = get_code_line(self)
                if ("**{}".format(caller[0]) in code_line):
                    return self.keys

            if attr.startswith("_") and getattr(self, attr[1:]):
                return getattr(self, attr[1:])
            return self.__getitem__(attr)


    def __len__(self):
        result = set(self._query_dict.keys()) | set(self._configs.keys())
        return len(result)

    def __getitem__(self, attr):
        config = self._configs.get(attr)
        if config is None:  # 若是没有写config直接返回值
            r = self._query_dict.get(attr)
            if r:
                return r
            else:
                raise KeyError
        default = config.get('default', _EMPTY_OBJECT)
        raw = self._query_dict.get(attr, default)
        if raw is _EMPTY_OBJECT:
            raise RuntimeError()
        if raw is default:
            return default
        else:
            try:
                raw = config.get('access', str)(raw)
                return raw
            except:
                raise RuntimeError()

    def __iter__(self):
        for i in self._query_dict.keys():
            yield i
        for i in self._configs.keys():
            if i not in self._query_dict.keys():
                yield i


if __name__ == '__main__':
    arg_post = LazeAttrDict(
        {'a': 2, 'keys': 'kk'},
        {
            'a': {
                'access': str
            },
            'b': {
                'default': 'default',
            },
            'items': {
                'default': [1, 2]
            },
            'values': {
                'default': 'vvv'
            }

        })

    assert arg_post.a == "2"
    assert arg_post.b == "default"
    assert arg_post.items == [1, 2]
    assert arg_post.values == "vvv"
    assert arg_post.keys == "kk"

    print("items方法")
    for k, v in arg_post._items():
        print('\t', k, v)

    print("keys方法")
    print("\t", list(arg_post._keys()))
    print("**dict方法\n\t", dict(**arg_post))
