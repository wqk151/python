#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:projcetUpdate.py
@time:2017/1/10 0010 11:29
"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import time,os

updatePackageDir = '/data/updatePackage/'
startTomcatScript= '/data/sh/startTomcat.sh'
stopTomcatScript = '/data/sh/stopTomcat.sh'
programDir = '/data/workspace/website/datatangapi-service'
releaseVersion = 'release'
localDate = time.strftime('%Y%m%d')
updatePackage = 'datatangapi-service.tar.gz'

#env.user = 'root'
env.hosts = []
#env.password = '123'
env.gateway = ''
env.colorze_errors = True

def uncompressUpdatePackage(package):
    print yellow("uncompress update package %s" % package)
    with cd(updatePackageDir):
        run("tar zxf %s" % package)
        #run("chown -R jumpserver:jumpserver %s" % package.rstrip('.tar.gz'))

def uploadUpdatePackage():
    print yellow("upload update package %s" % updatePackage)
    put(updatePackageDir + updatePackage ,updatePackageDir + updatePackage)
    uncompressUpdatePackage(updatePackage)

def stopTomcat():
    print yellow("stop tomcat")
    run("sh %s " % stopTomcatScript)
def startTomcat():
    print yellow("start tomcat")
    run("sh %s " % startTomcatScript)

def createLink():
    print yellow("create soft link")
    with settings(warn_only=True):
        # 变量linkDirExists是命令输出的值，而不能是一个执行命令后的返回值
        linkDirExists = run("test -d %s && echo $? || echo $?" % programDir)
    # the variable linkDirExists is a string
    if not int(linkDirExists):
        run("rm -fr %s" % programDir)
        with cd(updatePackageDir):
            run("mv %s %s_v2" % (releaseVersion,localDate))
            run("mv %s %s" % (updatePackage.rstrip('.tar.gz'),releaseVersion))
            run("ln -s %s%s %s"%(updatePackageDir,updatePackage.rstrip('tar.gz'),programDir))
            run("chown -R jumpserver:jumpserver %s" % programDir)
            run("rm -fr %s%s" % (updatePackageDir,updatePackage))
    else:
        with cd(updatePackageDir):
            run("mv %s %s" % (updatePackage.rstrip('.tar.gz'), releaseVersion))
            run("ln -s %s%s  %s"%(updatePackageDir,releaseVersion,programDir))
            run("chown -R jumpserver:jumpserver %s" % programDir)
            run("rm -fr %s%s" % (updatePackageDir, updatePackage))

@task
def rollBack():
    print yellow("begin rollBack version %s_v2" % localDate)
    stopTomcat()
    run("rm -fr %s" % programDir)
    run("ln -s %s%s  %s"% (updatePackageDir,localDate+'_v2',programDir))
    run("chown -R jumpserver:jumpserver %s" % programDir)
    startTomcat()

@task
def go():
    with hide("running","stdout"):
        uploadUpdatePackage()
        stopTomcat()
        createLink()
        startTomcat()
