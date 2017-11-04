## 实现了-n 和 -P 功能的xargs

1. 用时
边开发边测试了一个半小时, 确认完成之后测试了10分钟

2. 遇到的问题:  
    1.基本上每个模块都需要查一下文档,虽然之前用过很多次这些包了.  
    2.ThreadPool 被理解错误了, 这个主要是配合map这种方法来用, 自己提交task的话,需要自己增加process数量.
改了一个bug: 退出条件原来写的很复杂, 判断好几个队列是不是空, 也没能保证退出的时候没有任务在执行

3. 问题
pdf文档放家了,可能一些要求没考虑到, 另外基本没做异常处理, 返回值什么的. 代码的话是用函数风格写的, 如果功能更多的话, 应该组织成类会更好.

```
>./xargs.sh -h
usage: xargs.py [-h] [-n ARGS_NUM] [-P PROCESS_NUM] X [X ...]

xargs in python

positional arguments:
  X               the argue

optional arguments:
  -h, --help      show this help message and exit
  -n ARGS_NUM     how many args
  -P PROCESS_NUM  process num run
```

-n: 指定多少个参数,开始执行命令

1. 测试-n可以用
```
$./xargs.py -n 2 echo                             *[master] 
a b  #输入
a b
c  #输入
d  #输入
c d
e f g #输入
e f
ctrl+c
```
2. 测试-p可以用
```
$ echo 2 2 2 2 | ./xargs.py -n 1 -P 2 ./sleep.sh  
sleep 2
sleep 2
# 两秒之后
sleep 2
sleep 2
# 两秒后退出
```
```
$ echo 2 2 2 2 | ./xargs.py -n 1 -P 0 ./sleep.sh 
sleep 2
sleep 2
sleep 2
sleep 2
# 两秒后退出
```
