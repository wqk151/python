#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:init.py
@time:2016/11/8 0008 11:05
"""

import sys
sys.path.append('..')
from conf.hosts import *
from bin.ssh_hosts_exec_order import ssh_transport_file,ssh_cmd
import multiprocessing
#print conf.hosts.h1.port
#print h1.port

def main():
    file_result = []
    cmd_results = []
    p = multiprocessing.Pool(processes=5)
    for i in h1.ip: # h1.ip是一个list
        msg = "-------result%s--------" % i
        print msg
        file_result.append(p.apply_async(ssh_transport_file,(i,h1.port,h1.user,h1.passwd,h1.file)))
        cmd_results.append(p.apply_async(ssh_cmd,(i,h1.port,h1.user,h1.passwd,h1.file)))
    p.close()

    #for res in file_result:
    #    res.get()

    for rest in cmd_results:
        rest.get()
if __name__ == '__main__':
    main()



