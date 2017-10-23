#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:domain_resolve.py
@time:2017/5/10 0010 14:16
"""
from dns import resolver
import threading
import datetime
import time
domainlist = []

def recordlog(msg):
    with open('/data/log/domainResolvError.txt','ab') as f:
        f.write(msg)
def resolvDomain(domain,strdate):
    try:
        A = resolver.query(domain,'A')
    except Exception,e:
        #print e
        #print type(str(e))
        recordlog(strdate + '\n')
        recordlog(str(e)+ '\n')

def main():
    while 1:
        threads = []
        nowdata = datetime.datetime.now()
        strdate = nowdata.strftime('%Y-%m-%d %H:%M:%S')
        for d in domainlist:
            t = threading.Thread(target=resolvDomain,args=(d,strdate))
            threads.append(t)
        for i in range(len(threads)):
            threads[i].start()
        for i in range(len(threads)):
            threads[i].join()
        time.sleep(5)

if __name__ == '__main__':
    main()