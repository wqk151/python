#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_supervisor.py
@time:2017/1/4 0004 18:20
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['supervisor-3.3.1.tar.gz','setuptools-32.3.1.zip', 'python_environment.sh']

env.user = 'root'
env.hosts = []
env.password = '123'
env.colorze_errors = True

env.supervisor_uncompress_dir = local_file[0].rstrip('.tar.gz')
env.setuptools_uncompress_dir = local_file[1].rstrip('.zip')

def uncompress_installation_package(file):
    print yellow("uncompress %s" % file)
    with cd(remote_dir):
        if file.endswith('gz'):
            run("tar zxf %s" % file)
        elif file.endswith("zip"):
            run("unzip %s" % file)


def upload_installation_package():
    for i in range(len(local_file)):
        print yellow("upload package %s" % local_file[i])
        result = put(local_dir + '/' + local_file[i],remote_dir+local_file[i])
        if result.failed and not confirm("put file failed,Continue[Y/n]"):
            abort("Aborting file put task")
        uncompress_installation_package(local_file[i])

def configure_python_environment_variable():
    print yellow("configure python environment variable")
    with cd(remote_dir):
        run("sh python_environment.sh")

def install_package(file_dir):
    print yellow("install %s" %(file_dir.split('-')[0]))
    with cd(remote_dir):
        run("cd %s && python setup.py install" % file_dir)
        if file_dir.startswith('supervisor'):
            print yellow("create supervisor confguration file")
            run(". /etc/profile && echo_supervisord_conf >/etc/supervisord.conf")
            run("chown jumpserver:jumpserver /etc/supervisord.conf")


@task
def go():
    with hide("running","stdout"):
        upload_installation_package()
        #configure_python_environment_variable()
        install_package(env.setuptools_uncompress_dir)
        install_package(env.supervisor_uncompress_dir)