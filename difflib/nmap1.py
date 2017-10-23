#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:nmap1.py
@time:2016/12/12 0012 10:01
"""

"""
通过python-nmap实现一个高效的端口扫描工具，与定时作业crontab及邮件告警结合，来及时发现异常开发的高危端口。该工具也可以作为业务服务端口的可用性探测，例如扫描192.168.1.20-25网段web服务端口80是否处于open状态。
采用的scan()方法的arguments参数指定为"-v -PE -p"+端口，-v 表示启动细节模式，可以返回非up状态主机清单；-PE表示采用TCP同步扫描(TCP SYN)方式；-p指定扫描端口范围。程序输出部分采用三个for循环体
第一层遍历扫描主机，第二层为遍历协议，第三层为遍历端口，最后输出主机状态。
"""

import sys
import nmap
scan_now=[]
input_data = raw_input('Please input hosts and port:')
scan_now = input_data.split(" ")
if len(scan_now)!=2:
    print "Input errors,example \"192.168.1.0/24 80,443,22\""
    sys.exit()

hosts = scan_now[0]
port = scan_now[1]

try:
    nm = nmap.PortScanner()
except nmap.PortScannerError:
    print ('Nmap not found',sys.exc_info()[0])
    sys.exit(0)
except:
    print ("Unexpect error:",sys.exc_info()[0])
    sys.exit(0)

try:
    nm.scan(hosts=hosts,arguments=' -v -sS -p' + port)
except Exception,e:
    print "Scan error:" + str(e)
for host in nm.all_hosts():
    print ('-----------------------------')
    print "Host: %s (%s)"  % (host,nm[host].hostname())
    print "State: %s" % nm[host].state()
    for proto in nm[host].all_protocols():
        print "------------"
        print "Protocal:%s"  % proto

        lport = nm[host][proto].keys()
        lport.sort()
        for port in lport:
            print "port: %s \t state : %s" % (port,nm[host][proto][port]['state'])

