#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="ping"
__date__="2016/9/14"
__time__="9:13"
"""
import os
import Queue
import threading

q = Queue.Queue()
_thread = 100
iplist = ['192.168.4.129','192.168.4.130','192.168.4.131']
for i in iplist:
    q.put(i)
#print q.get()
#print q.get()
#print q.get()

def Ping(i,q):
    while True:
        ip = q.get()
        print "thread%s ping %s"  % (i,ip)
        data = os.system("ping -c 1 %s >/dev/null 2<&1" % ip)
        if data ==0:
            print "ping %s ok" % ip
        else:
            print "pint %s no ok" % ip
        q.task_done()



for i in range(_thread):
    run = threading.Thread(target=Ping,args=[i,q])
    run.setDaemon(True) # 结束Ping的死循环，否则会话会挂起
    run.start()
q.join()
print "ping over"

