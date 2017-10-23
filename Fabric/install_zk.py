#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_zk.py
@time:2017/1/3 0003 15:07
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['zookeeper-3.4.8.tar.gz','zk_environment.sh']

env.user = 'root'
env.hosts = ['139.224.37.185:61303','139.224.37.185:61304','139.224.37.185:61305']
env.password = '50dxOp&^4V1z'

env.zkdatadir = '/data/workspace/zkdata'
env.zkiplist = ['192.168.0.12','192.168.0.13','192.168.0.14']

#env.gateway = '124.243.248.107'
env.colorze_errors = True

def put_file():
    print yellow("put file %s" % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
        if result.failed and not confirm("put file failed,Continue[Y/N]"):
            abort("Aborting file put task")
        if local_file[i] == 'zookeeper-3.4.8.tar.gz':
            uncompress_zk(local_file[i])
def uncompress_zk(zk_file):
    print yellow("uncompress %s" % zk_file)
    with settings(warn_only=True):
        with cd(remote_dir):
            run('tar zxf %s' % zk_file)
            run('mv zookeeper-3.4.8 /data/apps/zookeeper')

def configure_zk():
    print yellow("configure zookeeper")
    with settings(warn_only=True):
        myid = 3  # env是定义全局变量，这里不能使用全局变量，否则会出现0 - -5
        run('mkdir -p %s'% env.zkdatadir)
        with cd('/data/apps/zookeeper/conf'):
            run('cp zoo_sample.cfg zoo.cfg')
            run("sed -i '/dataDir=/s/=.*/=\/data\/workspace\/zkdata/' zoo.cfg")
            local_ip = run("ifconfig | grep 'inet addr' | grep -v 127|awk '{print $2}' |sed 's/addr://'")
            for i in range(len(env.zkiplist)):
                run("sed -i '/dataDir=/a\server.%s=%s:2888:3888' zoo.cfg " % (myid,env.zkiplist[i]))
                if env.zkiplist[i] == local_ip:
                    run("echo %s >%s/myid" %(myid,env.zkdatadir))
                myid -=1

def env_zk():
    print yellow("configure zookeeper environment variable")
    with settings(warn_only=True):
        run("sh %szk_environment.sh" % remote_dir)

@task
def go():
    with hide('running', 'stdout'):
        put_file()
        configure_zk()
        env_zk()




