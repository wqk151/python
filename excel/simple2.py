#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:simple2.py
@time:2017/1/16 0016 9:44
"""
import xlsxwriter

workbook = xlsxwriter.Workbook('chart.xlsx') #创建一个Excel文件
worksheet = workbook.add_worksheet() #创建一个工作表对象
chart = workbook.add_chart({'type':'column'})  #创建一个图表对象

#定义数据表头列表
title = [u'业务名称',u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日',u'平均流量']

#定义频道名称
buname = [u'业务官网',u'新闻中心',u'购物频道',u'体育频道',u'亲子频道',]

#定义5个频道一周7天流量数据表
data = [
    [150,152,158,149,155,145,148],
    [89,88,95,93,98,100,99],
    [201,200,198,175,170,198,195],
    [75,77,78,78,74,70,79],
    [88,85,87,90,93,88,84]
]

format = workbook.add_format()# 定义format格式对象
format.set_border(1)  #定义format对象单元格边框加粗（1像素）的格式

format_title = workbook.add_format()  #定义fromat_title格式对象
format_title.set_border(1)  #定义format_title对象单元格边框加粗（1像素）的格式
format_title.set_bg_color('#cccccc') #定义format_title对象单元格背景颜色为 #‘#cccccc的格式
format_title.set_align('center') #定义format_title对象单元格居中对齐格式
format_title.set_bold()  #定义format_title对象单元格内容加粗的格式

format_ave=workbook.add_format() #定义format_ave格式对象
format_ave.set_border(1)  #定义format_ave对象单元格边框加粗（1像素）的格式
format_ave.set_num_format('0.00') #定义format_ave对象单元格数字类别显示格式

#下面分别以行或者列写入方式将标题、业务名称、流量数据写入起初单元格，同时引用不同格式对象
worksheet.write_row('A1',title,format_title)
worksheet.write_column('A2',buname,format)
worksheet.write_row('B2',data[0],format)




workbook.close()

