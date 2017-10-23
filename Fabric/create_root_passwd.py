#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:create_root_passwd.py
@time:2017/1/3 0003 10:52
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm

env.user = 'root'
env.hosts = []
env.password = '123'
#env.gateway = ''
env.colorze_errors = True

@task
def create_root_passwd():
    print yellow("create root passwd")
    sudo("echo '123' | passwd --stdin root")

@task
#配置hosts，并修改阿里云虚机的主机名
def put_file():
    put("/data/tool/hosts", "/etc/")
    local_ip = run("ifconfig | grep 'inet addr' | grep -v 127|awk '{print $2}' |sed 's/addr://'")
    local_hostname = run("sed -n '/%s/p' /etc/hosts |awk '{print $2}'" % local_ip)
    run("sed -i '/HOSTNAME/s/HOSTNAME=.*/HOSTNAME=%s/' /etc/sysconfig/network " % local_hostname)
    run("hostname %s" %local_hostname)