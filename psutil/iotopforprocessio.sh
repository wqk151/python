#!/bin/bash
set -x
set -e
#__date__=2017/3/14 0014 10:57

LOCAL_DATE=`date +%F`
TOWDAYSAGO=`date +%F -d "-2 day"`
local_hostname=`cat /etc/sysconfig/network|grep HOSTNAME|cut -d'=' -f 2`
TODAY_LOG=${LOCAL_DATE}_${local_hostname}_iotop.log
TOWDAY_LOG=${TOWDAYSAGO}_${local_hostname}_iotop.log
mkdir -p /data/workspace/iotopLog/
echo `date` >>/data/workspace/iotopLog/$TODAY_LOG

/usr/bin/iotop -o -n1 -t >>/data/workspace/iotopLog/$TODAY_LOG

echo " " >>/data/workspace/iotopLog/$TODAY_LOG
echo " " >>/data/workspace/iotopLog/$TODAY_LOG
rm -fr /data/workspace/iotopLog/$TOWDAY_LOG
