#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:mongodb_discovery.py
@time:2016/11/25 0025 14:57
"""
#This script is used to discovery disk on the server
import subprocess
import json
args='''awk -F':' '{print $1":"$2}' /data/sh/mongodb_servers'''
t=subprocess.Popen(args,shell=True,stdout=subprocess.PIPE).communicate()[0]
mongodbs=[]

for mongo in t.split('\n'):
    if len(mongo) != 0:
       mongodbs.append({'{#MONGO_HOST}':mongo})
print json.dumps({'data':mongodbs},indent=4,separators=(',',':'))