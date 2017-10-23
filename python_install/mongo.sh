#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/12"
#__time__="16:31"
source common.sh
if [ ! -d /data/apps/mongo ];then
    mkdir -p ${WORKSPACE_DIR}mongo
    cd ${SOFTWARE_DIR}  && tar zxf mongo.tar.gz
	mv mongo $APP_DIR
fi


#env
MONGODB_HOME_NUM=$(sed -n '/MONGODB_HOME/p' /etc/profile  |wc -l)
if [ $MONGODB_HOME_NUM == 0 ];then
PATH_NUM=$(sed -n '/^PATH=\$/p' /etc/profile  |wc -l)
	if [ $PATH_NUM == 0 ];then
		echo "MONGODB_HOME=${APP_DIR}mongo"  >> /etc/profile
		echo "PATH=\$PATH:\$HOME/bin:\$MONGODB_HOME/bin"  >> /etc/profile
		echo "export PATH MONGODB_HOME" >>/etc/profile
	else
		sed -i '/^PATH=/i\MONGODB_HOME='${APP_DIR}'mongo' /etc/profile
		sed -i '/^PATH\=\$/s/$/\:\$MONGODB_HOME\/bin/'  /etc/profile
		sed -i '/^export/s/$/ MONGODB_HOME/' /etc/profile

	fi

. /etc/profile

mongod --fork --port 27011 --dbpath=/data/workspace/mongo/ --logpath=/data/workspace/mongo/mongodb.log  --logappend
fi

