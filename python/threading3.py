#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading3.py
@time:2017/4/20 0020 11:36
"""
# 三：从thread派生出一个子类，创建一个这个子类的实例，重写run方法
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

class myThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
    def run(self):
        apply(self.func,self.args)

def main():
    print 'main -- start: ',time.ctime()
    threads = []
    t1 = myThread(sleep_second,(2,))
    # func = sleep_second ;args = (2,)  # 实例化
    threads.append(t1)
    t2 = myThread(sleep_five,(5,))
    threads.append(t2)
    for i in range(len(threads)):
        threads[i].start()  # 执行start()方法时，将运行run()方法。
    for i in range(len(threads)):
        threads[i].join()
    print 'main -- done: ',time.ctime()
if __name__ == '__main__':
    main()
'''
说明一下run方法 和start方法:
它们都是从Thread继承而来的，
run()方法将在线程开启后执行，
可以把相关的逻辑写到run方法中（通常把run方法称为活动[Activity]。）；
start()方法用于启动线程。
'''