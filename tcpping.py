#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:tcpping.py
@time:2016/11/8 0008 16:50
"""
import threading
import subprocess
import time,sys
class TcpPing(threading.Thread):
    def __init__(self,func,args):
        super(TcpPing, self).__init__()
        self.func = func
        self.args = args
    def run(self):
        apply(self.func,self.args)

def tcping(name,ip,port):
    #print name,ip,port
    now_time = time.strftime('%Y-%m-%d-%H-%M-%S')
    ping_log_name = '/data/workspace/pinglog/' + name +'-'+ now_time
    #print ping_log_name
    try:

        f = file(ping_log_name, 'w')    # 一定要先创建文件，否则，文件名称（带时间）与创建时间不一致，等于是延迟60秒（ping了60次）写入
        ret = subprocess.Popen('/sbin/pwaiwang -c 50 %s -p %d'% (ip,int(port)),shell=True,stdout=subprocess.PIPE)
        out,err = ret.communicate()
        f.write(out)
        f.flush()
        f.close()
    except Exception:
        pass
'''
subprocess.call  直接打印输出到终端
subprocess.check_out 无法接收错误输出（即retruncode =1的无法接收）
'''


def main():
    threads = []
    f = file('/data/sh/hostslist')  # 如果不写绝对路径，手动执行没问题，但在crontab中执行报错
    file_list = f.readlines()
    nloops = range(len(file_list))
    for i in nloops:
        name = file_list[i].split()[0]
        ip = file_list[i].split()[1]
        port = file_list[i].split()[2]
        #print NAME,IP,PORT
        t = TcpPing(tcping,(name,ip,port,))
        threads.append(t)
        #print threads
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()
        sys.exit(0)     # 如果不退出，程序会一直循环执行，跟crontab并行执行

if __name__ == '__main__':
    main()




