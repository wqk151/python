#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:gatewy_put_exec.py
@time:2016/12/13 0013 15:08
"""
"""
通过Fabric的env对象定义网关模式，即俗称的中转、堡垒机环境。定义格式为“env.gateway='192.168.1.23'”，其中"192.168.1.23"为堡垒机ip，
在结合任务函数实现目标主机文件上传与执行的操作。
通过配置env.gateway='192.168.1.23'就可以轻松实现堡垒机环境的文件上传及执行，比paramiko的实现方法简洁了很多，编写任务函数完全不用考虑堡垒机环境，配置env.gateway即可。
"""
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = 'root'
env.gateway = '192.168.1.23'    # 定义堡垒机ip，作为文件上传，执行的中转设备
env.hosts = ['192.168.1.21','192.168.1.22']
# 假如所有主机密码都不一样，可以通过env.passwords自定变量一一指定
env.passwords = {
    'root@192.168.1.21:22':'123455',
    'root@192.168.1.22:22':'123456',
    'root@192.168.1.23:22':'123457',    # 堡垒机账号信息
}

lpackpath = '/home/install/lnmp0.9.tar.gz'  # 本地安装包路径
rpackpath = '/tmp/install'  # 远程安装包路径

@task
def put_task():
    run('mkdir -p /tmp/install')
    with settings(warn_only=True):
        result = put(lpackpath,rpackpath)   # 上传安装包
    if result.failed and not confirm("put file failed,Continue[Y/N]?"):     # confirm获取提示信息
        abort("Aborting file put task!")
@task
def run_task():     # 执行远程命令，安装lnmp环境
    with cd("/tmp/install"):
        run('tar -zxf lnmp0.9.tar.gz')
        with cd('lnmp0.9'):     #使用with继续继承/tmp/install目录位置状态
            run('./contos.sh')
@task
def go():
    put_task()
    run_task()