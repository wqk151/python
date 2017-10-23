#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:理解yield.py
@time:2017/4/21 0021 16:11
"""
def addlist(alist):
    for i in alist:
        yield i +1

alist = [1,2,3,4]
for x in addlist(alist):
    print x

def h():
    print 'wu han'
    yield 5
    print 'beijing'

c = h()
c.next()