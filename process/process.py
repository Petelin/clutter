from multiprocessing import Process, Pool
import os
from time import sleep

sub = []
def info(title):
    print('title name:', title)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    while True:
        sub.append(title)
        print(sub)

def f(name):
    def enen():
        print("enen")
        sleep(100)
    info('function f')
    print('hello', name)
    p = Process(target=enen, args=())
    p.start()
    p.join()
    sleep(100)

if __name__ == '__main__':
    try:
        p = Process(target=info, args=('bob',))
        p.start()
        p2 = Process(target=info, args=('dit',))
        p2.start()
    except:
        print("end -----------------")



