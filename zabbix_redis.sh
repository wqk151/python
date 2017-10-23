#!/bin/bash
set -x
set -e
#__date__=2016/12/6 0006 15:17
REDISPATH="/data/apps/redis/src/redis-cli"
HOST="10.0.0.13"
PORT="6379"
REDIS_PA="$REDISPATH -h $HOST -p $PORT -a UVS8vqBD9HsXfEbTlJea info"
if [[ $# == 1 ]];then
    case $1 in
# clients
 connected_clients)
        result=`$REDIS_PA|/bin/grep -w connected_clients|awk -F":" '{print $NF}'`
            echo $result
            ;;
 client_longest_output_list)
        result=`$REDIS_PA|/bin/grep -w client_longest_output_list|awk -F":" '{print $NF}'`
            echo $result
            ;;
 client_biggest_input_buf)
        result=`$REDIS_PA|/bin/grep -w client_biggest_input_buf|awk -F":" '{print $NF}'`
            echo $result
            ;;
 blocked_clients)
        result=`$REDIS_PA|/bin/grep -w blocked_clients|awk -F":" '{print $NF}'`
            echo $result
            ;;
#memory
 used_memory)
        result=`$REDIS_PA|/bin/grep -w used_memory|awk -F":" '{print $NF}'|awk 'NR==1'`
            echo $result
            ;;

 used_memory_rss)
        result=`$REDIS_PA|/bin/grep -w used_memory_rss|awk -F":" '{print $NF}'`
            echo $result
            ;;
 used_memory_peak)
        result=`$REDIS_PA|/bin/grep -w used_memory_peak|awk -F":" '{print $NF}'|awk 'NR==1'`
            echo $result
            ;;

 used_memory_lua)
        result=`$REDIS_PA|/bin/grep -w used_memory_lua|awk -F":" '{print $NF}'`
            echo $result
            ;;
 mem_fragmentation_ratio)
        result=`$REDIS_PA|/bin/grep -w mem_fragmentation_ratio|awk -F":" '{print $NF}'`
            echo $result
            ;;

#stats
 total_connections_received)
        result=`$REDIS_PA|/bin/grep -w "total_connections_received" | awk -F':' '{print $2}'`
            echo $result
            ;;
 total_commands_processed)
        result=`$REDIS_PA|/bin/grep -w "total_commands_processed" | awk -F':' '{print $2}'`
            echo $result
            ;;
 instantaneous_ops_per_sec)
        result=`$REDIS_PA|/bin/grep -w "instantaneous_ops_per_sec" | awk -F':' '{print $2}'`
            echo $result
            ;;
 rejected_connections)
        result=`$REDIS_PA|/bin/grep -w "rejected_connections" | awk -F':' '{print $2}'`
            echo $result
            ;;
 expired_keys)
        result=`$REDIS_PA|/bin/grep -w "expired_keys" | awk -F':' '{print $2}'`
            echo $result
            ;;
 evicted_keys)
        result=`$REDIS_PA|/bin/grep -w "evicted_keys" | awk -F':' '{print $2}'`
            echo $result
            ;;
 keyspace_hits)
        result=`$REDIS_PA|/bin/grep -w "keyspace_hits" | awk -F':' '{print $2}'`
            echo $result
            ;;
 keyspace_misses)
        result=`$REDIS_PA|/bin/grep -w "keyspace_misses" | awk -F':' '{print $2}'`
            echo $result
            ;;
 pubsub_channels)
        result=`$REDIS_PA|/bin/grep -w "pubsub_channels" | awk -F':' '{print $2}'`
            echo $result
            ;;
 pubsub_patterns)
        result=`$REDIS_PA|/bin/grep -w "pubsub_patterns" | awk -F':' '{print $2}'`
            echo $result
            ;;
 bytes_received_per_sec)
        result=`$REDIS_PA|/bin/grep -w "instantaneous_input_kbps" | awk -F':' '{print $2}'`
            echo $result
            ;;
 bytes_sent_per_sec)
        result=`$REDIS_PA|/bin/grep -w "instantaneous_output_kbps" | awk -F':' '{print $2}'`
            echo $result
            ;;

#cpu
 used_cpu_sys)
        result=`$REDIS_PA|/bin/grep -w "used_cpu_sys"|awk -F':' '{print $2}'`
            echo $result
            ;;
 used_cpu_user)
        result=`$REDIS_PA|/bin/grep -w "used_cpu_user"|awk -F':' '{print $2}'`
            echo $result
            ;;
#persistence
 rdb_current_bgsave_time_sec)
        result=`$REDIS_PA|/bin/grep -w "rdb_current_bgsave_time_sec"|awk -F':' '{print $2}'`
            echo $result
            ;;
 rdb_bgsave_in_progress)
        result=`$REDIS_PA|/bin/grep -w "rdb_bgsave_in_progress"|awk -F':' '{print $2}'`
            echo $result
            ;;
 rdb_changes_since_last_save)
        result=`$REDIS_PA|/bin/grep -w "rdb_changes_since_last_save"|awk -F':' '{print $2}'`
            echo $result
            ;;
 rdb_last_save_time)
        result=`$REDIS_PA|/bin/grep -w "rdb_last_save_time"|awk -F':' '{print $2}'`
            echo $result
            ;;

  #slowlog
 slowlog-len)
        result=`echo 'slowlog len' |$REDISPATH -h $HOST -p $PORT -a UVS8vqBD9HsXfEbTlJea  |cut -f2`
            echo $result
            ;;
        *)
        echo "Usage:$0{connected_clients|client_longest_output_list|client_biggest_input_buf|blocked_clients|used_memory|used_memory_human|used_memory_rss|used_memory_peak|used_memory_peak_human|used_memory_lua|mem_fragmentation_ratio|rdb_changes_since_last_save|rdb_bgsave_in_progress|rdb_last_save_time|rdb_last_bgsave_status|rdb_current_bgsave_time_sec|aof_enabled|aof_rewrite_scheduled|aof_last_rewrite_time_sec|aof_current_rewrite_time_sec|aof_last_bgrewrite_status|aof_current_size|aof_base_size|aof_pending_rewrite|aof_buffer_length|aof_rewrite_buffer_length|aof_pending_bio_fsync|aof_delayed_fsync|rejected_connections|instantaneous_ops_per_sec|total_connections_received|total_commands_processed|expired_keys|evicted_keys|keyspace_hits|keyspace_misses|pubsub_channels|pubsub_patterns|latest_fork_usec|connected_slaves|master_link_status|master_sync_in_progress|master_last_io_seconds_ago|connected_slaves|slave_priority|used_cpu_user|used_cpu_sys|used_cpu_sys_children|used_cpu_user_children}"
        ;;
    esac
fi