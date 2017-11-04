## 实现了-n 和 -P 功能的xargs

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
