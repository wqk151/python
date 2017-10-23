#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="main"
__date__="2016/9/6"
__time__="17:13"
"""
import install
import sys
if __name__ == '__main__':
    server_name = sys.argv[1]
    install.IPprocess(server_name)
