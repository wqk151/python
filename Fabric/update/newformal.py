#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:newformal.py
@time:2017/4/19 0019 11:38
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
import datetime
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)
logging.disable(logging.INFO)
env.user = 'root'
# 正式环境主机ip
#env.hosts = ['139.217.15.186:22','139.217.26.253:22','139.217.14.172:22']

#web3
#env.hosts = ['139.217.14.172:22']
#web4
env.hosts = ['42.159.24.56:22']

#datamall-api-web1
env.hosts = ['139.217.24.57:22']


env.gateway = '124.243.248.109:22'
env.colorze_errors = True
env.rootDirectory = '/data/workspace/website/datatangapi-service/WEB-INF/classes/'
env.updatePackageDir = '/data/updatePackage'
env.nowTime = datetime.datetime.now().strftime('%Y%m%d')    # '20170221'
env.updatePackage = env.nowTime + '.zip'    # '20170221.zip'
localDir = env.updatePackageDir + '/' + env.nowTime # '/data/updatePackage/20170221'
listFile = 'list.txt'

@task
def drop_port_8080():
    run("iptables -I INPUT -p tcp --dport 8080 -j DROP")
    run("iptables -I INPUT -s 124.65.37.222 -p tcp --dport 8080 -j ACCEPT")

@task
def restart_iptables():
    run("/etc/init.d/iptables restart")

@task
def codeBackup():
    backupTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    print yellow("backup souce code")
    with cd('/data/workspace/website/'):
        run("cp -r datatangapi-service datatangapi-service_%s_bak" % backupTime)
        run("chown -R jumpserver:jumpserver datatangapi-service_%s_bak" % backupTime)
@task
def updateCode():
    n = 0
    with open(localDir + '/' + listFile) as f:
        for i in f.xreadlines():
            completeList = env.rootDirectory + i.replace('\\','/').strip()
            remoteDir =  os.path.split(completeList)[0]
            updateFile =  os.path.split(completeList)[1]
            #put(os.path.split(full)[0],os.path.split(full)[1])
            for currentDir,nextDir,currentFileList in os.walk(localDir):
                if updateFile in currentFileList:
                    currentFile = os.path.join(currentDir,updateFile)
                    run("mkdir -p %s" %  remoteDir)
                    put(currentFile,remoteDir)
                    n +=1
    print green("A total of %s files were updated" % n)
    run("chown -R jumpserver:jumpserver %s" % env.rootDirectory)

@task
def restartTomcat():
    print yellow("restart tomcat")
    run(" ps aux | grep ClassLoaderLogManager  | egrep -v 'grep' |awk '{print $2}' | xargs kill")
    time.sleep(5)
    run('. /etc/profile &&  su jumpserver -l -c "/data/apps/tomcat/bin/startup.sh" ')


@task
def go():
    drop_port_8080()
    codeBackup()
    updateCode()
    restartTomcat()


logging.debug('end')
