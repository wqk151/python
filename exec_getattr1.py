#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:exec_getattr1.py
@time:2016/11/1 0001 14:56
"""
class trygetattr(object):
    def __init__(self):
        self.name = 'tom'
    def onemethod(self):
        print 'this is a method'

aninstance = trygetattr()

print getattr(aninstance,'name','not found')
print getattr(aninstance,'age','not found')
print getattr(aninstance,'onemethod','default')
print getattr(aninstance,'onemethod','default')()
