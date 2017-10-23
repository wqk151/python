#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:mongo_repset_conf.py
@time:2017/7/13 0013 18:04
"""
import sys
sys.path.append('.')
from fabric.colors import *
from fabric.api import *
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)
#define the variables
#env.hosts = ['10.10.20.59',]
env.password = '123456'
env.user = 'root'
#env.gateway = '124.243.248.107'
env.locatDir = '/data/tools'
env.remoteDir = '/data/tools'
env.appsDir = '/data/apps'
env.workspaceDir = '/data/workspace'
env.scriptsDir = '/data/sh'
# use this user you must add it to Fortress machine first
env.homeOwner = 'jumpserver'
# grouping the hosts
env.roledefs = {
    'tomcat': ['42.159.118.146','42.159.114.145',],
    'jdk': ['42.159.118.146','42.159.116.246','42.159.114.221','42.159.115.32','139.217.12.97','42.159.114.145','139.217.24.57'],
    'mysql': ['42.159.115.32'],
    'mongodb': ['42.159.114.221'],
    'zookeeper':['42.159.118.146','42.159.114.145','139.217.12.97'],
    'python':['42.159.118.146','42.159.116.246','42.159.114.221','42.159.115.32','139.217.12.97','42.159.114.145','139.217.24.57'],
    'iftop':['42.159.118.146','42.159.116.246','42.159.114.221','42.159.115.32','139.217.12.97','42.159.114.145','139.217.24.57'],
    'iotop':['42.159.118.146','42.159.116.246','42.159.114.221','42.159.115.32','139.217.12.97','42.159.114.145','139.217.24.57'],
    'mq':['139.217.12.97'],
    'zabbix':['42.159.118.146','42.159.116.246','42.159.114.221','42.159.115.32','139.217.12.97','42.159.114.145','139.217.24.57'],
    'kafka':['42.159.118.146','42.159.114.145','139.217.12.97'],
}
# get the number of hosts within the cluster
env.mongoNum = len(env.roledefs['mongodb']) if env.roledefs.has_key('mongodb') else 0




# 安装并启动所有mongodb
@task
@roles('mongodb')
def install_mongo():
    mongoIndexName = 'mongodb'
    mongoHomeDir = env.appsDir + '/' + mongoIndexName
    mongoHomeName = 'MONGO_HOME'
    mongoDataDir = common.perfectDir(env.workspaceDir) + 'mongoData'
    mongoConfigurationFile = '/etc/mongodb.conf'
    mongoInstallationPackage = common.getInstallationPackageName(mongoIndexName)
    mongoPort = '27011'
    with hide('running','stdout'):
        try:
            common.uploadFiles(env.locatDir, env.remoteDir, mongoInstallationPackage)
            common.uploadFiles(env.locatDir, env.scriptsDir, 'keyfiletest')
            run("chmod 600 /data/sh/keyfiletest")
        except Exception,e:
            print 'directory or file not exit!!!',str(e)
        try:
            common.uncompressFile(env.remoteDir, mongoIndexName, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
        # create mongodb configuration file
        localPrivateIP = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
        env.mongoList.append(localPrivateIP)
        run("""
cat >%s <<EOF
systemLog:
  destination: file
  path: %s/shard1.log
  logAppend: true
processManagement:
  fork: true
  pidFilePath: "%s/mongod.pid"
net:
  bindIp: %s
  port: %s
  http:
    enabled: true
storage:
  dbPath: "%s"
  engine: wiredTiger
  wiredTiger:
    engineConfig:
      cacheSizeGB: 4
      directoryForIndexes: true
    collectionConfig:
      blockCompressor: zlib
    indexConfig:
      prefixCompression: true
  journal:
    enabled: true
  directoryPerDB: true
#security:
#  keyFile: "/data/sh/keyfiletest"
#  authorization: enabled
replication:
   replSetName: repset
EOF
"""% (mongoConfigurationFile,mongoDataDir,mongoHomeDir,localPrivateIP,mongoPort,mongoDataDir))
        # configure environment of mongodb
        common.configureEnvironmentVariable(mongoHomeName, mongoHomeDir)
        # create mongo dir
        run("mkdir -p %s" % mongoDataDir)

        if env.mongoNum ==1:
            run(" sed '/repl/s/^/\#/' %s" % mongoConfigurationFile)
        # start mongodb
        run('. /etc/profile &&  %s/bin/mongod -f %s ' %(mongoHomeDir,mongoConfigurationFile))
        '''
        if env.mongoNum >1:
            # configure cluster

            changeMongoconfigure(mongoConfigurationFile,2)
            if env.mongoNum == 1:
                changeMongoconfigure(mongoConfigurationFile, 2)
                configureMongoCluster(mongoHomeDir,localPrivateIP,mongoPort)
            env.mongoNum -= 1
'''
# 配置副本集
def configureMongoCluster():
    mongoHomeDir='/data/apps/mongodb'
    localIP = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
    port = 27011
    if env.mongoNum>1:
        idList = ''
        for i in range(len(env.mongoList)):
            idList += ' {_id:%s,host:"%s:%s"},' % (i,env.mongoList[i],port)
        configOrder = 'config = {_id:"repset", members:[ %s ]}'   % idList.rstrip(',')
        initOrder = 'rs.initiate(config);'
        #print 'configOrder: ',configOrder
        print yellow("initiate mongodb replication...")
        # run('cat /tmp/a.txt |%s/bin/mongo %s:%s/admin --shell' % (mongoHomeDir,localIP,port))
        run('echo  "%s;%s" |%s/bin/mongo %s:%s/admin --shell' % (configOrder,initOrder,mongoHomeDir, localIP, port))
        '''    print yellow("create /tmp/a.txt...")
            run("echo '%s' >/tmp/a.txt" % configOrder)
            run("echo '%s' >> /tmp/a.txt" % initOrder)'''
# 配置密码
@runs_once
@roles('mongodb')
def changeMongoconfigure(flag):
    mongoHomeDir='/data/apps/mongodb'
    localIP = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
    port = 27011
    mongoConfigureFile = '/etc/mongodb.conf'
    print yellow("enable replication in mongodb configure file...")
    #flag=1 ,then will Configure encryption
    if flag==1:
        print yellow("enable security conf in mongodb configure file...")
        run("sed 's/\#//' %s" % mongoConfigureFile)
        run('''echo 'use admin;db.createUser({user: "apimongoadmin",pwd: "YZb4ce5L9o8n",roles:[ "clusterAdmin","userAdminAnyDatabase","dbAdminAnyDatabase","readWriteAnyDatabase"]})' |%s/bin/mongo %s:%s/admin --shell''' % (mongoHomeDir, localIP, port))
@roles('mongodb')
def stop_all_mongodb():
    pass
@roles('mongodb')
def start_all_mongodb():
    pass
'''
当mongo_num=1
当mongo_num>1
启动所有mongo(不能在这个方法里调用其他的配置函数)之后
配置副本集（执行一次run_once）
当mongo副本初始化完成后，
配置账户密码
停止所有mongo
上传秘钥文件
修改配置文件
启动所有mongo
'''