#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:psutil_all.py
@time:2017/3/14 0014 10:00
"""
import psutil
import datetime

pidList = psutil.pids()

for p in range(len(pidList)):
    if pidList[p] > 100:
        process = psutil.Process(pidList[p])
        process_create_time = datetime.datetime.fromtimestamp(process.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        pidStatus = [ process.name() , process.exe() , process_create_time , process.uids() , process.cpu_percent() , process.memory_percent() , process.io_counters() , process.connections()]

        print pidStatus