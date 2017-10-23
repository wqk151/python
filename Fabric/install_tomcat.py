#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_tomcat.py
@time:2017/1/6 0006 11:22
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['apache-tomcat-7.0.68.tar.gz','tomcat_environment.sh']

env.user = 'root'
env.hosts = []
env.password = '123'
env.colorze_errors = True

env.tomcat_unmpress_dir = local_file[0].rstrip('.tar.gz')

def uncompress_installation_package(file):
    print yellow("uncompress %s" % file)
    with cd(remote_dir):
        run("tar zxf %s" % file)
        run("mv %s /data/apps/tomcat" % env.tomcat_unmpress_dir)
        run("chown jumpserver:jumpserver -R /data/apps/tomcat")

def upload_installation_package():
    for i in range(len(local_file)):
        print yellow("upload package %s" % local_file[i])
        put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
        if local_file[i].endswith('gz'):
            uncompress_installation_package(local_file[i])

def configrue_tomcat_environment_variable():
    print yellow("configure tomcat environment variable")
    with cd(remote_dir):
        run("sh tomcat_environment.sh")
@task
def go():
    with hide("running","stdout"):
        upload_installation_package()
        configrue_tomcat_environment_variable()




