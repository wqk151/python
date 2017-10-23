#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:StatisticalAssetInformation.py
@ Statistical Asset Information for API
@time:2017/1/16 0016 9:36
"""
# get public ip :curl http://members.3322.org/dyndns/getip
#a3:7.0 a2:3.5 a5:14.0
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import confirm
import xlsxwriter

title = [u'主机名',u'内网ip','SSH',u'登录账户密码',u'CPU',u'内存(G)',u'机型',u'虚机价格',u'备注']
#env.hosts = ['10.10.9.56',]
env.roledefs = {
    'azureTEST':['42.159.28.126:55915','42.159.28.126:40122','42.159.28.126:6022','139.217.6.248:22'],
    'azureOldPotal':['139.217.26.123:60362','139.217.26.123:60366','139.217.26.123:61232','139.217.26.123:60368','139.217.26.123:60361',],
    'azureNewPotal':['139.217.3.79:22','139.217.9.227:22','139.217.15.49:22','139.217.9.72:22','139.217.5.102:22','139.217.4.72:22','139.217.0.48:22','139.217.15.186:22','139.217.26.253:22','139.217.14.172 :22','139.217.7.69:22','139.217.27.71:22','139.217.15.210:22','139.217.7.147:22'],
    'azureUAT':['42.159.24.183:58159','42.159.24.183:63068','42.159.24.183:56971','42.159.24.183:58568','42.159.24.183:56940','42.159.24.183:52523',],
    'alish':['139.224.37.185:61300','139.224.37.185:61301','139.224.37.185:61302','139.224.37.185:61303','139.224.37.185:61304','139.224.37.185:61305','139.224.37.185:61306','139.224.37.185:61307','139.224.37.185:61308']
}
env.gateway = '124.243.248.107:22'
#env.password = '50dxOp&^4V1z'
env.azureData = []
env.aliyunData = []

@roles('azureTEST','azureOldPotal','azureNewPotal','azureUAT','alish')
def hostData():
    hostname = run("cat /etc/sysconfig/network | grep HOSTNAME |awk -F'=' '{print $2}'")
    privateIP = run("ifconfig | grep 'inet addr' | grep -v '127' | tr ':' ' ' | awk '{print $3}'")
    sshHostPort = env.host_string  # Obtain this property by looking at the source code,and have some other like :env.roledefs  env.host can use directly
    loginNamePasswd='root=50dxOp&^4V1z'
    cpuInfo = run("cat /proc/cpuinfo| grep -w processor| wc -l")
    memInfo = run("cat /proc/meminfo  | grep -w MemTotal |awk '{print $2}'")
    memSize = int(memInfo)/1000000
    if memSize == 7:
        serverModel = 'A3'
        serverPrice = 1398
    elif memSize == 3:
        serverModel = 'A2'
        serverPrice = 699
    elif memSize == 14:
        serverModel = 'A5'
        serverPrice = 1272
    elif memSize == 1:
        serverModel ='A1'
        serverPrice = 349
    elif memSize == 8:
        serverModel = 'n4'
        serverPrice = 422
    elif memSize == 16:
        serverModel = 'mn4'
        serverPrice = 634
    else:
        serverModel = 'Unknown'
        serverPrice = ' '

    remarks = ' '
    hostDataList = [hostname,privateIP,sshHostPort,loginNamePasswd,cpuInfo,memSize,serverModel,serverPrice,remarks]
    if env.host in env.roledefs['alish']:
        env.aliyunData.append(hostDataList)
    else:
        env.azureData.append(hostDataList)

@roles('azureTEST','azureOldPotal','azureNewPotal','azureUAT','alish')
def createExcel():
    workbook = xlsxwriter.Workbook('apiServer.xlsx')

    azureSheet = workbook.add_worksheet(name='azure')
    aliyunSheet = workbook.add_worksheet(name='aliyun')

    workbookFormat = workbook.add_format()
    workbookFormat.set_align('center')

    azureSheet.write_row('A1',title)
    for i in range(len(env.azureData)):
        azureSheet.write_row('A%s' % (i+2) , env.azureData[i],workbookFormat)

    aliyunSheet.write_row("A1",title)
    for l in range(len(env.aliyunData)):
        aliyunSheet.write_row("A%s" %(l + 2),env.aliyunData[l],workbookFormat)

    workbook.close()
'''
@task
def go():
    hostData()
    createExcel()
'''
def go():
    with hide("running","stdout"):
        execute(hostData)
        execute(createExcel)