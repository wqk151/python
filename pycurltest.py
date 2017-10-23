#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = "Administrator"
__name__="pycurltest"
__date__="2016/9/9"
__time__="17:43"
"""
import pycurl

c = pycurl.Curl()
url = 'http://www.shujutang.com'

c.setopt(pycurl.URL,url)
print c.perform()
print c.getinfo(pycurl.HTTP_CODE)
print "DNS解析时间:%s" % c.getinfo(c.NAMELOOKUP_TIME)
print "远程服务器的连接时间:%s" % c.getinfo(c.CONNECT_TIME)
print "连接上后开始传输时的时间:%s" % c.getinfo(c.PRETRANSFER_TIME )
print "接收到第一个字节的时间:%s" % c.getinfo(c.STARTTRANSFER_TIME )
print "上一请求总的时间:%s" % c.getinfo(c.TOTAL_TIME)

print "重定向的次数:%s" % c.getinfo(c.REDIRECT_COUNT)
print "上传数据的大小:%s" % c.getinfo(c.SIZE_UPLOAD)
print "下载数据的大小:%s" % c.getinfo(c.SIZE_DOWNLOAD)

