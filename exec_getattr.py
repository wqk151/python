#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:exec_getattr.py
@time:2016/11/1 0001 9:18
"""
class attrtest(object):
    def __init__(self):
        pass
    def trygetattr0(self):
        self.name = 'lucas'
        self.age = '18'
        print self.name
        print getattr(self,'name')
        print getattr(self,'age')

if __name__ == '__main__':
    test = attrtest()
    test.trygetattr0()