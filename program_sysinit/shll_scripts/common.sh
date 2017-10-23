#!/bin/bash
#__author__ = "Administrator"
#__date__="2016/9/9"
#__time__="16:53"
SCRIPT_DIR=/data/sh/
SOFTWARE_DIR=/data/tools/
APP_DIR=/data/apps/
SCRIPT_DIR=/data/sh/
WORKSPACE_DIR=/data/workspace/
NAGIOS_HOSTNAME='192.168.1.1'

log_record(){
	#安装日志记录,调用函数，如果有与函数中重名的变量，会改变变量的值
  if [ $? == 0 ];then
    LOG_REC_TIME=$(date +%F\ %T)
    echo OK - $LOCAL_DATE  $G_NAME:$S_NAME $1 Ok !! >>${LOG_DIR}/"$S_NAME"_install.log
  else
  	LOG_REC_TIME=$(date +%F\ %T)
    echo ERROR - $LOCAL_DATE  $G_NAME:$S_NAME $1 error!! >>${LOG_DIR}/"$S_NAME"_install.log
  fi
LOG_OK_NUM=$(cat ${LOG_DIR}/"$S_NAME"_install.log | wc -l)
}