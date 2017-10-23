#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file:receive.py
@time:2017/9/5 0005 15:36
"""

import pika

#rabbitmq验证信息
credentials = pika.PlainCredentials('tom','123456')  #文本方式验证，还支持其他验证方式。
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='192.168.1.1',credentials=credentials
))

channel = connection.channel()

#声明queue,这里声明是为了防止发送端没有启动，而queue没有声明(如果发送端已启动，这里可以不用再次声明)
channel.queue_declare(queue='hello')


def callback(ch,mehtod,properties,body):
    print '[x] received %r ' % body

channel.basic_consume(callback,  # 收到消息之后，执行这个回调函数
                          queue='hello',  # 接收消息的queue
                          no_ack=True)   #


print '[*] waiting for messages. to exit press Ctrl+c'

channel.start_consuming()