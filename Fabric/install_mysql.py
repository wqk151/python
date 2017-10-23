#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:install_mysql.py
@time:2017/1/3 0003 18:16
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
local_dir = os.getcwd()
remote_dir = '/data/tools/'
local_file = ['mysql-5.6.10.tar.gz','mysql_environment.sh']

env.user = 'root'
env.hosts = ['']
env.password = '123'
env.colorze_errors = True
env.mysal_install_dir = '/data/apps/mysql/'
env.mysql_data_dir = '/data/workspace/mysql/'

def yum_package():
    print yellow("yum some packages")
    run("yum -y install  gcc gcc-c++ gcc-g77 autoconf automake zlib* fiex* libxml* ncurses-devel libtool-ltdl-devel* make cmake library  bison-devel")

def add_user_workdir():
    print yellow("add user for mysql")
    run("groupadd mysql && useradd -s /sbin/nologin -g mysql -M mysql")
    print yellow("mkdir some dirs for mysql work")
    run("mkdir -p %slogs && mkdir -p %s" % (env.mysal_install_dir,env.mysql_data_dir))

def umcompress_mysql(mysql_file):
    print yellow("uncompress %s" % mysql_file)
    with settings(warn_only=True):
        with cd(remote_dir):
            run("tar zxf %s" % mysql_file)

def put_file():
    print yellow("put files %s " % local_file)
    for i in range(len(local_file)):
        with settings(warn_only=True):
            result = put(local_dir + '/' + local_file[i],remote_dir + local_file[i])
        if result.failed and not confirm("put the failed,Continue[Y/N]"):
            abort("Aborting file put task")
        if local_file[i] == "mysql-5.6.10.tar.gz":
            umcompress_mysql(local_file[i])

def compile_mysql():
    print yellow("compile mysql")
    with cd("%smysql-5.6.10" % remote_dir):
        run("cmake \
-DMYSQL_USER=mysql \
-DCMAKE_INSTALL_PREFIX=/data/apps/mysql \
-DMYSQL_DATADIR=/data/workspace/mysql \
-DMYSQL_UNIX_ADDR=/data/apps/mysql.sock \
-DSYSCONFDIR=/data/apps/mysql/ \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_READLINE=1 \
-DMYSQL_TCP_PORT=3306 \
-DENABLED_LOCAL_INFILE=1 \
-DWITH_PARTITION_STORAGE_ENGINE=1 \
-DEXTRA_CHARSETS=all \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DWITH_READLINE=1")
        run("make && make install")

def initialize_msyql():
    print yellow("initialize mysql")
    run("mv /etc/my.cnf /tmp/my.cnf-bak")
    run("%sscripts/mysql_install_db  --datadir=%s --user=mysql --basedir=%s" %(env.mysal_install_dir,env.mysql_data_dir,env.mysal_install_dir))
    run("chown -R mysql:mysql %s" % env.mysal_install_dir)
    print yellow("configure mysql")
    run("cp %ssupport-files/mysql.server /etc/init.d/mysql" % env.mysal_install_dir)
    run("cp %sbin/mysql /bin/" % env.mysal_install_dir)
    run('sed -i "/\[mysqld\]/a\datadir=%s" %smy.cnf' %(env.mysql_data_dir,env.mysal_install_dir))
    run('sed -i "/\[mysqld\]/a\log_error=%slogs/error.log" %smy.cnf'%(env.mysal_install_dir,env.mysal_install_dir))
    run("chkconfig mysql on")

def env_mysql():
    print yellow("env mysql")
    with cd(remote_dir):
        run("sh mysql_environment.sh")

@task
def go():
    with hide('running', 'stdout'):
        yum_package()
        add_user_workdir()
        put_file()
        compile_mysql()
        initialize_msyql()
        env_mysql()


