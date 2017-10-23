#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_iftop.py
@time:2017/1/5 0005 15:03
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['iftop-1.0pre4.tar.gz', 'iftop_environment.sh']

env.user = 'root'
env.hosts = ['139.217.0.48','139.217.4.72','139.217.3.79','139.217.9.227','139.217.15.49','139.217.9.72','139.217.5.102']
env.password = '50dxOp&^4V1z'
env.colorze_errors = True

env.iftop_uncompress_dir = local_file[0].rstrip('.tar.gz')



def uncompress_installation_package(file):
    with cd(remote_dir):
        if file.endswith('gz'):
            print yellow("uncompress %s" % file)
            run("tar zxf %s" %file)

def upload_installation_package():
    run("yum install -y libpcap-devel ncurses-devel")
    for i in range(len(local_file)):
        print yellow("upload package %s" % local_file)
        result = put(local_dir + '/' +local_file[i],remote_dir+local_file[i])
        if result.failed and not confirm("put file failed,Continue[Y/N]"):
            abort("Aborting file put task")
        uncompress_installation_package(local_file[i])

def configure_iftop_environment_variable():
    print yellow("configure iftop environment variable")
    with cd(remote_dir):
        run("sh iftop_environment.sh")

def install_package(file_dir):
    print yellow("install %s" %(file_dir.split('-')[0]))
    with cd(remote_dir):
        run("cd %s && ./configure --prefix=/data/apps/iftop && make && make install" % file_dir)

@task
def go():
    with hide("running","stdout"):
        upload_installation_package()
        install_package(env.iftop_uncompress_dir)
        configure_iftop_environment_variable()

#TODO 同时配置流量监控
'''
#!/bin/bash
set -e
#set -x
LOCAL_DATE=`date +%F`
TOWDAYSAGO=`date +%F -d "-2 day"`

echo `date` >>/data/workspace/networkLog/${LOCAL_DATE}_web4_network.log
/data/apps/iftop/sbin/iftop -Pp -Nn -t -L 30 -s 1 >>/data/workspace/networkLog/${LOCAL_DATE}_web4_network.log

rm -fr /data/workspace/networkLog/${TOWDAYSAGO}_web4_network.log

定时任务：* * * * * sh /data/sh/networkFlowStatistic.sh
'''