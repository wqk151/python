#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:send.py
@time:2017/9/5 0005 15:31
"""
import pika

#rabbitmq验证信息
credentials = pika.PlainCredentials('tom','123456')  #文本方式验证，还支持其他验证方式。
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.1.1',credentials=credentials
))

channel = connection.channel()

#声明queue ，发送端不执行，queue没声明。
channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='hello world!')

print '[x] send "hello world!" '

connection.close()