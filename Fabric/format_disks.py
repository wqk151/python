#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:format_disks.py
@time:2017/1/3 0003 11:07
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'root'
env.hosts = []
env.password = '123'
#env.gateway = ''
env.colorze_errors = True

local_dir = os.getcwd()
remote_dir = '/tmp/'
local_file = 'fdiskcmd.txt'

def put_file():
    print yellow("put file %s" % local_file)
    result = put(local_dir + '/' + local_file, remote_dir + local_file)
    if result.failed and not confirm("put file failed Continue?[Y/N]"):
        abort("Aborting file put task")


def format_disks():
    print yellow("format disk vdb")
    run("fdisk /dev/vdb < /tmp/fdiskcmd.txt")
    run("mkfs.ext4 -T largefile /dev/vdb1")
    run("mkdir -p /data && mount /dev/vdb1  /data")
    run("echo '/dev/vdb1 /data ext4 defaults  0 0'>> /etc/fstab")
@task
def go():
    with hide('running', 'stdout'):
        put_file()
        format_disks()
