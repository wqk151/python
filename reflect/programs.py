#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:programs.py
@time:2016/11/14 0014 11:51
"""
# I am a program need connect DB
import sys
db_model = 'slave'
sys.path.append('..')
'''
model = __import__(db_model)
model.master_func()
'''
pro_func = 'slave_func'
model = __import__(db_model)
function = getattr(model,pro_func)
print function  # 打印函数对象
print getattr(model,'ip')   # 打印属性ip的值
function()
