#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading1.py
@time:2017/4/18 0018 18:25
"""
# threading是Python的管理多线程模块，实际工作中很常用，很多功能类似multiprocessing(多进程模块)
'''
python提供了几个用于多线程编程的模块，包括thread，threading，和Queue等。
threading是比thread更高级的模块。
'''
# 多线程实例一，创建一个Thread实例，传给它一个函数
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
threads = []
def main():
    print 'main start !!! ',time.ctime()
    t1 = threading.Thread(target=sleep_second,args=(2,))  #把函数和参数传进去，得到返回的Thread实例
    threads.append(t1)
    t2 = threading.Thread(target=sleep_five,args=(5,))
    threads.append(t2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    '''
    for i in range(len(threads)):
        threads[i].start()
        #threads[i].join()    如果join在此处，则所有线程为串行

    for i in range(len(threads)):
        threads[i].join()   #join()函数运行主线程等待所有线程结束。
    '''
    print 'main done !!!',time.ctime()

if __name__ == '__main__':
    main()
