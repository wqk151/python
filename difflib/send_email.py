#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:send_email.py
@time:2016/12/9 0009 10:19
"""
import smtplib
import string
HOST = "stmp.gmail.com"     # 定义SMTP主机，发件主机
SUBJECT = "test email from python"  # 定义邮件主题
TO = "testmail@qq.com"  # 定义收件人
FROM = "mymail@gmail.com"   # 定义发件人
text = "python roules them all" # 邮件内容
BODY = string.join((    # 组装sendmail方法的邮件主题内容，各段以"\r\n"进行分隔
    "From: %s" % FROM,
    "To: %s" % TO,
    "Subject: %s" % SUBJECT,
    "",
    text
),"\r\n")
server = smtplib.SMTP()     # 创建一个SMTP()对象
server.connect(HOST,"25")   # 通过connect方法连接SMTP主机
server.starttls()   # 启动安全传输模块
server.login(FROM,"mypassword")     # 邮箱账号登录校验
server.sendmail(FROM,[TO],BODY)     # 邮件发送
server.quit()   # 断开SMTP连接
