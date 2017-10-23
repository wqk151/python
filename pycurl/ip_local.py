#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:ip_local.py
@time:2016/12/20 0020 18:01
"""
import pycurl
import StringIO
import random
from time import sleep
f_ip = file('file')
for i in f_ip.xreadlines():

    url = "http://freeapi.ipip.net/" + i.split()[0]
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.MAXREDIRS,5)
    c.setopt(pycurl.CONNECTTIMEOUT,60)
    c.setopt(pycurl.TIMEOUT,300)
    c.setopt(pycurl.USERAGENT,"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)")
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION,b.write)
    sleep_time = random.randrange(1,7)
    sleep(sleep_time)
    c.perform()
    f = file('aaa.txt','a')
    ip_message = i.strip('\n') + ':' + b.getvalue() + '\n'
    f.write(ip_message)
    f.close()
    b.close()
    c.close()

