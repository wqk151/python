#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:discovery_hadoop_items.py
@time:2016/11/30 0030 16:30
"""
#['Hadoop:service=NameNode,name=FSNamesystem', 'BlockCapacity', 'BlocksTotal', 'CapacityRemainingGB']
import sys
import json
f = file('/data/sh/item_list')
all_data = f.readlines()
alldata=[]
def get_data(item_num):
    for each_item in range(item_num):
        if each_item == item_num-1:
            #print each_item
            continue
        else:
            alldata.append({'{#PROJECT}':each_list[0],'{#ITEM}':each_list[each_item + 1]})
#    print alldata

for each_line in all_data:
    each_list=each_line.split()
    item_num = len(each_list)
    #print item_num
    get_data(item_num)


print json.dumps({'data':alldata},indent=4,separators=(',',':'),ensure_ascii=False)

a
