#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:订阅.py
@time:2017/9/5 0005 11:13
"""
import redis

pool = redis.ConnectionPool(host='192.168.1.1',port=6379,password='123456',db=1)
r = redis.Redis(connection_pool=pool)

pub = r.pubsub()  #打开收音机

pub.subscribe("fm87.7")  #调台

pub.parse_response()  #准备接收
print '准备监听'
data = pub.parse_response()  #正式接收

print data
