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
env.hosts = ['139.217.0.48','139.217.4.72','139.217.3.79','139.217.9.227','139.217.15.49','139.217.9.72','139.217.5.102']
env.password = '50dxOp&^4V1z'
#env.gateway = '124.243.248.107'
env.colorze_errors = True

@task
def create_root_passwd():
    print yellow("create root passwd")
    sudo("echo '50dxOp&^4V1z' | passwd --stdin root")

@task
#配置hosts，并修改阿里云虚机的主机名
def put_file():
    put("/data/tool/hosts", "/etc/")
    local_ip = run("ifconfig | grep 'inet addr' | grep -v 127|awk '{print $2}' |sed 's/addr://'")
    local_hostname = run("sed -n '/%s/p' /etc/hosts |awk '{print $2}'" % local_ip)
    run("sed -i '/HOSTNAME/s/HOSTNAME=.*/HOSTNAME=%s/' /etc/sysconfig/network " % local_hostname)
    run("hostname %s" %local_hostname)