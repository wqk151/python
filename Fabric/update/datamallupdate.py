#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:datamallupdate.py
@time:2017/5/4 17:28
"""
from fabric.colors import *
from fabric.api import *
import os
# 测试环境主机ip
env.hosts = ['42.159.28.126:55915']
env.gateway = '124.243.248.109:22'
env.colorze_errors = True
env.rootDirectory = '/opt/workspace/tomcat/tomcat-datamall/webapps/'
env.dataMall = 'dataMall.zip'
'''
1、上传包
2、停止tomcat
3、unzip 包
4、删除ROOT包
5、重命名datamall-->ROOT --》修改权限
6、启动tomcat
'''
def put_zip():
    localDir = os.getcwd()
    with cd(localDir):
        put(env.dataMall,env.rootDirectory)

def stop_tomcat():
    run(" ps aux | grep ClassLoaderLogManager|grep datamall  | egrep -v 'grep' |awk '{print $2}' | xargs kill")

def update():
    with cd(env.rootDirectory):
        run("unzip %s" % env.dataMall)
        run("rm -fr ROOT && mv dataMall ROOT")
        run("chown -R jumpserver:jumpserver ROOT")
        run("rm -fr %s" % env.dataMall)
@task
def start_tomcat():
    run('. /etc/profile &&  su jumpserver -l -c "/opt/workspace/tomcat/tomcat-datamall/bin/startup.sh" ')


@task
def go():
    put_zip()
    stop_tomcat()
    update()
    start_tomcat()