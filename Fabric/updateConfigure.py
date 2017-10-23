#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:updateConfigure.py
@time:2017/1/18 0018 17:19
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file =[ 'server.properties',]
kafka_config_dir = '/data/apps/kafka/config/'

env.hosts = ['139.224.37.185:61303','139.224.37.185:61304',]
env.password = '50dxOp&^4V1z'


def uploadUpdateConfigureFile():
    for f in range(len(local_file)):
        print yellow("upload file %s" % f)
        put(local_dir + '/' + local_file[f],remote_dir + local_file[f])

def updateKafaConfigureFile():
    print yellow("update KafaConfigureFile")
    with cd(remote_dir):
        run("\\cp server.properties %s" % kafka_config_dir)

def stopKafka():
    print yellow("stop kafka")
    run("ps aux | grep kafka  | grep -v grep  |awk '{print $2}' | xargs kill ")

def startKafka():
    print yellow("start kafka")
    run('. /etc/profile && su jumpserver -l -c "nohup /data/apps/kafka/bin/kafka-server-start.sh /data/apps/kafka/config/server.properties &" ')

def modification_kafka_configure():
    print yellow("modification kafka configure")
    run("sed -i '/2181/s/\/.*//' /data/apps/kafka/config/server.properties")
    run("sed -n '/2181/p' /data/apps/kafka/config/server.properties")

@task
def go():
    #uploadUpdateConfigureFile()
    #updateKafaConfigureFile()
    modification_kafka_configure()
    stopKafka()
    startKafka()
