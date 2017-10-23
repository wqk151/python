#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:pythonRedis.py
@time:2017/1/16 0016 17:42
"""
import redis

azureRedis = redis.ConnectionPool(host='42.159.29.38',password='HrQOuSvJZaWemwr1GFzRgXDIisrkAZSARcgd+hGRNJE=')
r = redis.StrictRedis(connection_pool=azureRedis)

localRedis = redis.ConnectionPool(host='10.10.8.132',password='HrQOuSvJZaWemwr1GFzRgXDIisrkAZSARcgd+hGRNJE=')
l = redis.StrictRedis(connection_pool=localRedis)

keysList = r.keys()

for key in keysList:
    if r.type(key) == 'hash':
        allKeyValue = r.hgetall(key)
        l.hmset(key,allKeyValue)

# 查看键的数据类型
#print r.type('userkey32')
#print r.type("userkey:payblackwarning:9fdf8ccd9ed3e26f90a1b819749ac257")
#print r.hgetall("userkey:umpay:bf3259ffb9775f17b5dd42f918b3e170")

print '********'
# 获取键值总数
print r.dbsize()
print l.dbsize()

