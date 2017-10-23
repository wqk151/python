#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:mcb.pyw
@time:2017/1/23 0023 9:31
"""
# .pyw 扩展名意味着Python运行该程序时，不会显示终端窗口

'''
1、针对要检查的关键字，提供命令行参数。
2、如果参数save，那么将剪贴板的内容保存到关键字
3、如果参数是list，就讲所有的关键字拷贝到剪贴板(打印显示所有关键字)
4、否则，就讲关键词对应的文本拷贝到剪贴板
'''
#Usage: python mcb.pyw save <keyword>  - Save clipboard to keyword.
#       python mcb.pyw <keyword>    -  Loads keyword to clipboard.
#       python mcb.pyw list   - Loads all keywords to clipboard.

import shelve,pyperclip,sys

mcbShelf = shelve.open('mcb')
# Save clipboard content.
#print sys.argv[1]
if len(sys.argv) == 3:
    if sys.argv[1].lower() == 'save':
        mcbShelf[sys.argv[2]] = pyperclip.paste()
    elif sys.argv[1].lower() == 'del':
        del mcbShelf[sys.argv[2]]
elif len(sys.argv) == 2:
    #  List keywords and load content.
    if sys.argv[1].lower() == 'list':
        #pyperclip.copy(str(list(mcbShelf.keys())))
        for k,v in  enumerate(mcbShelf.keys()):
            print k,v
    elif sys.argv[1] in mcbShelf:
        pyperclip.copy(mcbShelf[sys.argv[1]])

mcbShelf.close()
