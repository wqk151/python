#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading1.py
@time:2016/11/11 0011 14:58
"""
import threading
from Queue import Queue
from time import sleep,ctime

class ThreadFunc(object):
    def __init__(self,func,args,name=''):
        self.name = name
        self.func = func
        self.args = args

    def __call__(self):
        print self.name,self.func,self.args
        apply(self.func,self.args)

def loop(nloop,ip,queue):
    print 'start',nloop,'at:',ctime()
    queue.put(ip)
    sleep(2)
    print 'loop',nloop,'done at:',ctime()

if __name__ == '__main__':
    threads = []
    queue = Queue()
    iplist = ['1','2','3']
    nloops = range(len(iplist))

    for i in nloops:
        print loop.__name__
        t = threading.Thread(target=ThreadFunc(loop,(i,iplist[i],queue),loop.__name__))
        threads.append(t)
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()
    for i in nloops:
        print queue.get()
