#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:a.py
@time:2017/5/17 0017 15:36
"""
import pymongo
import pprint
import re
import datetime
mongo_config = {
    'host':'10.0.1.35',
    'port':27014,
}
def search_mongo():
    apicodelist = ['mobilecheck', 'mobilecheck_tc', 'mobilecheck_ty', 'mobilecheck_yst']
    flaglist = ['500','502']
    mongoConn = pymongo.MongoClient(**mongo_config)
    adminMongodb = mongoConn['admin']
    adminMongodb.authenticate('apimongoadmin','YZb4ce5L9o8n')
    db = mongoConn['apiservice']
    collection = db['reqtimehis_2017-05-17']
    #print collection.count()
    a =  collection.find({"$and":[{"apicode":{"$in":apicodelist}},{"flag":{"$in":flaglist}}]})

    #lastPhone = [x for x in a]
    #print lastPhone
    for i in a:
        print i
try:
    search_mongo()
except Exception,e:
    print e

'''
获取时间的操作
t = i['urs'].encode('utf-8')
res = re.split(r'[-,\s,:,.]',t)
tt = [int(x) for x in res]
print datetime.datetime(*tt)
'''