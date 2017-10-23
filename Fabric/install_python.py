#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:put_file.py
@time:2016/12/28 0028 8:54
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['Python-2.7.11.tgz','python_environment.sh']

env.user = 'root'
env.hosts = ['']
env.password = ''
#env.gateway = ''
env.colorze_errors = True


def yum_parket():
    print yellow("yum some parket")
    run('yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel')


def put_file():
    print yellow("Start put file %s" % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
        if result.failed and not confirm("put file failed,Continue[Y/N]"):
            abort("Aborting file put task")
        if local_file[i].endswith('tgz'):
            install_python(local_file[i])


def install_python(local_file):
    print yellow("Start tar file %s" % local_file)
    with settings(warn_only=True):
        with cd(remote_dir):
            run('tar zxf %s' % local_file)
            run('cd Python-2.7.11 && ./configure --prefix=/data/apps/python && make && make install ')


def ln_python():
    print yellow("link python to /usr/bin/")
    with cd('/usr/bin'):
        run('mv python python-bak')
        run('ln -s /data/apps/python/bin/python /usr/bin/python')
        run("sed -i '1s/$/2.6/' yum ")


def configure_python_environment_variable():
    print yellow("configure python environment variable")
    with cd(remote_dir):
        run("sh python_environment.sh")
@task
def go():
    with hide('running', 'stdout'):
        yum_parket()
        put_file()
        ln_python()
        configure_python_environment_variable()