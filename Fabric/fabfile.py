#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:fabfile.py
@time:2017/2/14 0014 13:39
"""
"""
remote installation of the entry file
"""
import sys
sys.path.append('.')
from fabric.colors import *
from fabric.api import *
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)
import common
import time
#define the variables
#env.hosts = ['10.10.20.59',]
env.password = '123456'
env.user = 'root'
#env.gateway = ''
env.locatDir = '/data/tools'
env.remoteDir = '/data/tools'
env.appsDir = '/data/apps'
env.workspaceDir = '/data/workspace'
env.scriptsDir = '/data/sh'
# use this user you must add it to Fortress machine first
env.homeOwner = 'jumpserver'
# grouping the hosts
env.roledefs = {
    'tomcat': [],
    'jdk': [],
    'mysql': [],
    'mongodb': [],
    'zookeeper':[],
    'python':[],
    'iftop':[],
    'iotop':[],
    'mq':[],
    'zabbix':[],
    'kafka':[],
}
# get the number of hosts within the cluster
env.kafkaNum = len(env.roledefs['kafka']) if env.roledefs.has_key('kafka') else 0
env.mongoNum = len(env.roledefs['mongodb']) if env.roledefs.has_key('mongodb') else 0
env.zookeeperNum = len(env.roledefs['zookeeper']) if env.roledefs.has_key('zookeeper') else 0
env.mongoList = []
env.zookeeperPrivateIP = []
@task
def getHelp(item):
    if item == 'order':
        pass
    elif item == 'install':
        print "execute a method with parameters：fab install_tomcatAndJdk:'jdk'"
    elif item == 'get':
        pass
    elif item == 'put':
        pass

@task
@roles('iotop')
def install_iotop():
    javaIndexName = 'iotop'
    jdkInstallationPackage = common.getInstallationPackageName(javaIndexName)
    with hide('running','stdout'):
        try:
            # uplad iotop installation package
            common.uploadFiles(env.locatDir, env.remoteDir, jdkInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress iotop'tar package
            common.uncompressFile(env.remoteDir, javaIndexName, env.appsDir, moveFlag=2)
        except Exception,e:
            print 'file not exits!!!',str(e)
        with cd(env.remoteDir + '/' +javaIndexName):
            run("python setup.py build")
            run("python setup.py install")

@task
@roles('jdk')
def install_jdk(indexName):
    # can be used to install tomcat,jdk,activeMQ
    javaIndexName = indexName
    javaHomeDir = env.appsDir + '/' + javaIndexName
    javaHomeName = indexName.upper() + '_HOME'
    jdkInstallationPackage = common.getInstallationPackageName(javaIndexName)
    with hide('running','stdout'):
        try:
            # uplad jdk installation package
            common.uploadFiles(env.locatDir, env.remoteDir, jdkInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress jdk'tar package
            common.uncompressFile(env.remoteDir, javaIndexName, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
        # configure jdk environment variable
        common.configureEnvironmentVariable(javaHomeName, javaHomeDir)


def install_cronolog():
    cronologIndexName = 'cronolog'
    cronologDir = env.remoteDir+ '/' + cronologIndexName
    cronologInstallationPackage = common.getInstallationPackageName(cronologIndexName)
    common.uploadFiles(env.locatDir, env.remoteDir, cronologInstallationPackage)
    common.uncompressFile(env.remoteDir, cronologIndexName, env.appsDir, moveFlag=2)
    with cd(cronologDir):
        run("./configure --prefix=/data/apps/cronolog && make && make install")
    run(''' sed -i '/touch "$CATALINA_OUT"/s/^/#/' /data/apps/tomcat/bin/catalina.sh ''')
    run(""" sed -i '383s/ start / start 2\>\&1 /'  /data/apps/tomcat/bin/catalina.sh """)
    run(""" sed -i '392s/ start / start 2\>\&1 /'  /data/apps/tomcat/bin/catalina.sh """)
    run(""" sed -i '/"$CATALINA_OUT" 2>&1/d' /data/apps/tomcat/bin/catalina.sh """)
    run("""  sed -i '/start 2/a\   |/data/apps/cronolog/sbin/cronolog "$CATALINA_BASE/logs/catalina-%Y-%m-%d.out" >>/dev/null &' /data/apps/tomcat/bin/catalina.sh  """)

def install_tomcat_apr():
    package_list = ['apr-1.5.2.tar.gz','apr-util-1.5.4.tar.gz','apr-iconv-1.2.1.tar.gz']
    common.uploadFiles(env.locatDir, env.remoteDir, package_list)
    for i in range(len(package_list)):
        common.uncompressFile(env.remoteDir, package_list[i], env.appsDir, moveFlag=2)
    with cd(env.remoteDir+'/'+'apr'):
        run("./configure --prefix=/data/apps/apr && make && make install")
    with cd(env.remoteDir+'/'+'apr-util'):
        run("./configure --prefix=/data/apps/apr-util --with-apr=/data/apps/apr/bin/apr-1-config && make && make install")
    with cd(env.remoteDir+'/'+'apr-iconv'):
        run("./configure --prefix=/data/apps/apr-iconv --with-apr=/data/apps/apr/bin/apr-1-config && make && make install")
    with cd('/data/apps/tomcat/bin'):
        run("tar zxf tomcat-native.tar.gz")
        with cd('tomcat-native-1.1.33-src/jni/native/'):
            run("./configure --prefix=/data/apps/apr --with-java-home=/data/apps/jdk --with-apr=/data/apps/apr/bin/apr-1-config && make && make install")
    with cd('/data/apps/tomcat/bin'):
        run(""" sed -i '/# OS specific /a\JAVA_OPTS="$JAVA_OPTS -server -Xms1024m -Xmx1024m -XX:PermSize=256M -XX:MaxPermSize=256M -XX:ParallelGCThreads=8 -XX:+UseConcMarkSweepGC -Duser.timezone=GMT+08 -XX:+HeapDumpOnOutOfMemoryError  -XX:HeapDumpPath=/data/logs/tomcatoomlog/oom.hprof"' catalina.sh """)
        run(""" sed -i '/# OS specific /a\CATALINA_OPTS="$CATALINA_OPTS -Djava.library.path=/data/apps/apr/lib"' catalina.sh  """)

@task
@roles('tomcat')
def install_tomcat(indexName):
    tomcatIndexName = indexName
    tomcatHomeDir = env.appsDir + '/' + tomcatIndexName
    tomcatHomeName = indexName.upper() + '_HOME'
    tomcatInstallationPackage = common.getInstallationPackageName(tomcatIndexName)
    with hide('running','stdout'):
        try:
            # uplad jdk installation package
            common.uploadFiles(env.locatDir, env.remoteDir, tomcatInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress jdk'tar package
            common.uncompressFile(env.remoteDir, tomcatIndexName, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
        # configure jdk environment variable
        common.configureEnvironmentVariable(tomcatHomeName, tomcatHomeDir)
        # intall cronolog
        install_cronolog()
        install_tomcat_apr()

@task
@roles('mq')
def install_mq(indexName):
    # can be used to install tomcat,jdk,activeMQ
    javaIndexName = indexName
    javaHomeDir = env.appsDir + '/' + javaIndexName
    javaHomeName = indexName.upper() + '_HOME'
    jdkInstallationPackage = common.getInstallationPackageName(javaIndexName)
    with hide('running','stdout'):
        try:
            # uplad jdk installation package
            common.uploadFiles(env.locatDir, env.remoteDir, jdkInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress jdk'tar package
            common.uncompressFile(env.remoteDir, javaIndexName, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
        # configure jdk environment variable
        common.configureEnvironmentVariable(javaHomeName, javaHomeDir)

@task
@roles('kafka')
def install_kafka():
    #zookeeper_list=' 先执行安装zookeeper,可以获取所有内网ip'
    zookeeper_list = ','.join([x+':2181' for x in env.zookeeperPrivateIP])
    kafkaIndexName = 'kafka'
    kafkaHomeDir = env.appsDir + '/' + kafkaIndexName
    kafkaHomeName = 'KAFKA_HOME'
    kafkaDataDir = common.perfectDir(env.workspaceDir) + 'kafkaData'
    kafkaInstallationPackage = common.getInstallationPackageName(kafkaIndexName)
    with hide('running','stdout'):
        try:
            common.uploadFiles(env.locatDir, env.remoteDir, kafkaInstallationPackage)
        except Exception,e:
            print 'directory or file not exit!!!',str(e)
        try:
            common.uncompressFile(env.remoteDir, kafkaIndexName, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
    # configure kafka
        with cd(kafkaHomeDir):
            localPrivateIP = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
            run("sed -i '/#host.name/a\host.name=%s' config/server.properties " % localPrivateIP)
            run("sed -i '/^log.dirs/s/=.*$/=%s/' config/server.properties"% kafkaDataDir.replace('/','\/'))
            env.kafkaNum -= 1
            if env.kafkaNum >= 0:
                run("sed -i '/broker.id/s/=.*$/=%s/' config/server.properties" % env.kafkaNum)
                run("sed -i '/zookeeper.connect=/s/=.*$/=%s/' config/server.properties " % zookeeper_list)
    # configure environment of kafka
        common.configureEnvironmentVariable(kafkaHomeName, kafkaHomeDir)
    # create kafka dir
        run("mkdir -p %s" % kafkaDataDir)

# 安装并启动所有mongodb
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
        run('%s/bin/mongod -f %s ' %(mongoHomeDir,mongoConfigurationFile))
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
@runs_once
@roles('mongodb')
def configureMongoCluster(flag):
    mongoHomeDir='/data/apps/mongodb'
    # 需要安装Python2.7来用此命令获取ip
    localIP = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
    port = 27011
    mongoConfigureFile = '/etc/mongodb.conf'
    if env.mongoNum>1:
        idList = ''
        for i in range(len(env.mongoList)):
            idList += ' {_id:%s,host:"%s:%s"},' % (i,env.mongoList[i],port)
        configOrder = 'config = {_id:"repset", members:[ %s ]}'   % idList.rstrip(',')
        initOrder = 'rs.initiate(config);'
        print 'configOrder: ',configOrder
        print yellow("initiate mongodb replication...")
        # run('cat /tmp/a.txt |%s/bin/mongo %s:%s/admin --shell' % (mongoHomeDir,localIP,port))
        #echo中的命令要使用单引号
        run("echo  '%s;%s' |%s/bin/mongo %s:%s/admin --shell" % (configOrder,initOrder,mongoHomeDir, localIP, port))

    #flag=1 ,then will Configure encryption
    time.sleep(20)
    if flag==1:
        print yellow("enable security conf in mongodb configure file...")
        run("sed 's/\#//' %s" % mongoConfigureFile)
        if env.mongoNum >1:
            # 获取主节点ip+port
            primaryip = run(''' echo 'rs.status()' |mongo %s:%s| grep -B3 PRIMARY| grep name |awk -F'"' {'print $4'} '''%(localIP,port))
            conn = primaryip
        elif env.mongoNum ==1:
            conn = localIP + ':' + port
        # 字符串里面不要有双引号，否则Python执行时会变成\".
        create_mongo_user_cmd = r"db.createUser({user: 'apimongoadmin',pwd: 'YZb4ce5L9o8n',roles:[ 'clusterAdmin','userAdminAnyDatabase','dbAdminAnyDatabase','readWriteAnyDatabase']})"
        run('echo -e \"use admin;\n{}\" |{}/bin/mongo {}/admin '.format(create_mongo_user_cmd, mongoHomeDir, conn))


@roles('mongodb')
def stop_all_mongodb():
    mongo_pid = run("ps aux | grep mongodb.conf | grep -v grep |awk '{print $2}'")
    if len(mongo_pid) >0:
        run("kill {}".format(mongo_pid))
@roles('mongodb')
def start_all_mongodb():
    mongoHomeDir='/data/apps/mongodb'
    mongoConfigureFile = '/etc/mongodb.conf'
    mongo_pid = run("ps aux | grep mongodb.conf | grep -v grep |awk '{print $2}'")
    if len(mongo_pid) >0:
        run("kill {}".format(mongo_pid))
    elif len(mongo_pid)==0:
        run('%s/bin/mongod -f %s ' % (mongoHomeDir, mongoConfigureFile))

@task
@roles('mysql')
def install_mysql():
    mysqlIndexName = 'mysql'   # also mysql user name
    mysqlHomeDir = env.appsDir + '/' + mysqlIndexName
    mysqlUncompressDir = common.perfectDir(env.remoteDir) + mysqlIndexName
    mysqlHomeName = 'MYSQL_HOME'
    mysqlDataDir = common.perfectDir(env.workspaceDir) + 'mysqlData'
    mysqlConfigurationFile = 'my.cnf'
    mysqlInstallationPackage = common.getInstallationPackageName(mysqlIndexName)
    with hide('running','stdout'):
        try:
            common.uploadFiles(env.locatDir, env.remoteDir, mysqlInstallationPackage)
        except Exception,e:
            print 'directory or file not exit!!!',str(e)
        try:
            common.uncompressFile(env.remoteDir, mysqlIndexName, env.appsDir, moveFlag=2)
        except Exception,e:
            print 'file not exits!!!',str(e)
        # yum install gcc
        with settings(warn_only=True):
            print yellow("yum some packages")
            run("yum -y install  gcc gcc-c++ gcc-g77 autoconf automake zlib* fiex* libxml* ncurses-devel libtool-ltdl-devel* make cmake library  bison-devel")
            print yellow('add user of mysql')
            run("groupadd %s && useradd -s /sbin/nologin -g %s -M %s"  %(mysqlIndexName,mysqlIndexName,mysqlIndexName))
            print yellow("mkdir some dirs for mysql ")
            run("mkdir -p %s/logs && mkdir -p %s" % (mysqlHomeDir, mysqlDataDir))
            run("test -f '/etc/my.cnf' && mv /etc/my.cnf /etc/my.cnf-bak ||echo 'my.cnf not exit' ")
        print yellow("compile mysql")
        with cd(mysqlUncompressDir):
            print yellow("cmake mysql")
            run("cmake \
-DMYSQL_USER=%s \
-DCMAKE_INSTALL_PREFIX=%s \
-DMYSQL_DATADIR=%s \
-DMYSQL_UNIX_ADDR=%s/mysql.sock \
-DSYSCONFDIR=%s \
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
-DWITH_READLINE=1" %(mysqlIndexName,mysqlHomeDir,mysqlDataDir,env.appsDir,mysqlHomeDir))
            print yellow("make mysql")
            run("make")
            print  yellow("make install mysql")
            run("make install")
            print yellow("initialize mysql")
        run("%s/scripts/mysql_install_db  --datadir=%s --user=%s --basedir=%s"%(mysqlHomeDir,mysqlDataDir,mysqlIndexName,mysqlHomeDir))
        common.changePermissions(mysqlHomeDir, ownerName='mysql', ownerGroup='mysql')
        print yellow("configure mysql")
        run("cp %s/support-files/mysql.server /etc/init.d/mysql" % mysqlHomeDir)
        run("cp %s/bin/mysql /bin/" % mysqlHomeDir)
        run('sed -i "/\[mysqld\]/a\datadir=%s" %s/my.cnf' % (mysqlDataDir.replace('/','\/'), mysqlHomeDir))
        run('sed -i "/\[mysqld\]/a\log_error=%s/logs/error.log" %s/%s' % (
        mysqlHomeDir.replace('/','\/'), mysqlHomeDir,mysqlConfigurationFile))
        run('sed -i "/\[mysqld\]/a\socket=%s/mysql.sock" %s/%s' % (
        mysqlHomeDir.replace('/','\/'), mysqlHomeDir,mysqlConfigurationFile))
        run('sed -i "1 i\\[client\]" %s/%s' % (mysqlHomeDir,mysqlConfigurationFile))
        run('sed -i "/\[client\]/a\socket=%s/mysql.sock" %s/%s' % (
        mysqlHomeDir.replace('/','\/'), mysqlHomeDir,mysqlConfigurationFile))
        run("chkconfig mysql on")
        # configure mysql environment
        print yellow("configure mysql environment")
        common.configureEnvironmentVariable(mysqlHomeName, mysqlHomeDir)

@task
@roles('zookeeper')
def get_zookeeper_private_ip():
    local_ip = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
    env.zookeeperPrivateIP.append(local_ip)

@task
@roles('zookeeper')
def install_zookeeper():
    # can be used to install zookeeper
    # depend on function get_zookeeper_private_ip
    zookeeperIndexName = 'zookeeper'
    zookeeperHomeDir = env.appsDir + '/' + zookeeperIndexName
    zookeeperHomeName = 'ZOOKEEPER_HOME'
    zookeeperDataDir = env.workspaceDir + '/' + 'zkDatadir'
    zookeeperInstallationPackage = common.getInstallationPackageName(zookeeperIndexName)
    with hide('running','stdout'):
        try:
            # uplad zookeeper installation package
            common.uploadFiles(env.locatDir, env.remoteDir, zookeeperInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress zookeeper'tar package
            common.uncompressFile(env.remoteDir, zookeeperIndexName, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
        # configure zookeeper
        print yellow("configure zookeeper")
        myid = 3
        local_ip = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
        run("mkdir -p %s" % zookeeperDataDir)
        with cd("%s/conf" % zookeeperHomeDir):
            run("cp zoo_sample.cfg zoo.cfg")
            run("sed -i '/dataDir=/s/=.*/=%s/' zoo.cfg" % zookeeperDataDir.replace('/','\/'))
            if env.zookeeperNum >1:
                for i in range(env.zookeeperNum):
                    run("sed -i '/dataDir=/a\server.%s=%s:2888:3888' zoo.cfg " % (myid, env.zookeeperPrivateIP[i]))
                    if env.zookeeperPrivateIP[i] == local_ip:
                        run("echo %s >%s/myid" % (myid,zookeeperDataDir))
                    myid -=1

        # configure zookeeper environment variable
        common.configureEnvironmentVariable(zookeeperHomeName, zookeeperHomeDir)

@task
@roles('python')
def install_python():
    print yellow("yum some parket of python")
    pythonHomeDir = env.appsDir + '/python'
    pythonHomeName = 'PYTHON_HOME'
    run('yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel')
    pythonInstallPackage = common.getInstallationPackageName('python')
    common.uploadFiles(env.locatDir, env.remoteDir, pythonInstallPackage)
    common.uncompressFile(env.remoteDir, 'python', env.appsDir, moveFlag=2)
    print yellow("compile and install python")
    with cd(env.remoteDir + '/python'):
        run("./configure --prefix=%s && make && make install " % pythonHomeDir)
    print yellow("link python to /usr/bin/")
    with cd('/usr/bin'):
        run('mv python python-bak')
        run('ln -s %s/bin/python /usr/bin/python' % pythonHomeDir)
        run("sed -i '1s/$/2.6/' yum ")
    # configure python environment variable
    print yellow("configure python environment variable")
    common.configureEnvironmentVariable(pythonHomeName, pythonHomeDir)
@task
@roles('iftop')
def install_iftop():
    # can be used to install iftop
    iftopIndexName = 'iftop'
    iftopHomeDir = env.appsDir + '/' + iftopIndexName
    iftopHomeName = iftopIndexName.upper() + '_HOME'
    iftopInstallationPackage = common.getInstallationPackageName(iftopIndexName)
    with hide('running','stdout'):
        try:
            # uplad iftop installation package
            common.uploadFiles(env.locatDir, env.remoteDir, iftopInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress iftop'tar package
            common.uncompressFile(env.remoteDir, iftopIndexName, env.appsDir, moveFlag=2)
        except Exception,e:
            print 'file not exits!!!',str(e)
        print yellow("yum some package of iftop")
        run("yum install -y libpcap-devel ncurses-devel")
        print yellow("compile iftop and install iftop")
        with cd(env.remoteDir + '/' + iftopIndexName):
            run("./configure --prefix=%s && make && make install" % iftopHomeDir)
        # configure iftop environment variable
        common.configureEnvironmentVariable(iftopHomeName, iftopHomeDir, scriptDir='sbin')
        # create network monitor script
        run("mkdir -p %s/networkLog" % env.workspaceDir)
        local_hostname = run("cat /etc/sysconfig/network  |grep HOSTNAME |cut -d '=' -f2")
        """
        run("
cat >%s/networkFlowStatistic.sh<<EOF
#!/bin/bash
set -e
#set -x
LOCAL_DATE=`date +%F`
TOWDAYSAGO=`date +%F -d "-2 day"`
echo `date` >>%s/networkLog/${LOCAL_DATE}_%s.log
%s/sbin/iftop -Pp -Nn -t -L 30 -s 1 >>%s/networkLog/${LOCAL_DATE}_%s.log
rm -fr %s/networkLog/${TOWDAYSAGO}_%s.log
EOF
" % (env.scriptsDir,env.workspaceDir,local_hostname,iftopHomeDir,env.workspaceDir,local_hostname,env.workspaceDir,local_hostname))
        run("echo '* * * * * sh /data/sh/networkFlowStatistic.sh' >> /var/spool/cron/root")

"""
@task
def install_supervisor():
    pass
@task
@roles('zabbix')
def install_zabbix_agentd():
    zabbixServer = '124.243.248.98'
    zabbixActiveServer = '124.243.248.109'
    zabbixConfigureFile = '/etc/zabbix/zabbix_agentd.conf'
    local_hostname = run("cat /etc/sysconfig/network| grep HOSTNAME|awk -F= '{print $2}'")
    print yellow("Install zabbix agent...")
    zabbix_agentd_rpm = ['zabbix-agent-3.2.1-1.el6.x86_64.rpm']
    common.uploadFiles(env.locatDir, env.remoteDir, zabbix_agentd_rpm)
    with cd(env.remoteDir):
        run("rpm -ivh %s" % zabbix_agentd_rpm[0])
    # Configuration the zabbix
    run(" sed -i '/^Server=/s/=.*$/=%s/' %s" % (zabbixServer,zabbixConfigureFile))
    run(" sed -i '/^ServerActive=/s/=.*$/=%s/' %s" % (zabbixActiveServer, zabbixConfigureFile))
    run(" sed -i '/^Hostname=/s/=.*$/=%s/' %s" % (local_hostname, zabbixConfigureFile))
    run(" sed -i '/UnsafeUserParameters/s/0/1/' %s" % (zabbixConfigureFile))
    run(" sed -i '/UnsafeUserParameters/s/# //' %s" % ( zabbixConfigureFile))
    run("echo 'Timeout=30' >> %s" % zabbixConfigureFile)
    run("/etc/init.d/zabbix-agent start")
    run("chkconfig zabbix-agent on")

@task
@roles('nginx')
def install_nginx():
    # neet install pcre and nginx
    print yellow("yum some packages of nginx")
    with settings(warn_only=True):
        run("yum install -y zlib-devel openssl openssl-devel gd keyutils patch perl mhash")
    nginxInstallPackage = [common.getInstallationPackageName('nginx'), common.getInstallationPackageName('pcre')]
    common.uploadFiles(env.locatDir, env.remoteDir, nginxInstallPackage)
    common.uncompressFile(env.remoteDir, 'pcre', env.appsDir, moveFlag=2)
    common.uncompressFile(env.remoteDir, 'nginx', env.appsDir, moveFlag=2)
    print yellow('compile pcre')
    with cd(env.remoteDir+'/pcre'):
        run("./configure --prefix=%s && make && make install" % (env.appsDir + '/pcre'))
    print yellow("compile nginx")
    with cd(env.remoteDir + '/nginx'):
        run("./configure --prefix=%s --with-http_stub_status_module --with-http_ssl_module --with-http_gzip_static_module --with-pcre=%s --with-http_realip_module" % (
            env.appsDir+'/nginx', env.remoteDir + '/pcre'))
        run("make && make install")


@task
@roles('jdk')
def create_lvm(disk):
    run('pvcreate /dev/%s' % disk)
    run('vgcreate vg01 dev/%s' % disk)
    run('lvcreate -L 1023G -n lv1 vg01')
    run('mkfs.ext4 -T largefile /dev/mapper/vg01-lv1')
    run('mkdir -p /data && mount /dev/mapper/vg01-lv1  /data ')
    run('echo "/dev/mapper/vg01-lv1 /data ext4 defaults  0 0" >> /etc/fstab')

@task
@roles('jdk')
def format_disks():
    diskList = ['sdc']
    for i in range(len(diskList)):
        print yellow("format disk %s" % diskList[i])
        run("""
        cat >/tmp/fdiskcmd.txt<<EOF
n
p
1


w
        EOF
        """)
        run("fdisk /dev/%s < /tmp/fdiskcmd.txt" % diskList[i])
        run("mkfs.ext4 -T largefile /dev/%s1" % diskList[i])
        if len(diskList) ==1:
            run("mkdir -p /data && mount /dev/%s1  /data" % diskList[i])
            run("echo '/dev/%s1 /data ext4 defaults  0 0'>> /etc/fstab" % diskList[i])
        else:
            run("mkdir -p /%sdata && mount /dev/%s1  /%sdata" % (diskList[i],diskList[i],diskList[i]))
            run("echo '/dev/%s1 /%sdata ext4 defaults  0 0'>> /etc/fstab" % (diskList[i],diskList[i]))

@task
@roles('jdk')
def install_autojump():
    # can be used to install tomcat,jdk,activeMQ
    autojumpIndex = 'autojump'
    javaHomeDir = env.appsDir + '/' + autojumpIndex
    autojumpInstallationPackage = common.getInstallationPackageName(autojumpIndex)
    with hide('running','stdout'):
        try:
            # uplad jdk installation package
            common.uploadFiles(env.locatDir, env.remoteDir, autojumpInstallationPackage)
        except Exception,e:
            print 'directory or file not exits!!!',str(e)
        try:
            # uncompress jdk'tar package
            common.uncompressFile(env.remoteDir, autojumpIndex, env.appsDir)
        except Exception,e:
            print 'file not exits!!!',str(e)
        run(' . /etc/profile && python /data/tools/autojump/install.py ')
        # run(" echo '[[ -s /home/jumpserver/.autojump/etc/profile.d/autojump.sh ]] && source /home/jumpserver/.autojump/etc/profile.d/autojump.sh'>>/home/jumpserver/.bashrc ")


@task
@roles('jdk')
def system_initialization():
    # azure VM  need to change dns
    changeDNSflag = 1
    with settings(warn_only=True):
        print yellow("yum some packages")
        run("yum install -y libselinux-python net-snmp* git bzip-devel lrzsz  wget gcc gcc-c++ ftp lftp openssl-devel libffi-devel python-devel openssl-devel PyYAML  libyaml  vim zlib zlib-devel openssh-clients  ntpdate")
        run("mkdir -p /data/{apps,workspace,sh,tools,logs,jar}")
        print yellow("time synchronization")
        run("echo '15 1 * * * /usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1' >> /var/spool/cron/root")
        run("\\cp -f  /usr/share/zoneinfo/Asia/Shanghai /etc/localtime")
        run("/usr/sbin/ntpdate pool.ntp.org; hwclock -w >/dev/null 2>&1")
        print yellow("config iptables selinux")
        run("/etc/init.d/iptables stop")
        run("chkconfig iptables off")
        run("/usr/sbin/setenforce 0")
        run("sed -i '7s/enforcing/disabled/' /etc/sysconfig/selinux")
        print yellow("put file nmon pwaiwang...")
        scriptsfilelist=['pwaiwang','nmon']
        common.uploadFiles(env.locatDir, '/sbin', scriptsfilelist)
        run("chmod +x /sbin/%s" % scriptsfilelist[0])
        run("chmod +x /sbin/%s" % scriptsfilelist[1])

@task
@roles('jdk')
def create_root_password():
    print yellow("create root passwd")
    # if you are general user please use order 'sudo'
    sudo("echo '123456' | passwd --stdin root")
    sudo("useradd %s" % env.homeOwner)

@task
# hosts of aliyun neet to change hostname
def configureHosts():
    print yellow("will add hosts")
    run("""
    cat >>/etc/hosts <<EOF
10.10.20.59 centos2
10.10.20.58 centos1
    EOF
    """ )
    local_ip = run("python -c 'import socket;print socket.gethostbyname(socket.gethostname())'")
    local_hostname = run("sed -n '/%s/p' /etc/hosts |awk '{print $2}'" % local_ip)
    run("sed -i '/HOSTNAME/s/HOSTNAME=.*/HOSTNAME=%s/' /etc/sysconfig/network " % local_hostname)
    run("hostname %s" %local_hostname)

#execute remote shell commands
@task
def execCommand(shellCmd):
    with hide('running'):
        common.executeRemoteCommands(shellCmd)

 #组合执行具体任务示例

@task
def go():
    with hide('running','stdout'):
        execute(create_root_password)
        # format_disks 和create_lvm 只能二选一
        execute(format_disks)
        execute(create_lvm,'sdc')
        execute(system_initialization)
        execute(install_jdk, 'jdk')    # with parameter of 'jdk'
        execute(install_tomcat,'tomcat')
        execute(install_mq,'activemq')
        # 先执行get_zookeeper_private_ip，获取zookeeper内网ip，然后install_zookeeper，然后install_kafka
        execute(get_zookeeper_private_ip)
        execute(install_zookeeper)
        execute(install_kafka)
        # 安装mongo需要4个步骤
        execute(install_mongo)
        execute(configureMongoCluster,1)
        execute(stop_all_mongodb)
        execute(start_all_mongodb)
        execute(install_zabbix_agentd)
        execute(install_iftop)
        execute(install_iotop)
        execute(install_mysql)
        execute(install_python)

logging.debug('fabfile end')