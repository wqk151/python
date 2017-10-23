#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:jstat.py
@time:2017/4/11 0011 11:47
"""
import subprocess
import sys
import commands
ITEM = sys.argv[1]
ORDER_SELECT=sys.argv[2]
jstat_dir = '/opt/workspace/jdk/bin/jstat'

def get_item_value(order):
    TOMCAT_PID = subprocess.check_output("ps aux | grep Bootstrap| grep -v grep |awk '{print $2}' ",shell=True)
    #class_output = subprocess.Popen("%s -%s %s" %(jstat_dir,order,int(TOMCAT_PID)),shell=True,stdout=subprocess.PIPE)
    #class_output.wait()
    #data = class_output.communicate()
    #class_list = data[0].split()
    status,out = commands.getstatusoutput("%s -%s %s" %(jstat_dir,order,int(TOMCAT_PID)))
    data = out.split()
    get_item_index = data.index(ITEM)
    item_value = data[len(data)/2 + get_item_index]
    return item_value
order_select = int(ORDER_SELECT)
if order_select == 1:
    print get_item_value('class')
elif order_select == 2:
    print get_item_value('compiler')
elif order_select ==3:
    print get_item_value('gc')
elif order_select==4:
    print get_item_value('gccapacity')
elif order_select==5:
    print get_item_value('gcnew')
elif order_select==6:
    print get_item_value('gcnewcapacity')
elif order_select==7:
    print get_item_value('gcold')
elif order_select==8:
    print get_item_value('gcoldcapacity')
elif order_select==9:
    print get_item_value('gcmetacapacity')
elif order_select==10:
    print get_item_value('gcutil')

