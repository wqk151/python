#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:ftp_test.py
@time:2016/12/12 0012 16:06
"""
"""
使用pexpect模块的spawnu()方法执行FTP命令，通过expect()方法定义匹配的输出规则，sendline()方法执行相关FTP交互命令等
"""
from __future__ import unicode_literals     # 使用Unicode编码
import pexpect
import sys
child = pexpect.spawnu('ftp ftp.openbsd.org')   # 运行FTP命令
child.expect('(?i)name .*: ')   # (?i) 表示后面的字符串正则匹配忽略大小写
child.sendline('anonymous')     # 输入FTP账号信息
child.expect('(?i)password')    # 匹配密码输入提示
child.sendline('pexpect@sourceforge.net')   # 输入FTP密码
child.expect('ftp> ')
child.sendline('bin')       # 启用二进制传输模式
child.expect('ftp> ')
child.expect('get robots.txt')      # 下载robots.txt文件
child.expect('ftp> ')
sys.stdout.write(child.before)
print ("Escape character is '^]'.\n")   # 输出匹配"ftp> "之前的输入与输出
sys.stdout.write(child.after)
sys.stdout.flush()
child.interact()    # 调用interact()让出控制权，用户可以继续当前的会话手工控制子程序，默认输入"^]"字符跳出
child.sendline('bye')
child.close()