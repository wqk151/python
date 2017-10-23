#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:hosts.py
@time:2016/11/8 0008 11:32
"""
import template
h1 = template.HostTemplate()

h1.ip=['192.168.4.129',]
h1.file=['/tmp/sysinit.sh','/tmp/a.sh']
#g1.port=6022
#print g1.ip,g1.passwd,g1.user,g1.port
