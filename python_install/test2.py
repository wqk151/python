#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="test2"
__date__="2016/9/9"
__time__="9:46"
"""

# 传递list参数
def show(*arg):
    #for i in range(len(arg)):
    print arg
    print arg[0]
    print arg[0][3]
    for i in arg:
        print i
        print i[0]

a=[1,2,3,4,5]
show(a)