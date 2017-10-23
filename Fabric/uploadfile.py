#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:update_test.py
@time:2017/1/19 0019 16:05
"""
'''
批量上传当前目录下的文件到远程服务器
例如：将当前目录下的a.txt b.txt 两个文件上传到远程服务器的/data/tools目录下
eg: fab -f test.py uploadFile:'/data/tools','a.txt  b.txt'
'''

from fabric.colors import *
from fabric.api import *

import os,sys
localFileDir = os.getcwd()
env.hosts = ['10.10.20.59',]
env.password = '123456'

def uploadHelp():
    print blue("""
1、you need to switch to directory  where you want to upload the file first.
2、format:
fab -f scriptName functionName:'<remoteDir>','<file list>'
note: multiple files are separated by spaces
3、eg:
fab -f uploadfile.py go:'/data/tools','a.txt  b.txt'
    """)

if len(sys.argv) != 4:
    uploadHelp()
    sys.exit()

@task
def go(remoteDir,fileName):
    for f in range(len(fileName.split())):
        print green(" upload file %s to %s " % (fileName.split()[f],env.hosts))
        remoteDir = remoteDir if str(remoteDir).endswith('/') else remoteDir + '/'
        result = put(localFileDir + '/' + fileName.split()[f],remoteDir )
        if result.failed:
            uploadHelp()
        run("chown jumpserver:jumpserver %s" % (remoteDir + fileName.split()[f]))