#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_nginx.py
@time:2017/1/4 0004 11:14
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['nginx-1.10.2.tar.gz','pcre-8.38.tar.gz']

env.nginx_name=local_file[0].split('-')[0]
env.nginx_uncom_dir = local_file[0].rstrip('.tar.gz')
env.nginx_app_dir = '/data/apps/nginx'
env.pcre_name=local_file[1].split('-')[0]
env.pcre_uncom_dir = local_file[1].rstrip('.tar.gz')
env.pcre_app_dir = '/data/apps/pcre'


env.user = 'root'
env.hosts = ['139.224.37.185:61306']
env.password = '50dxOp&^4V1z'
env.colorze_errors = True

def yum_packages():
    print yellow("yum some packages")
    with settings(warn_only=True):
        run("yum install -y zlib-devel openssl openssl-devel gd keyutils patch perl mhash")

def uncompress_file(file):
    print yellow("uncompress %s" % file)
    with cd(remote_dir):
        run("tar zxf %s" % file)

def put_files():
    print yellow("put files %s" % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
        if result.failed and not confirm("put file failed,Continue[Y/N]"):
            abort("Aborting file put task")
        if local_file[i].endswith('gz'):
            uncompress_file(local_file[i])

def compile_file(file):
    if file == env.pcre_name:
        print yellow("compile %s" % file)
        with cd(remote_dir+env.pcre_uncom_dir):
            run("./configure --prefix=%s && make && make install" % env.pcre_app_dir)
    elif file == env.nginx_name:
        print yellow("compile %s" % file)
        with cd(remote_dir + env.nginx_uncom_dir):
            run("./configure --prefix=%s --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-pcre=%s --with-http_realip_module"% (env.nginx_app_dir,remote_dir+env.pcre_uncom_dir))
            run("make && make install")


@task
def go():
    with hide("running","stdout"):
        yum_packages()
        put_files()
        compile_file('pcre')
        compile_file('nginx')