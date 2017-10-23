#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:test_var_args.py
@time:2016/10/27 0027 18:50
"""
def test_var_args(f_arg,*argv):
    print 'first normal arg:',f_arg
    for arg in argv:
        print 'another arg through *argv:',arg

test_var_args('yesoob','python','eggs','test')