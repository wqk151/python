#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading2.py
@time:2016/11/11 0011 15:24
"""
from Queue import Queue
import random,time,threading

class Producer(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue
    def run(self):
        for i in range(5):
            print "%s:%s is producing %d to the queue! \n" % (time.ctime(),self.getName(),i)
            self.data.put(i)
            self.data.put(i*i)
            time.sleep(2)
        print "%s:%s finished!"%(time.ctime(),self.getName())

class Consumer(threading.Thread):
    def __init__(self,t_name,queue):
        threading.Thread.__init__(self,name=t_name)
        self.data = queue
    def run(self):
        for i in range(10):
            val = self.data.get()
            print "%s:%s is consuming.%d in the queue is consumed! \n" %(time.ctime(),self.getName(),val)
        print "%s:%s finished!" %(time.ctime(),self.getName())

if __name__ == '__main__':
    queue = Queue()
    producer = Producer('Pro.',queue)
    consumer = Consumer('Con,',queue)
    producer.start()
    consumer.start()
    producer.join()
    producer.join()