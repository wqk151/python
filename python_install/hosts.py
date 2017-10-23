#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="hosts"
__date__="2016/9/6"
__time__="11:45"
"""
import os
class HOST(object):
    def __init__(self):
        self.IP = []
        self.PORT = 22
        self.USERNAME = 'root'
        self.PASSWORD = '123456'
        self.SCRIPT_DIR='/mnt/'



class ftp_host(object):
    def __init__(self):
        self.IP='10.10.8.136'
        self.PORT=22
        self.USERNAME='root'
        self.PASSWD='123456'
        self.REMOTE_TOOL_DIR='/data/ftpdata/tools/'
        self.LOCAL_TOOL_DIR='/data/tools/'
    def mk_dir(self):
        if not os.path.exists(self.LOCAL_TOOL_DIR):
            os.makedirs(self.LOCAL_TOOL_DIR)