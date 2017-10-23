#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:simple1.py
@time:2016/12/5 0005 10:16
"""
import os,sys
import time
import pycurl
import json
url = "http://apidata.datatang.com/data/credit/p2pBlack?apikey=01e73b08b425faa18d5a1534b219d41a&rettype=json&entityName=%E7%8E%8B%E7%A1%95&entityId=130629199211090911"
c = pycurl.Curl()

c.setopt(pycurl.URL,url)
c.setopt(pycurl.CONNECTTIMEOUT,3)
c.setopt(pycurl.TIMEOUT,5)
c.setopt(pycurl.NOPROGRESS,1)
c.setopt(pycurl.FORBID_REUSE,1)
c.setopt(pycurl.MAXREDIRS,1)
c.setopt(pycurl.DNS_CACHE_TIMEOUT,1)
#indexfile = open(os.path.dirname(os.path.realpath(__file__))+'/content.txt','wb')
#c.setopt(pycurl.WRITEHEADER,indexfile)
#c.setopt(pycurl.WRITEDATA,indexfile)
try:
    c.perform()
except Exception,e:
    print "connecion error:"+str(e)
    c.close()
    sys.exit()
NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
#PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
HTTP_CODE = c.getinfo(c.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
#HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)
data =[{'namelookup_time':'%.2f'%(NAMELOOKUP_TIME*1000)},
       {'connect_time':'%.2f'%(CONNECT_TIME*1000)},
       {'starttransfer_time': '%.2f' %(STARTTRANSFER_TIME*1000)},
       {'total_time':'%.2f' % (TOTAL_TIME*1000)},
       {'http_code':'%d'%HTTP_CODE},
       {'size_download':'%.2f'%SIZE_DOWNLOAD},
       {'speed_download':'%.2f'%SPEED_DOWNLOAD},
       ]
f = open('/tmp/.http_stat','w')
f.write(str(data).replace(',','\n'))
f.close()
print data
print json.dumps({'alldata':[
    {'#WEB_ITEM':'namelookup_time','#WEB_DES':'DNS解析时间'},
    {'#WEB_ITEM':'connect_time','#WEB_DES':'三次握手时间'},
    {'#WEB_ITEM':'starttransfer_time','#WEB_DES':'接收到第一个字节的时间'},
    {'#WEB_ITEM':'total_time','#WEB_DES':'请求总花费时间'},
    {'#WEB_ITEM':'http_code','#WEB_DES':'HTTP状态码'},
    {'#WEB_ITEM':'size_download','#WEB_DES':'下载数据包大小'},
    {'#WEB_ITEM':'speed_download','#WEB_DES':'平均下载速度'},
]},indent=4,ensure_ascii=False)

# python simple1.py >/dev/null 2>&1
'''
将脚本放入crontab中一分钟执行一次，将输出写入文件中，然后从文件中读取数据，而不直接取调用返回的值，减少调用次数
'''