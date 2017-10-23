#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:interfaceDetection.py
@time:2017/1/20 0020 10:14
"""
import pycurl
import xlsxwriter
import smtplib
import StringIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time,sys
import xlrd

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

localeTime = time.strftime('%Y-%m-%d')
excelFileName = '/data/workspace/apiInter/interfaceDetection_%s.xlsx' % localeTime
allData = []
def getCurl(id,des,interUrl):
    c = pycurl.Curl()
    c.setopt(c.URL,interUrl)
    b = StringIO.StringIO()
    c.setopt(c.CONNECTTIMEOUT,5) #连接的等待时间
    c.setopt(c.TIMEOUT,10) # 连接超时时间
    c.setopt(c.NOPROGRESS,1)# 屏蔽下载进度条
    c.setopt(c.FORBID_REUSE,1) #完成交互后强制断开连接
    c.setopt(c.MAXREDIRS,3) # 最大重定向次数
    c.setopt(c.DNS_CACHE_TIMEOUT,1) # 设置保存DNS信息的时间
    indexFile = open('/data/workspace/apiInter/content_%s.txt' % localeTime ,'a')
    #c.setopt(c.WRITEHEADER,indexFile)
    c.setopt(c.WRITEFUNCTION,b.write)

    try:
        c.perform()
    except Exception,e:
        # print 'have some wrong',e
        HTTP_CODE = u'超时'
        REMARK = str(e)
    else:
        # 返回的http状态码
        HTTP_CODE = c.getinfo(c.HTTP_CODE)
        REMARK = ' '
    #传输结束所消耗的总时间
    totalTime = c.getinfo(c.TOTAL_TIME)
    #dns解析所消耗的时间
    namelookupTime = c.getinfo(c.NAMELOOKUP_TIME)
    #建立连接所消耗的时间
    connectTime = c.getinfo(c.CONNECT_TIME)
    # 重定向所消耗的时间
    #redirectTime = c.getinfo(c.REDIRECT_TIME)
    # 下载数据包的大小
    sizeDownload = c.getinfo(c.SIZE_DOWNLOAD)
    htmldata = b.getvalue()
    indexFile.write(htmldata)
    indexFile.close()
    if 'resCode' in htmldata:
        errorMessage = ' '
    else:
        errorMessage = str(htmldata)
    curlData = [id,des,connectTime,namelookupTime,totalTime,sizeDownload,HTTP_CODE,REMARK,errorMessage]
    allData.append(curlData)
    b.close()
    return allData
def createExcel():

    workbook = xlsxwriter.Workbook(excelFileName)
    worksheet = workbook.add_worksheet()
    title = [u'接口ID',u'接口描述',u'建立连接时间(s)',u'dns解析时间(s)',u'传输消耗总时间(s)',u'数据包大小(byte)',u'http状态码',u'备注',u'错误信息']
    columnNum = len(title)
    worksheet.set_column(0,columnNum,20)

    workBookFormat = workbook.add_format()
    workBookFormat.set_align('center')
    workBookFormat.set_text_wrap()
    worksheet.write_row('A1',title,workBookFormat)
    for i in range(len(allData)):
        worksheet.write_row('A%s'%(i+2),allData[i])
    workbook.close()

def sendEmail():
    HOST= 'smtp.163.com'
    SUBJECT = u"每周接口调用检测"
    TO = ['','','']  # 群发收件人为列表形式
    FROM = ""
    SECRET = '123'
    msg = MIMEMultipart()
    msgtext = MIMEText("所有接口调用情况统计,见附件")
    msg.attach(msgtext)

    part = MIMEApplication(open(excelFileName,'rb').read())

    part.add_header('Content-Disposition', 'attachment', filename=excelFileName.split('/')[4])
    msg.attach(part)
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = ','.join(TO)    # 收件人列表要转换成字符串
    try:
        server = smtplib.SMTP()
        server.connect(HOST,'25')
        server.starttls()
        server.login(FROM,SECRET)
        server.sendmail(FROM,TO,msg.as_string())
        server.quit()
        print 'mail send sucess'
    except Exception,e:
        print 'faild: ' + str(e)

if __name__ == '__main__':
    with open('/data/sh/file') as f:
        data = f.xreadlines()
        for i in data:
            id = i.split()[0]
            des = i.split()[1]
            url = i.split()[2]
            getCurl(id,des,url)
    createExcel()
    sendEmail()