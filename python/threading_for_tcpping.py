#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:threading_for_tcpping.py
@time:2017/4/19 0019 9:13
"""
import subprocess
import threading
import time
iplist = ['www.baidu.com','www.163.com','www.qq.com','www.google.com']

def ping_host(ip):
    cmd = 'ping -c 1 %s' % ip
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    data = p.communicate()  # 阻塞主进程，等待子进程执行结束；communicate()返回一个元组：(stdoutdata, stderrdata)
    print data[0]
    print p.returncode  #获取子进程的返回值

threads = []
def main():
    print time.ctime()
    for ip in range(len(iplist)):
        t = threading.Thread(target=ping_host,args=(iplist[ip],))
        threads.append(t)
    for i in range(len(threads)):
        threads[i].start()
    for i in range(len(threads)):
        threads[i].join()
    print time.ctime()
if __name__ == '__main__':
    main()
