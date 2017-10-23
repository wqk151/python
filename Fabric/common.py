#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:common.py
@time:2017/2/13 0013 10:37
"""
"""
description:
some public method
note:
decompress the compressed package，unify the naming of the software and last to compressed them that must be end with 'tar.gz'.
process:
unpack the installation package --> rename(only keep the software name) --> package and compression(format:name-version.tar.gz)
for example:
tar zxf nginx-1.10.2.tar.gz
mv nginx-1.10.2 nginx
tar zcf nginx-1.10.2.tar.gz

"""
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import os
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)
env.tarList = []
# the directory of software installation package
installationPackageDir = '/data/tools'
filelist = os.listdir(installationPackageDir)
for i in range(len(filelist)):
    if filelist[i].endswith('tar.gz'):
        env.tarList.append(filelist[i])

# upload files
def perfectDir(fileDir):
    fileDir = fileDir if str(fileDir).endswith('/') else fileDir + '/'
    return fileDir

def uploadFiles(localDir,remoteDir,fileList):
    # fileList can be a list or a str.
    if type(fileList) == list:
        for i in range(len(fileList)):
            print yellow("upload file %s" % fileList[i])
            localDir = perfectDir(localDir)
            remoteDir = perfectDir(remoteDir)
            put(localDir + fileList[i],remoteDir + fileList[i])
    elif type(fileList) == str:
        print yellow("upload file %s" % fileList)
        localDir = perfectDir(localDir)
        remoteDir = perfectDir(remoteDir)
        put(localDir + fileList, remoteDir + fileList)

# download files
def downloadFile(localDir,remoteDir,fileList):
    if type(fileList) == list:
        for i in range(len(fileList)):
            print yellow("downlaod file %s" % fileList[i])
            localDir = perfectDir(localDir)
            remoteDir = perfectDir(remoteDir)
            get(remoteDir + fileList[i],localDir + fileList[i])
    elif type(fileList) == str:
        print yellow("download file %s" % fileList)
        localDir = perfectDir(localDir)
        remoteDir = perfectDir(remoteDir)
        get(remoteDir + fileList, localDir + fileList)

# move directory
def moveFileDir(fileName,appsDir):
    """like software of zookeeper,mongodb,kafka,tomcat,jdk and so on,that do not to compile"""
    print yellow("mv %s to %s" %(fileName.split('-')[0],appsDir))
    appsDir = perfectDir(appsDir)
    run('mv %s %s' % (fileName.split('-')[0],appsDir))

#decompress the compressed package，unify the naming of the software and last to compressed them that must be end with 'tar.gz'.
#default moveFlag = 1, means it well be moved to the directory of '/data/apps' after the package decompress.
def uncompressFile(fileDir,fileName,appsDir,moveFlag=1):
    """like the software of MySQL，nginx,python,iftop and so an,that neet to compile，moveFlag=2"""
    print yellow("uncompress %s" % fileName)
    #fileDir = perfectDir(fileDir)
    with cd(fileDir):
        fullFileName = run("ls | grep %s" % fileName)
        if fullFileName.endswith('tar.gz'):
            run('tar zxf %s' % fullFileName)
        if moveFlag == 1:
            moveFileDir(fileName,appsDir)

#modify the permissions of a directory or file，default group is root.
def changePermissions(fileDir,ownerName,ownerGroup='root'):
    print yellow("change %s permissions,Owner=%s,OwnerGroup=%s "%(fileDir,ownerName,ownerGroup))
    run("chown %s:%s -R %s" % (ownerName,ownerGroup,fileDir))

#configure environment variables，where default the scripts exits is the directory 'bin'.
def configureEnvironmentVariable(fileNameHome,appsDir,scriptDir='bin'):
    """fileNameHome=MONGO_HOME,appsDir=/data/apps/mongo/ """
    print yellow("configure %s's environment variable" % fileNameHome.split('_')[0])
    environmentConfigureFile = '/etc/profile'
    fileNameHomeNum = run("sed -n '/^%s/p' %s |wc -l" %(fileNameHome,environmentConfigureFile))
    if int(fileNameHomeNum) == 0:
        PATH_NUM = run("sed -n '/^PATH=\$/p' %s |wc -l " % environmentConfigureFile)
        if int(PATH_NUM) == 0:
            run("echo -e '%s=%s\nPATH=$PATH:$%s/%s\nexport PATH %s\n' >> %s"
                % (fileNameHome,appsDir,fileNameHome,scriptDir,fileNameHome,environmentConfigureFile))
        else:
            run("sed -i '/^PATH=/i\%s=%s' %s" % (fileNameHome,appsDir,environmentConfigureFile))
            run("sed -i '/^PATH=/s/$/:$%s\/%s/' %s" % (fileNameHome,scriptDir,environmentConfigureFile))
            run("sed -i '/^export/s/$/ %s/' %s" %(fileNameHome,environmentConfigureFile))
# excute remote shell commands
def executeRemoteCommands(shellCmd):
    with hide('running'):
        print yellow("execute remote commands: %s" % shellCmd)
        run(shellCmd)

# get installation package
def getInstallationPackageName(indexName):
    print yellow("will get installation package from  directory %s" % installationPackageDir)
    for i in range(len(env.tarList)):
        if env.tarList[i].startswith(indexName):
            return env.tarList[i]

logging.debug('end')