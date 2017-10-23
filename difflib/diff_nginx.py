#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:diff_nginx.py
@time:2016/12/8 0008 14:00
"""
import difflib
import sys
try:
    textfile1 = sys.argv[1] # 第一个配置文件路径参数
    textfile2 = sys.argv[2] # 第二个配置文件路径参数
except Exception,e:
    print "Error:"+str(e)
    print "Usage: diff_nginx.py filename1 filename2"
    sys.exit()

def readfile(filname):  # 文件读取分割函数
    try:
        fileHandle = open(filname,'rb')
        text = fileHandle.read().splitlines()   # 读取后以行进行分割
        fileHandle.close()
        return text
    except IOError as error:
        print('Read file Rrror:' + str(error))
        sys.exit()

if textfile1 == "" or textfile2=="":
    print "Uage: diff_nginx.py filename1 filename2"
    sys.exit()
text1_lines = readfile(textfile1)   # 调用readfile函数，获取分割后的字符串
text2_lines = readfile(textfile2)

d = difflib.HtmlDiff()  # 创建HtmlDiff()类对象
print d.make_file(text1_lines,text2_lines)  # 通过make_file方法输出HTML格式的对比结果

