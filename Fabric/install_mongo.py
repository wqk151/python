#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_mongo.py
@time:2017/1/4 0004 9:24
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['mongodb-linux-x86_64-rhel62-3.2.8.tgz','mongo_environment.sh','mongod.conf']

env.user = 'root'
env.hosts = ['']
env.password = '123'
env.colorze_errors = True
env.mongo_install_dir = '/data/apps/mongo'
env.mongo_data_dir = '/data/workspace/mongo'

def uncompress_mongo(file):
    print yellow("uncompress %s" % file)
    with settings(warn_only=True):
        with cd(remote_dir):
            run("tar zxf %s" % file)
            run("mv mongodb-linux-x86_64-rhel62-3.2.8 %s" % env.mongo_install_dir)

def put_file():
    print yellow("put file %s" % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i], remote_dir+local_file[i])
        if result.failed and not confirm("put file failed,Continue[Y/N]"):
            abort("Aborting file put task")
        if local_file[i] == 'mongodb-linux-x86_64-rhel62-3.2.8.tgz':
            uncompress_mongo(local_file[i])

def env_mongo():
    print yellow("env mongo")
    with settings(warn_only=True):
        with cd(remote_dir):
            run("cp mongod.conf /etc/")
            run("mkdir -p %s" % env.mongo_data_dir)
            run("sh mongo_environment.sh")

@task
def go():
    with hide("running","stdout"):
        put_file()
        env_mongo()

