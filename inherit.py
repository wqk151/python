#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:inherit.py
@time:2016/10/31 0031 16:24
"""
class Father:
    def __init__(self):
        self.fname = 'fffff'
        print 'father.init'

class Son(Father):
    def __init__(self):
        self.sname='sss'
        print 'son.init'
        Father.__init__(self)

s1 = Son()
print s1.sname
print s1.fname
