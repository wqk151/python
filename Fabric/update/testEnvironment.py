#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:testEnvironment.py
@time:2017/2/20 0020 14:28
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
# 测试环境主机ip
env.hosts = ['42.159.28.126:55915']
#uat环境主机ip
#env.password = '123456'
env.gateway = '124.243.248.107:22'
env.colorze_errors = True
env.rootDirectory = '/opt/workspace/website/datatangapi-service/WEB-INF/classes/'
env.updatePackageDir = '/data/updatePackage'
env.nowTime = datetime.datetime.now().strftime('%Y%m%d')    # '20170221'
env.updatePackage = env.nowTime + '.zip'    # '20170221.zip'
localDir = env.updatePackageDir + '/' + env.nowTime # '/data/updatePackage/20170221'
listFile = 'list.txt'

@task
def codeBackup():
    backupTime = datetime.datetime.now().strftime('%Y%m%d%H%M')
    print yellow("backup souce code")
    with cd('/opt/workspace/website'):
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
    time.sleep(3)
    run('. /etc/profile &&  su jumpserver -l -c "/opt/workspace/tomcat/apache-tomcat-7.0.57/bin/startup.sh" ')


@task
def go():
    codeBackup()
    updateCode()
    restartTomcat()


logging.debug('end')
