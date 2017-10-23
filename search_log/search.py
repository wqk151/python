#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:search.py
@time:2017/5/17 0017 15:18
"""
import sys
import datetime
import pymongo
import pprint
import MySQLdb as mysqldb
import subprocess
import os
import ConfigParser
'''
python search.py apicode:mobilecheck time:02:29
python search.py apicode:mobilecheck
'''

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
search_log_func_dir = os.path.join(BASE_DIR,'searchTomcatLog.py')
conf_file = os.path.join(BASE_DIR,'conf.ini')
argumentNum = len(sys.argv)
if argumentNum == 3:
    timearg = sys.argv[2]
    search_time = timearg.split(':')[1:]
    search_time = ':'.join(search_time)
elif argumentNum ==2:
    search_time = ''
else:
    print 'must gave one argument at least'
arg = sys.argv[1]
#firstFlag = arg if ':' not in arg else arg.split(':')[0].lower()
if ':' in arg:
    firstFlag = arg.split(':')[0].lower()
    searchArgument = arg.split(':')[1]
else:
    firstFlag = arg


conf = ConfigParser.ConfigParser()
conf.read(conf_file)
mysql_config = {
    'host':conf.get('mysql','host'),
    'port':conf.getint('mysql','port'),
    'user':conf.get('mysql','user'),
    'passwd':conf.get('mysql','passwd'),
    'db':conf.get('mysql','db'),
    'charset':conf.get('mysql','charset'),
}
mongo_config = {
    'host':conf.get('mongo','host'),
    'port':conf.getint('mongo','port'),
}
# 获取全部的apicode (multiport来判断是否有多个接口，主副接口)
def search_mysql(apicode):
    conn = mysqldb.connect(**mysql_config)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `API_INFO_M` WHERE `apicode` LIKE '%{}%' LIMIT 0, 1000".format(apicode))
    res = cursor.fetchall()
    apicode_list = [code[0].encode('utf-8') for code in res]
    print '\033[1;35m查询apicode:{} \033[0m'.format(apicode_list)
    return apicode_list # 返回所有apicode的列表
def search_mongo(search_time,apicodelist=None,apikey=None):
    nowtime = datetime.datetime.now()
    formatTime = nowtime.strftime('%Y-%m-%d')
    flaglist = ['500','502']    # 错误码列表
    keylist = ['name','idname','idCardName','JGDM','mobileNo','mobile']  # 用于获取参数的键的列表
    mongoConn = pymongo.MongoClient(**mongo_config)
    adminMongodb = mongoConn['admin']
    adminMongodb.authenticate('apimongoadmin','YZb4ce5L9o8n')
    db = mongoConn['apiservice']
    collection = db['reqtimehis_{}'.format(formatTime)]
    #print collection.count()
    if apicodelist != None: # 当使用apicode查询时
        a =  collection.find({"$and":[{"apicode":{"$in":apicodelist}},{"flag":{"$in":flaglist}},{"urs":{"$regex":search_time}}]})
    elif apikey != None:    # 当使用apikey查询时
        a = collection.find({"$and":[{"apikey":apikey},{"flag":{"$in":flaglist}},{"urs":{"$regex":search_time}}]})
    lastDta = [x for x in a]
    for k in range(len(keylist)):
        arguments = [d.get(keylist[k]) for d in lastDta[-3:] if d.has_key(keylist[k])]
      # 获取最后三条记录，然后获取参数
        return arguments   # 返回参数

def search_log(argument,search_time):   # 根据mongo查询得到的参数，查tomcat日志
    if type(argument) == str:
        print '\033[1;35m查询参数:{} \033[0m'.format(argument)
        p = subprocess.Popen("fab -f {} search_logs:{},{}".format(search_log_func_dir, argument,search_time), shell=True,stdout=subprocess.PIPE)
        #p.wait()
        print p.stdout.read()
        p.communicate()
    else:
        for a in argument:
            a = a.encode('utf-8').replace(' ','\ ')
            print '\033[1;35m查询参数:{} \033[0m'.format(a)
            p = subprocess.Popen("fab -f {} search_logs:{},{}".format(search_log_func_dir, a,search_time), shell=True,stdout=subprocess.PIPE)
            #p.wait()
            print p.stdout.read()
            p.communicate()

def main():
    if firstFlag == 'apicode':
        apicodelist = search_mysql(searchArgument)
        argument = search_mongo(apicodelist=apicodelist,search_time=search_time)
        search_log(argument,search_time)
    elif firstFlag =='apikey':
        argument = search_mongo(apikey=searchArgument,search_time=search_time)
        search_log(argument,search_time)
    else:
        search_log(firstFlag,search_time)

if __name__ == '__main__':
    main()