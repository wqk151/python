#!/bin/bash
set -x
set -e
#__date__=2016/11/24 0024 9:00
#echo "db.serverStatus()"   |/data/apps/mongo/bin/mongo 192.168.0.6:27011/admin -u apimongoadmin -p  YZb4ce5L9o8n
MONGOPATH="/data/apps/mongo/bin/mongo"
HOST="192.168.0.6"
AUTH_DB="admin"
PORT="27011"
USERNAME="apimongoadmin"
PASSWORD="YZb4ce5L9o8n"
MONGO_CONN=`echo "db.serverStatus()"  | ${MONGOPATH} ${HOST}:${PORT}/${AUTH_DB} -u ${USERNAME} -p ${PASSWORD}`
if [[ $# == 1 ]];then
pass
result =
echo "" >>file


sed


rm -fr file
fi