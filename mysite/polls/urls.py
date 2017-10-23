#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:urls.py
@time:2017/3/1 0001 18:39
"""
from django.conf.urls import url
from . import views
"""
urlpatterns = [
    # ex: /polls/
    url(r'^$',views.index,name='index'),
    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$',views.detail,name='detail'),
    # ex: /polls/5/result/
    url(r'^(?P<question_id>[0-9]+)/results/$',views.results,name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote,name='vote')
]
"""
"""
url()参数：view---指定视图函数
并将HttpRequest对象作为该函数的第一个参数，从正则表达式中"捕获"的其他值作为该函数的其他参数。
如果正则表达式使用简单的捕获方式，值作为位置参数传递给该函数；如果使用命名的捕获方式，值将作为关键字参数传递给该函数。
url()参数：kwargs---将关键字参数以字典形式传递给目标视图。
url()参数：name ---命令URL。这样就可以在Django的其他地方尤其是模板中，通过名称来明确地引用这个URL。

question_id是一个关键字参数，传递给视图函数；
?P<question_id> 定义了一个名字，它用于表示匹配的模式；
[0-9]+是匹配一串数字的正则表达式
"""
urlpatterns = [
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view(),name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$',views.ResultsView.as_view(),name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote,name='vote'),
]