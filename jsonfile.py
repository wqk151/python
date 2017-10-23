#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:jsonfile.py
@time:2016/11/30 0030 15:23
"""
import urllib2
import json
import sys
# http://124.243.248.100:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeActivity
def get_data(ip,port,qry_value,name):
    url = 'http://' + ip + ':' + port + '/jmx?qry='+qry_value
    reponse = urllib2.urlopen(url)
    data = reponse.read()
    get_value(data,name)
def get_value(data,name):
    s = json.loads(data)
    s_key = s.keys()
    print s[s_key[0]][0][name]
ip = '124.243.248.100'
port = '50070'
qry_value= sys.argv[1]
name = sys.argv[2].split('(')[0]

get_data(ip,port,qry_value,name)




