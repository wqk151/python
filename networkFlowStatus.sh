#!/bin/bash
set -x
set -e
#__date__=2017/2/7 0007 8:56

#set -x
LOCAL_DATE=`date +%F`
TOWDAYSAGO=`date +%F -d "-2 day"`

echo `date` >>/data/workspace/networkLog/${LOCAL_DATE}_web3_network.log
/data/apps/iftop/sbin/iftop -Pp -Nn -t -L 30 -s 1 >>/data/workspace/networkLog/${LOCAL_DATE}_web3_network.log
#/usr/sbin/nethogs -d 1 >> /data/workspace/networkLog/${LOCAL_DATE}_web3_network.log
for ((i=1;i<6;i++))
do
   localPort = `${LOCAL_DATE}_web3_network.log | grep -A 13 $(date) | grep '^   2'  |awk '{print $2}'  | awk -F':' '{print $2}'`
   portNum = `netstat -anltp | grep $localPort  |wc -l`
   if [ $portNum -eq 1 ];then
        PID = `netstat -anltp | grep $localPort |awk '{print $NF}'  | awk -F'/' '{print $1}'`
        program = `ps aux | grep $PID | grep -v grep`
        sed -i '/$PID/s/$/${program}/' ${LOCAL_DATE}_web3_network.log
   fi
done

echo " " >>/data/workspace/networkLog/${LOCAL_DATE}_web3_network.log
echo "" >>/data/workspace/networkLog/${LOCAL_DATE}_web3_network.log
rm -fr /data/workspace/networkLog/${TOWDAYSAGO}_web3_network.log
