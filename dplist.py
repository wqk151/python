#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:dplist.py
@time:2016/10/13 9:49
"""
def dp(s):
    if isinstance(s,(int,str)):
        print s
    else:
        for item in s:
            dp(item)

li = ['jack',('tom',23),'rose',(14,55,('jon',18))]

dp(li)