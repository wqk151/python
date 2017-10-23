#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:test.py
@time:2016/12/16 0016 11:03
"""
from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import time
env.gateway = ''
env.colorze_errors = True

# 定义web服务器地址
env.hosts = ['']
env.now_time = time.strftime("%Y%m%d")
# 本地代码路径
env.project_dev_source = '/data/workspace'
env.project_tar_source = '/data/code_tar_dir'

# 远程web服务器代码路径
env.deploy_procect_dir = '/tmp'

@task
@runs_once
# [localhost] local: tar -zcf /data/code_tar_dir/20161219.tar.gz *
def tar_source_code():
    print yellow("start tar source code to package ...")
    with lcd(env.project_dev_source):
        local("tar -zcf %s/%s.tar.gz *" % (env.project_tar_source,env.now_time))


# 代码上传函数
@task
# put: /data/code_tar_dir/20161219.tar.gz -> /tmp/20161219.tar.gz
def put_package():
    print yellow('start put package ...')
    env.project_tar_code = env.project_tar_source + '/' + env.now_time + '.tar.gz'
    with settings(warn_only=True):
        result = put(env.project_tar_code,env.deploy_procect_dir)
    if result.failed  and not confirm("put file failed,Continue[Y/N]"):
        abort("Aborting file put task!")
    print green("put package sucess!!!")


# 建立软连接
#ln -s  env.deploy_procect_dir/20161219  /opt/workspace/tomcat
# 删除软连
#rm -fr /opt/workspace/tomcat

'''
使用普通用户执行命令
def run_su(command, user="tomcat"):
    return run('su %s -c "%s"' % (tomcat, /startup.sh))
'''
'''
@task
def go():
    with hide('running','stdout'):   # 定义输出信息的级别，针对命令
        with cd('/mnt'):
            env.old_version_id =  run("ls -l tomcat  |awk -F'/' '{print $3}'")
    print env.old_version_id
或
@task
def go():
    with hide('running','stdout'):
        tar_source_code()  # 针对函数
'''

@task
def go():
    tar_source_code()
    put_package()
