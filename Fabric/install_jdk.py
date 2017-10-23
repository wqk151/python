#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_jdk.py
@time:2017/1/3 0003 10:19
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['jdk-7u51-linux-x64.tar.gz','jdk_environment.sh']

env.user = 'root'
env.hosts = ['139.217.0.48']
env.password = '50dxOp&^4V1z'
#env.gateway = '124.243.248.107'
env.colorze_errors = True

def put_file():
    print yellow('start put file %s' % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
        if result.failed and not confirm("put file failed ,Continue[Y/N]"):
            abort("Aborting file put task")
        if local_file[i] == 'jdk-7u51-linux-x64.tar.gz':
            uncompress_jdk(local_file[i])

def uncompress_jdk(local_file):
    print yellow("uncompress %s" % local_file)
    with settings(warn_only=True):
        with cd(remote_dir):
            run('tar zxf %s' % local_file)
            run('mv jdk1.7.0_51 /data/apps/jdk')



def configure_jdk_environment_variable():
    print yellow("configure jdk environment variable")
    with settings(warn_only=True):
        run("rpm -qa | grep jdk | xargs rpm -e --nodeps")
        run("sh /data/tools/jdk_environment.sh")
        run('chown jumpserver:jumpserver -R /data/')


@task
def go():
    with hide('running', 'stdout'):
        put_file()
        configure_jdk_environment_variable()