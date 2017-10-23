#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="test1"
__date__="2016/9/9"
__time__="9:34"
"""
import paramiko
from multiprocessing import Pool
def FilePut(ip,arg):
    print arg
    t = paramiko.Transport((ip,22))
    t.connect(username='root',password='123456')
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('/mnt/a.sh','/mnt/b.sh')
    t.close()
pool = Pool(processes=1)

#pool.apply_async(FilePut,['192.168.4.129','5555']).get()

def x(a,b):
    pool.apply_async(FilePut,[a,b]).get()

x('192.168.4.129','5555')