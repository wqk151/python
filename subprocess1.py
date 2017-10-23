#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:subprocess1.py
@time:2016/10/9 9:08
"""
from threading import Thread
import subprocess
from  Queue import Queue

num_threads = 3
ips = ['127.0.0.1','192.168.4.129']

q=Queue()

def pingme(i,queue):
    while True:
        ip = queue.get()
        print 'Thread %s pinging %s' %(i,ip)
        ret = subprocess.call('ping -c 1 %s' % ip,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.PIPE)
        if ret == 0:
            print '%s is alive!' %ip
        elif ret == 1:
            print '%s is down ..' %ip
        queue.task_done()

for i in range(num_threads):
    t = Thread(target=pingme,args=(i,q))
    t.setDaemon(True)
    t.start()

for ip in ips:
    q.put(ip)
print 'main thread waiting ...'
q.join();print 'done ..'
