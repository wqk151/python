#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:闭包.py
@time:2017/4/21 0021 15:37
"""
# 闭包是由函数和其相关的引用环境组合而成的实体。
# 在实现深约束时，需要创建一个能显式引用环境的东西，并将它与相关的子程序捆绑在一起，这样捆绑起来的整体被称为闭包。
# 通俗讲就是：如果在一个内部函数里，对在外部作用域（但不是全局作用域）的变量引用，那么内部函数就被认为是闭包。它只不过是个"内层"的函数，由一个名字（变量）来指代，而这个名字（变量）对于"外层"包含它的函数而言，是本地变量。

# 定义一个函数
def plus(number):
    # 在函数内部再定义一个函数，其实这个里面的函数就被认为是闭包
    def plus_in(number_in):
        print str(number_in) + "\r\n"
        return number + number_in
    #其实这里返回的就是闭包的结果
    return plus_in

# 给plus函数赋值，这个20就是给参数number
v1 = plus(20)
print v1(100) #注意这里的100其实给参数number_in
'''
运行结果：
100

120
'''
# 注意：100是print str(number_in) + "\r\n"打印的结果
