#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:mongo_migrate.py
@time:2017/2/22 0022 15:42
"""
import pymongo
import datetime
yesdate = datetime.datetime.now() - datetime.timedelta(days=1)
formalyesdate = yesdate.strftime('%Y-%m-%d')
#yes_req =  'reqtimehis_' + formalyesdate
#yes_acc = 'accounthistory_' + formalyesdate
#yes_acc = 'accounthistory_2017-08-37'
#yes_req = 'reqtimehis_2017-08-37'
newMongoConn = pymongo.MongoClient('172.16.1.5',27012)
newMongodb = newMongoConn['apiservice']
# 建立连接
oldMongoConn = pymongo.MongoClient('192.168.1.1', 27011)
oldadminMongodb = oldMongoConn['admin']
oldadminMongodb.authenticate('apimongo', '')
# 连接apiserviece库
oldMongodb = oldMongoConn['apiservice']
for i in range(19,30):
    yes_acc = 'accounthistory_2017-06-%s' % i
    yes_req = 'reqtimehis_2017-06-%s' % i
    # 建立连接
    #a = pymongo.MongoReplicaSetClient

    # 密码认证admin库
    #adminMongodb = newMongoConn['admin']
    #adminMongodb.authenticate('apimongo','')
    # 连接apiservice库

    # 连接集合
    newReqCollection = newMongodb[yes_req]
    newAccCollection = newMongodb[yes_acc]



    # 连接集合
    #oldMongoCollection = oldMongodb.get_collection('reqtimehis_2017-02-23').find({"_id":0})
    oldReqMongoCollection = oldMongodb[yes_req]
    oldAccMongoCollection = oldMongodb[yes_acc]

    # 查新mongo的reqtimehis集合
    oldReqMongodata = oldReqMongoCollection.find()
    newReqMongodata = newReqCollection.find()

    #获取所有订单号
    newreqlist = []
    for newreq in newReqMongodata:
        newreqlist.append(newreq.get('orderNo'))
    # newreqlist = (newreq.get('orderNo') for newreq in newReqMongodata)


    n = 0
    # 如果新库中没有这个订单号，将这条数据插入到新库中
    for req in oldReqMongodata:
        #newReqCollection.insert(req)
        oldorderNo = req.get('orderNo')
        if oldorderNo not in newreqlist:
            newReqCollection.insert(req)
            #print oldorderNo
            n +=1

    print '%s>>> record: '% yes_req ,n

    # 查询新mongo的accounthistory集合
    oldAccMongodata = oldAccMongoCollection.find()
    newAccMongodata = newAccCollection.find()
    newacclist = []
    for newacc  in newAccMongodata:
        newacclist.append(newacc.get('orderNo'))
    a = 0
    for acc in oldAccMongodata:
        #newAccCollection.insert(acc)
        oldaccorderno = acc.get('orderNo')
        if oldaccorderno not in newacclist:
            newAccCollection.insert(acc)
            a +=1
    print '%s>>> record: ' % yes_acc,a
