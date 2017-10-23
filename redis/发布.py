#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:发布.py
@time:2017/9/5 0005 11:19
"""
import redis
pool = redis.ConnectionPool(host='192.168.1.1',port=6379,password='123456',db=1)
r = redis.Redis(connection_pool=pool)


r.publish("fm87.7","hello  welcome to bj")