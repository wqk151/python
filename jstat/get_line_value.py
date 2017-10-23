#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:get_line_value.py
@time:2017/4/13 0013 11:35
"""
import linecache
import sys
jstat_file = '/tmp/aaa'
line_num = sys.argv[2]
line_item = sys.argv[1]

data = linecache.getline(jstat_file,int(line_num)).split()
get_item_index = data.index(line_item)
item_value = data[len(data)/2+get_item_index]
print item_value
