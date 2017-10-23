#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:fabfile.py
@time:2017/2/14 0014 13:39
"""
"""
remote installation of the entry file
"""
import sys
sys.path.append('.')
from fabric.colors import *
from fabric.api import *
env.password='123456'

def install_jdk():
    run('ifconfig')

def install_mongodb():
    run('uname -a')

def install_tomcat():
    run('cat /etc/hosts')
def install_zookeeper():
    run('cd /mmmmmm')