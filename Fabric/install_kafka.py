#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_kafka.py
@time:2017/1/3 0003 16:24
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['kafka_2.10-0.8.2.2.tgz','kafka_environment.sh','server.properties']

env.user = 'root'
env.hosts = []
env.password = '123'

env.kafkalogdir = '/data/workspace/kafkadata'
env.kafkaiplist = ['172.16.1.220','172.16.1.221']
env.num = 1
#env.gateway = '124.243.248.107'
env.colorze_errors = True

def put_file():
    print yellow("put file %s" % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' +local_file[i],remote_dir + local_file[i])
        if result.failed and not confirm("put file failed,Continue?[Y/N]"):
            abort("Aborting file put task")
        if local_file[i] == 'kafka_2.10-0.8.2.2.tgz':
            uncompress_kafka(local_file[i])

def uncompress_kafka(kafka_file):
    print yellow("uncompress %s" % kafka_file)
    with settings(warn_only=True):
        with cd(remote_dir):
            run("tar zxf %s" % kafka_file)
            run("mv kafka_2.10-0.8.2.2 /data/apps/kafka")
            run("\\cp server.properties /data/apps/kafka/config/")

def configure_kafka():
    print yellow("configure kafka")
    with settings(warn_only=True):
        run("mkdir -p %s" % env.kafkalogdir)
        with cd("/data/apps/kafka/config"):
            local_ip = run("ifconfig | grep 'inet addr' | grep -v 127|awk '{print $2}' |sed 's/addr://'")
            run("sed -i '/broker\.id/s/0/%s/' server.properties" % env.num )
            env.num -=1
            run("sed -i '/host\.name/s/$/%s/' server.properties" % local_ip)

def env_kafka():
    print yellow("configure kafka environment variable")
    with settings(warn_only=True):
        run("sh %skafka_environment.sh" % remote_dir)


@task
def go():
    with hide('running','stdout'):
        put_file()
        configure_kafka()
        env_kafka()
