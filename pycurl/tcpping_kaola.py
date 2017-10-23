#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:tcpping_kaola.py
@time:2017/4/17 0017 15:13
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:interfaceDetection.py
@time:2017/1/20 0020 10:14
"""
import pycurl
import StringIO

def getCurl(interUrl):
    c = pycurl.Curl()
    c.setopt(c.URL,interUrl)
    b = StringIO.StringIO()
    c.setopt(c.CONNECTTIMEOUT,30) #连接的等待时间
    c.setopt(c.TIMEOUT,30) # 连接超时时间
    c.setopt(c.NOPROGRESS,1)# 屏蔽下载进度条
    c.setopt(c.FORBID_REUSE,1) #完成交互后强制断开连接
    c.setopt(c.MAXREDIRS,3) # 最大重定向次数
    c.setopt(c.DNS_CACHE_TIMEOUT,1) # 设置保存DNS信息的时间
    #indexFile = open('/data/workspace/apiInter/content_%s.txt' % localeTime ,'a')
    #c.setopt(c.WRITEHEADER,indexFile)
    c.setopt(c.WRITEFUNCTION,b.write)
    c.perform()
    #传输结束所消耗的总时间
    totalTime = c.getinfo(c.TOTAL_TIME)
    #dns解析所消耗的时间
    namelookupTime = c.getinfo(c.NAMELOOKUP_TIME)
    #建立连接所消耗的时间
    connectTime = c.getinfo(c.CONNECT_TIME)
    print 'connect_time: ',connectTime
    print 'nslookup_time: ',namelookupTime
    print 'total_time: ',totalTime

getCurl('https://acctc.kaolazhengxin.com:8452/identityQuery.do')