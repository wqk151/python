#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:create_jstat_file.py
@time:2017/4/13 0013 11:06
"""
import subprocess
import commands

jstat_dir = '/opt/workspace/jdk/bin/jstat'
item_list = ['class','compiler','gc','gccapacity','gcnew','gcnewcapacity','gcold','gcoldcapacity','gcutil']
alldata = []
def get_item_value(order):
    TOMCAT_PID = subprocess.check_output("ps aux | grep Bootstrap| grep -v grep |awk '{print $2}' ",shell=True)
    out = commands.getoutput("%s -%s %s" %(jstat_dir,order,int(TOMCAT_PID)))
    return out.replace('\n',' ')

for i in range(len(item_list)):
    data = get_item_value(item_list[i])
    alldata.append(data)

with open('/tmp/aaa','w') as f:
    strdata = '\n'.join(alldata)
    f.writelines(strdata)
