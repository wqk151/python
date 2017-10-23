#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading2.py
@time:2017/4/20 0020 10:34
"""
# 创建一个Thread的实例，传给它一个可调用的类对象/实例。重写call方法
import threading
import time
def sleep_second(nes):
    print 'second++start',time.ctime()
    time.sleep(nes)
    print 'second++stop',time.ctime()
def sleep_five(nes):
    print 'five--start',time.ctime()
    time.sleep(nes)
    print 'five--stop',time.ctime()

class ThreadFunc(object):
    def __init__(self,func,args,name=''):
        self.name = name
        self.func = func
        self.args = args
    def __call__(self,):
        apply(self.func,self.args)

def main():
    print 'main --start: ',time.ctime()
    threads = []
    t1 = threading.Thread(target=ThreadFunc(sleep_second,(2,)))
    # 简化为：target=ThreadFunc() --(把类当函数类使用) ，这样写法就调用了call方法，里面的参数传递给apply方法。
    threads.append(t1)
    t2 = threading.Thread(target=ThreadFunc(sleep_five,(5,)))
    threads.append(t2)
    for t in range(len(threads)):
        threads[t].start()
    for i in range(len(threads)):
        threads[i].join()

    print 'main --done: ',time.ctime()

if __name__ == '__main__':
    main()