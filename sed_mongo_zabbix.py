#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:sed_mongo_zabbix.py
@time:2016/11/24 0024 14:11
"""
'''this script is used to send mongodb mmapv1 and wiredtiger storage engine status
'''
'''
    This script only for mongodb version 3.0 or later
'''
'''
    db.serverStatus().wiredTiger  only for mongodb 3.0 or later with wiredtiger storage engine
    db.serverStatus().backgroundFlushing    only for mongodb with mmapv1 storage engine
    check db.serverStatus().storageEngine.name first, if output is mmapv1,send backgroundFlushing data
    if output is wiredTiger then send wiredTiger data
'''
''' {#MONGO_HOST}  localhost:27017
    which_mongo=$(which mongo 2>/dev/null)
    mongo_bin=${which_mongo:-/opt/app/mongodb/sbin/mongo}
    command_line="$mongo_bin $host:$port/admin -u$username -p$password"

    MongoDB.Discovery_Status[wiredTiger,cursor,create,{#MONGO_HOST}]
    MongoDB.Discovery_Status[wiredTiger,cursor,insert,{#MONGO_HOST}]
    MongoDB.Discovery_Status[wiredTiger,cursor,next,{#MONGO_HOST}]
    MongoDB.Discovery_Status[wiredTiger,cursor,prev,{#MONGO_HOST}]
    MongoDB.Discovery_Status[wiredTiger,cursor,remove,{#MONGO_HOST}]
    MongoDB.Discovery_Status[wiredTiger,cursor,reset,{#MONGO_HOST}]

'''

import sys
import subprocess
import json
import logging
import optparse
import tempfile
import os

zabbix_sender = '/usr/sbin/zabbix_sender'
zabbix_conf = '/etc/zabbix/zabbix_agentd.conf'
logging.basicConfig(filename='/var/log/zabbix/mongodb_zabbix.log', level=logging.WARNING,
                    format='%(asctime)s %(levelname)s: %(message)s')


# logging.basicConfig(filename='mongodb_zabbix.log', level=logging.WARNING, format='%(asctime)s %(levelname)s: %(message)s')
#echo "db.serverStatus()"   |/data/apps/mongo/bin/mongo 192.168.0.6:27011/admin -u apimongoadmin -p  YZb4ce5L9o8n
def get_storage_status(mongo_host):
    mongo_host = mongo_host
    mongo_bin = subprocess.Popen(''' which mongo 2>/dev/null||echo '/data/apps/mongo/bin/mongo'  ''', shell=True,
                                 stdout=subprocess.PIPE).stdout.readline().strip()
    command_line = mongo_bin + " " + mongo_host +"/admin" + " " + "-u" + " " + "apimongoadmin" + " "+"-p" +" " + "YZb4ce5L9o8n"
    storage_engine = subprocess.Popen(
        '''echo 'db.serverStatus().storageEngine.name' | %s |sed -n '3p' ''' % (command_line), shell=True,
        stdout=subprocess.PIPE).stdout.readline().strip()

    if storage_engine == "wiredTiger":
        ####### used sed 's/NumberLong("\(.*\)")/\1/g' to remove NumberLong() , note that here we use \\1 in python code
        data = subprocess.Popen(
            '''echo 'db.serverStatus().wiredTiger' | %s |sed -n '3,$p'|sed '$d'|sed 's/NumberLong("\(.*\)")/\\1/g' ''' % (
            command_line), shell=True, stdout=subprocess.PIPE).communicate()[0]
    elif storage_engine == 'mmapv1':

        #########################   "last_finished" : ISODate("2016-05-29T09:31:02.689Z")  no need this line, json parser wrong for ISODate
        data = subprocess.Popen(
            '''echo 'db.serverStatus().backgroundFlushing' | %s |sed -n '3,$p'|sed '$d'|sed 's/"last_finished" :.*/"last_finished" : 0/'  ''' % (
            command_line), shell=True, stdout=subprocess.PIPE).communicate()[0]
    return storage_engine,data

def parse_mmapv1(mongo_host, data, tmpfile):
    mmapv1_json = json.loads(data)
    result = {}
    ################### get mmapv1 backgroundFlushing data   4 items
    result["MongoDB.Discovery_Status[backgroundFlushing,flushes,%s]" % (mongo_host)] = mmapv1_json.get('flushes')
    result["MongoDB.Discovery_Status[backgroundFlushing,average_ms,%s]" % (mongo_host)] = mmapv1_json.get('average_ms')
    result["MongoDB.Discovery_Status[backgroundFlushing,total_ms,%s]" % (mongo_host)] = mmapv1_json.get('total_ms')
    result["MongoDB.Discovery_Status[backgroundFlushing,last_ms,%s]" % (mongo_host)] = mmapv1_json.get('last_ms')
    for key in result:
        #        print key + ":" + str(result.get(key))
        value = result.get(key)
        tmpfile.write("- %s %s\n" % (key, value))

# subprocess.call([zabbix_sender, "-c", zabbix_conf, "-k", key, "-o", str(value) ], shell=False)

def parse_wiredTiger(mongo_host, data, tmpfile):
    wiredTiger_json = json.loads(data)
    '''
    b=str(wiredTiger_json)
    f = file('data.txt','a')
    f.write(b)
    f.flush()
    f.close()
    '''
    result = {}
    ################### get wiredTiger cursor data   11 items
    result["MongoDB.Discovery_Status[wiredTiger,cursor,create,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor create calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,insert,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor insert calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,next,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor next calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,prev,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor prev calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,remove,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor remove calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,reset,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor reset calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,restared_searches,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor restarted searches')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,search,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor search calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,search_near,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor search near calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,update,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('cursor update calls')
    result["MongoDB.Discovery_Status[wiredTiger,cursor,truncate,%s]" % (mongo_host)] = wiredTiger_json.get('cursor').get('truncate calls')

    #################### get wiredTiger transaction data 14 items
    result["MongoDB.Discovery_Status[wiredTiger,transaction,begins,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction begins')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,checkpoint.generation,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoint generation')
    result[
        "MongoDB.Discovery_Status[wiredTiger,transaction,checkpoint.max_time,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoint max time (msecs)')
    result[
        "MongoDB.Discovery_Status[wiredTiger,transaction,checkpoint.min_time,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoint min time (msecs)')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,checkpoint.recent_time,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoint most recent time (msecs)')
    result[
        "MongoDB.Discovery_Status[wiredTiger,transaction,checkpoint.running,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoint currently running')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,checkpoint.total_time,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoint total time (msecs)')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,checkpoints,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction checkpoints')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,committed,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transactions committed')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,failures,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction failures due to cache overflow')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,named_snapshots.created,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('number of named snapshots created')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,named_snapshots.dropped,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('number of named snapshots dropped')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,rolled_back,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transactions rolled back')
    result["MongoDB.Discovery_Status[wiredTiger,transaction,sync_calls,%s]" % (mongo_host)] = wiredTiger_json.get('transaction').get('transaction sync calls')

    ######## get wiredTiger concurrent transactions data 4 items

    result["MongoDB.Discovery_Status[wiredTiger,concurrentTransactions,read.available,%s]" % (mongo_host)] = wiredTiger_json.get('concurrentTransactions').get('read').get('available')
    result[
        "MongoDB.Discovery_Status[wiredTiger,concurrentTransactions,read.out,%s]" % (mongo_host)] = wiredTiger_json.get('concurrentTransactions').get('read').get('out')
    result["MongoDB.Discovery_Status[wiredTiger,concurrentTransactions,write.available,%s]" % (mongo_host)] = wiredTiger_json.get('concurrentTransactions').get('write').get('available')
    result["MongoDB.Discovery_Status[wiredTiger,concurrentTransactions,write.out,%s]" % (mongo_host)] = wiredTiger_json.get('concurrentTransactions').get('write').get('out')

    ####### get wiredTiger session data 2 items
    result["MongoDB.Discovery_Status[wiredTiger,session,cursor,%s]" % (mongo_host)] = wiredTiger_json.get('session').get('open cursor count')
    result["MongoDB.Discovery_Status[wiredTiger,session,session,%s]" % (mongo_host)] = wiredTiger_json.get('session').get('open session count')

    ####### get wiredTiger cache data  36 items
    result["MongoDB.Discovery_Status[wiredTiger,cache,bytes_in,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("bytes currently in the cache")
    result["MongoDB.Discovery_Status[wiredTiger,cache,bytes_read_into,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("bytes read into cache")
    result["MongoDB.Discovery_Status[wiredTiger,cache,bytes_written_from,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("bytes written from cache")
    result["MongoDB.Discovery_Status[wiredTiger,cache,blocked_page_eviction,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("checkpoint blocked page eviction")
    result["MongoDB.Discovery_Status[wiredTiger,cache,eviction_aggressive,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction currently operating in aggressive mode")
    result["MongoDB.Discovery_Status[wiredTiger,cache,eviction_queue_empty,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction server candidate queue empty when topping up")
    result[
        "MongoDB.Discovery_Status[wiredTiger,cache,eviction_queue_not_empty,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction server candidate queue not empty when topping up")
    result["MongoDB.Discovery_Status[wiredTiger,cache,server_evicting_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction server evicting pages")
    result[
        "MongoDB.Discovery_Status[wiredTiger,cache,queue_not_evicting_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction server populating queue, but not evicting pages")
    result["MongoDB.Discovery_Status[wiredTiger,cache,unable_goal,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction server unable to reach eviction goal")
    result["MongoDB.Discovery_Status[wiredTiger,cache,worker_thread_evicting_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("eviction worker thread evicting pages")
    result["MongoDB.Discovery_Status[wiredTiger,cache,failed_eviction_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("failed eviction of pages that exceeded the in-memory maximum")
    result["MongoDB.Discovery_Status[wiredTiger,cache,hazard_pointer_blocked_page_eviction,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("hazard pointer blocked page eviction")
    result["MongoDB.Discovery_Status[wiredTiger,cache,in-memory_page_passed_criteria_to_be_split,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("in-memory page passed criteria to be split")
    result["MongoDB.Discovery_Status[wiredTiger,cache,in-memory_page_splits,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("in-memory page splits")
    result["MongoDB.Discovery_Status[wiredTiger,cache,internal_pages_evicted,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("internal pages evicted")
    result["MongoDB.Discovery_Status[wiredTiger,cache,internal_pages_split,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("internal pages split during eviction")
    result["MongoDB.Discovery_Status[wiredTiger,cache,leaf_pages_split,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("leaf pages split during eviction")
    result["MongoDB.Discovery_Status[wiredTiger,cache,lookaside_table_insert,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("lookaside table insert calls")
    result["MongoDB.Discovery_Status[wiredTiger,cache,lookaside_table_remove,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("lookaside table remove calls")
    result["MongoDB.Discovery_Status[wiredTiger,cache,max_bytes_configured,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("maximum bytes configured")
    result["MongoDB.Discovery_Status[wiredTiger,cache,max_page_size_eviction,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("maximum page size at eviction")
    result["MongoDB.Discovery_Status[wiredTiger,cache,modified_pages_evicted,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("modified pages evicted")
    result["MongoDB.Discovery_Status[wiredTiger,cache,pages_held,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("pages currently held in the cache")

    result["MongoDB.Discovery_Status[wiredTiger,cache,pages_evicted_exceeded_in-memory_max,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("pages evicted because they exceeded the in-memory maximum")
    result["MongoDB.Discovery_Status[wiredTiger,cache,pages_evicted_deleted_items,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("pages evicted because they had chains of deleted items")
    result["MongoDB.Discovery_Status[wiredTiger,cache,pages_evicted_application_threads,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("pages evicted by application threads")
    result["MongoDB.Discovery_Status[wiredTiger,cache,pages_read_into_cache,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("pages read into cache")
    result[
        "MongoDB.Discovery_Status[wiredTiger,cache,pages_written_from_cache,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("pages written from cache")

    result["MongoDB.Discovery_Status[wiredTiger,cache,percentage_overhead,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("percentage overhead")
    result["MongoDB.Discovery_Status[wiredTiger,cache,tracked_bytes_internal_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("tracked bytes belonging to internal pages in the cache")
    result[
        "MongoDB.Discovery_Status[wiredTiger,cache,tracked_bytes_leaf_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("tracked bytes belonging to leaf pages in the cache")
    result["MongoDB.Discovery_Status[wiredTiger,cache,tracked_bytes_overflow_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("tracked bytes belonging to overflow pages in the cache")
    result["MongoDB.Discovery_Status[wiredTiger,cache,tracked_dirty_bytes,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("tracked dirty bytes in the cache")
    result["MongoDB.Discovery_Status[wiredTiger,cache,tracked_dirty_pages,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("tracked dirty pages in the cache")
    result[
        "MongoDB.Discovery_Status[wiredTiger,cache,unmodified_pages_evicted,%s]" % (mongo_host)] = wiredTiger_json.get('cache').get("unmodified pages evicted")

    #################### get wiredTiger log data  32 items

    result[
        "MongoDB.Discovery_Status[wiredTiger,log,busy_returns_switch_slots,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("busy returns attempting to switch slots")
    result[
        "MongoDB.Discovery_Status[wiredTiger,log,consolidated_slot_closures,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("consolidated slot closures")
    result["MongoDB.Discovery_Status[wiredTiger,log,consolidated_slot_join_races,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("consolidated slot join races")
    result["MongoDB.Discovery_Status[wiredTiger,log,consolidated_slot_join_transitions,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("consolidated slot join transitions")
    result["MongoDB.Discovery_Status[wiredTiger,log,consolidated_slot_joins,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("consolidated slot joins")
    result["MongoDB.Discovery_Status[wiredTiger,log,consolidated_slot_unbuffered_writes,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("consolidated slot unbuffered writes")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_bytes_payload_data,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log bytes of payload data")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_bytes_written,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log bytes written")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_files_manually_zero_filled,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log files manually zero-filled")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_flush_operations,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log flush operations")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_force_write,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log force write operations")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_force_write_skipped,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log force write operations skipped")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_records_compressed,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log records compressed")
    result[
        "MongoDB.Discovery_Status[wiredTiger,log,log_records_not_compressed,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log records not compressed")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_records_too_small,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log records too small to compress")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_release_advances_write_lsn,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log release advances write LSN")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_scan_operations,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log scan operations")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_sync_operations,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log sync operations")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_sync_dir_operations,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log sync_dir operations")
    result["MongoDB.Discovery_Status[wiredTiger,log,log_write_operations,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("log write operations")
    result[
        "MongoDB.Discovery_Status[wiredTiger,log,logging_bytes_consolidated,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("logging bytes consolidated")
    result["MongoDB.Discovery_Status[wiredTiger,log,max_log_size,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("maximum log file size")
    result["MongoDB.Discovery_Status[wiredTiger,log,pre-allocated_log_files_create,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("number of pre-allocated log files to create")
    result["MongoDB.Discovery_Status[wiredTiger,log,pre-allocated_log_files_not_ready_missed,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("pre-allocated log files not ready and missed")
    result["MongoDB.Discovery_Status[wiredTiger,log,pre-allocated_log_files_prepared,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("pre-allocated log files prepared")
    result["MongoDB.Discovery_Status[wiredTiger,log,pre-allocated_log_files_used,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("pre-allocated log files used")
    result["MongoDB.Discovery_Status[wiredTiger,log,records_processed_by_log_scan,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("records processed by log scan")
    result["MongoDB.Discovery_Status[wiredTiger,log,total_in-memory_compressed_records_size,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("total in-memory size of compressed records")
    result["MongoDB.Discovery_Status[wiredTiger,log,total_log_buffer_size,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("total log buffer size")
    result["MongoDB.Discovery_Status[wiredTiger,log,total_compressed_records_size,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("total size of compressed records")
    result["MongoDB.Discovery_Status[wiredTiger,log,written_slots_coalesced,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("written slots coalesced")
    result[
        "MongoDB.Discovery_Status[wiredTiger,log,yields_waiting_prelog_close,%s]" % (mongo_host)] = wiredTiger_json.get('log').get("yields waiting for previous log file close")

    ################### get wiredTiger connection data  11 items
    result["MongoDB.Discovery_Status[wiredTiger,connection,auto_adjusting_condition_resets,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("auto adjusting condition resets")
    result["MongoDB.Discovery_Status[wiredTiger,connection,auto_adjusting_condition_wait,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("auto adjusting condition wait calls")
    result["MongoDB.Discovery_Status[wiredTiger,connection,files_open,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("files currently open")
    result[
        "MongoDB.Discovery_Status[wiredTiger,connection,memory_allocations,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("memory allocations")
    result["MongoDB.Discovery_Status[wiredTiger,connection,memory_frees,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("memory frees")
    result["MongoDB.Discovery_Status[wiredTiger,connection,memory_re-allocations,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("memory re-allocations")
    result["MongoDB.Discovery_Status[wiredTiger,connection,pthread_mutex_condition_wait,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("pthread mutex condition wait calls")
    result["MongoDB.Discovery_Status[wiredTiger,connection,pthread_mutex_shared_read-lock,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("pthread mutex shared lock read-lock calls")
    result["MongoDB.Discovery_Status[wiredTiger,connection,pthread_mutex_shared_write_lock,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("pthread mutex shared lock write-lock calls")
    result["MongoDB.Discovery_Status[wiredTiger,connection,total_read_io,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("total read I/Os")
    result["MongoDB.Discovery_Status[wiredTiger,connection,total_write_io,%s]" % (mongo_host)] = wiredTiger_json.get('connection').get("total write I/Os")

    ##################### get wiredTiger  thread yield  5 items

    result["MongoDB.Discovery_Status[wiredTiger,thread-yield,page_acquire_busy_blocked,%s]" % (mongo_host)] = wiredTiger_json.get('thread-yield').get('page acquire busy blocked')
    result["MongoDB.Discovery_Status[wiredTiger,thread-yield,page_acquire_eviction_blocked,%s]" % (mongo_host)] = wiredTiger_json.get('thread-yield').get('page acquire eviction blocked')
    result["MongoDB.Discovery_Status[wiredTiger,thread-yield,page_acquire_locked_blocked,%s]" % (mongo_host)] = wiredTiger_json.get('thread-yield').get('page acquire locked blocked')
    result["MongoDB.Discovery_Status[wiredTiger,thread-yield,page_acquire_read_blocked,%s]" % (mongo_host)] = wiredTiger_json.get('thread-yield').get('page acquire read blocked')
    result["MongoDB.Discovery_Status[wiredTiger,thread-yield,page_acquire_time_sleeping,%s]" % (mongo_host)] = wiredTiger_json.get('thread-yield').get('page acquire time sleeping (usecs)')

    #################### get wiredTiger data handle  8 items

    result[
        "MongoDB.Discovery_Status[wiredTiger,data-handle,data_handles_active,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get('connection data handles currently active')
    result["MongoDB.Discovery_Status[wiredTiger,data-handle,sweep_referenced,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get('connection sweep candidate became referenced')
    result["MongoDB.Discovery_Status[wiredTiger,data-handle,sweep_dhandles_closed,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get("connection sweep dhandles closed")
    result["MongoDB.Discovery_Status[wiredTiger,data-handle,sweep_dhandles_removed,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get("connection sweep dhandles removed from hash list")
    result[
        "MongoDB.Discovery_Status[wiredTiger,data-handle,sweep_time-of-death,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get("connection sweep time-of-death sets")
    result["MongoDB.Discovery_Status[wiredTiger,data-handle,sweeps,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get("connection sweeps")
    result["MongoDB.Discovery_Status[wiredTiger,data-handle,session_dhandles_swept,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get("session dhandles swept")
    result["MongoDB.Discovery_Status[wiredTiger,data-handle,session_sweep_attempts,%s]" % (mongo_host)] = wiredTiger_json.get('data-handle').get("session sweep attempts")

    #################### get wiredTiger block manager 7 items
    result[
        "MongoDB.Discovery_Status[wiredTiger,block-manager,blocks_pre-loaded,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('blocks pre-loaded')
    result["MongoDB.Discovery_Status[wiredTiger,block-manager,blocks_read,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('blocks read')
    result["MongoDB.Discovery_Status[wiredTiger,block-manager,blocks_written,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('blocks written')
    result["MongoDB.Discovery_Status[wiredTiger,block-manager,bytes_read,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('bytes read')
    result["MongoDB.Discovery_Status[wiredTiger,block-manager,bytes_written,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('bytes written')
    result["MongoDB.Discovery_Status[wiredTiger,block-manager,mapped_blocks_read,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('mapped blocks read')
    result[
        "MongoDB.Discovery_Status[wiredTiger,block-manager,mapped_bytes_read,%s]" % (mongo_host)] = wiredTiger_json.get('block-manager').get('mapped bytes read')
    # print result



    for key in result:
        value = result.get(key)
        ########## some items can only exist on mongodb3.2, on mongodb3.0 they do not exit,so the items values are None,we replace them to 0
        if value is None:
            ########  here must be None, can not be value=="None", because None is NoneType in python
            value = 0
        # print key + ":" + str(value)
        tmpfile.write("- %s %s\n" % (key, value))

# subprocess.call([zabbix_sender, "-c", zabbix_conf, "-k", key, "-o", str(value) ], shell=False)

def send_data_to_zabbix(conf, tmpfile):
    args = zabbix_sender + ' -c {0} -i {1}  -vv'
    return_code = 0
    process = subprocess.Popen(args.format(conf, tmpfile.name),
                               shell=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    logging.debug("Finished sending data")
    return_code = process.wait()
    logging.info("Found return code of " + str(return_code))
    if return_code != 0:
        logging.warning(out)
        logging.warning(err)
    else:
        logging.debug(err)
        logging.debug(out)
    return return_code


def main():
    parser = optparse.OptionParser()
    parser.add_option('--mongo_host', help='The value of macro {#MONGO_HOST}')
    (options, args) = parser.parse_args()
    if options.mongo_host:
        storage_engine, data = get_storage_status(options.mongo_host)
        return_code = 0
        #### use tempfile module to create a file on memory, will not be deleted when it is closed , because 'delete' argument is set to False
        rdatafile = tempfile.NamedTemporaryFile(delete=False)

        if storage_engine == "mmapv1":
            parse_mmapv1(options.mongo_host, data, rdatafile)
        elif storage_engine == "wiredTiger":
            parse_wiredTiger(options.mongo_host, data, rdatafile)
        rdatafile.close()
        return_code = send_data_to_zabbix(zabbix_conf, rdatafile)
        #### os.unlink is used to remove a file
        os.unlink(rdatafile.name)
        print return_code

if __name__ == "__main__":
    main()