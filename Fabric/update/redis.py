#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:redis.py
@time:2017/2/24 0024 9:11
"""
import redis

azure = redis.ConnectionPool(host='10.10.20.59',password='JuvcPM6JCaUqtFAS6RUL1hriAEV2yrpUb0yzzS1Eid8=')
r = redis.StrictRedis(connection_pool = azure)

print r.dbsize()