#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading_setdaemon.py
@time:2017/4/20 0020 14:24
"""
'''
使用多线程默认情况下，当主线程退出后，即使子线程没有join，子线程也依然会继续执行。
如果希望主线程退出后，其子线程也退出而不再执行，则需要设置子线程为后台线程。
Python提供了setDaemon方法，将子线程与主线程进行绑定，当主线程退出时，子线程的生命也随之结束。
'''
import threading
import random
import time
class myThread(threading.Thread):
    def run(self):
        wait_time = random.randint(1,10)
        print 'thread %s will wait %s s' %(self.name,wait_time)
        time.sleep(wait_time)
        time.sleep(30)
        print 'thread %s finished ' % self.name

def main():
    print 'main thread start ---:'
    for i in range(3):
        t = myThread()
        t.setDaemon(1)
        # 设置线程的daemon标志，在start()方法前调用
        t.start()
    print 'main thread end ---'

if __name__ == '__main__':
    main()

# 本来子线程需要等待几秒才能结束，但是主线程提前结束了，所以子线程也随主线程结束了。