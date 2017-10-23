#!/bin/bash
# -------------------------------------------------------------------------------
# FileName:    check_mysql.sh
# Revision:    1.0
# Date:        2015/06/09
# Author:      DengYun
# Email:       dengyun@ttlsa.com
# Website:     www.ttlsa.com
# Description:
# Notes:       ~
# -------------------------------------------------------------------------------
# Copyright:   2015 (c) DengYun
# License:     GPL

# 用户名
MYSQL_USER='zabbix'

# 密码
MYSQL_PWD='123456'

# 主机地址/IP
MYSQL_HOST='127.0.0.1'

# 端口
MYSQL_PORT='3306'

# 数据连接
MYSQL_CONN="/data/apps/mysql/mysqlinstall/bin/mysqladmin --defaults-extra-file=/data/apps/mysql/mysqlinstall/my.cnf"
# 参数是否正确
if [ $# -ne "1" ];then
    echo "arg error!"
fi

# 获取数据
case $1 in
    Uptime)
        result=`${MYSQL_CONN} status|cut -f2 -d":"|cut -f1 -d"T"`
        echo $result
        ;;
    Com_update)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_update"|cut -d"|" -f3`
        echo $result
        ;;
    Slow_queries)
        result=`${MYSQL_CONN} status |cut -f5 -d":"|cut -f1 -d"O"`
        echo $result
        ;;
    Com_select)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_select"|cut -d"|" -f3`
        echo $result
                ;;
    Com_rollback)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_rollback"|cut -d"|" -f3`
                echo $result
                ;;
    Questions)
        result=`${MYSQL_CONN} status|cut -f4 -d":"|cut -f1 -d"S"`
                echo $result
                ;;
    Com_insert)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_insert"|cut -d"|" -f3`
                echo $result
                ;;
    Com_delete)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_delete"|cut -d"|" -f3`
                echo $result
                ;;
    Com_commit)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_commit"|cut -d"|" -f3`
                echo $result
                ;;
    Bytes_sent)
        result=`${MYSQL_CONN} extended-status |grep -w "Bytes_sent" |cut -d"|" -f3`
                echo $result
                ;;
    Bytes_received)
        result=`${MYSQL_CONN} extended-status |grep -w "Bytes_received" |cut -d"|" -f3`
                echo $result
                ;;
    Com_begin)
        result=`${MYSQL_CONN} extended-status |grep -w "Com_begin"|cut -d"|" -f3`
                echo $result
                ;;
    Threads_running)
        result=`${MYSQL_CONN} extended-status |grep -w "Threads_running"|cut -d"|" -f3`
                echo $result
                ;;
    Threads_connected)
        result=`${MYSQL_CONN} extended-status |grep -w "Threads_connected"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_data_reads)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_data_reads"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_data_writes)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_data_writes"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_data_fsyncs)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_data_fsyncs"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_data_read)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_data_read"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_data_written)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_data_written"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_buffer_pool_reads)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_buffer_pool_reads"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_buffer_pool_read_requests)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_buffer_pool_read_requests"|cut -d"|" -f3`
                echo $result
                ;;
    Innodb_buffer_pool_write_requests)
        result=`${MYSQL_CONN} extended-status |grep -w "Innodb_buffer_pool_write_requests"|cut -d"|" -f3`
                echo $result
                ;;
        *)
        echo "Usage:$0(Uptime|Com_update|Slow_queries|Com_select|Com_rollback|Questions|Com_insert|Com_delete|Com_commit|Bytes_sent|Bytes_received|Com_begin|Threads_running|Threads_connected|Innodb_data_reads|Innodb_data_writes|Innodb_data_fsyncs|Innodb_data_read|Innodb_data_written|Innodb_buffer_pool_reads|Innodb_buffer_pool_read_requests|Innodb_buffer_pool_write_requests)"
        ;;
esac
