#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:scapy.py
@time:2016/12/27 0027 16:40
"""
from scapy.all import *
import datetime
import subprocess
import os
pcap_dir = '/data/workspace/tcpdump/'
host = '192.168.0.10'
while True:
    pcap = sniff(timeout=300)
    pcapfile = pcap_dir + 'web3_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.pcap'
    wrpcap(pcapfile,pcap)
    child = subprocess.Popen(['scp '+ pcapfile + ' ' + host + ':' + pcap_dir],shell=True)
    child.communicate()
    os.remove(pcapfile)
