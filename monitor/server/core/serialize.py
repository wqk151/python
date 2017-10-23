#_*_coding:utf-8_*_
__author__ = 'alex'
from conf import hosts
import json,time,operator
def push_all_configs_into_redis(main_ins,host_groups):
    host_config_dic = {}
    for group in host_groups:
        #print group.name
        for h in group.hosts:
            #print h ,group.services
            if h not in host_config_dic:
                host_config_dic[h] = {}
            for s in group.services:
                host_config_dic[h][s.name] = [s.plugin_name, s.interval]
    for h,v in host_config_dic.items():
        #print h ,v
        host_config_key = "HostConfig::%s" %h
        main_ins.r.set(host_config_key,json.dumps(v))
def fetch_all_configs(host_groups):
    host_config_dic = {}
    for group in host_groups:
        #print group.name
        for h in group.hosts:
            #print h ,group.services
            if h not in host_config_dic:
                host_config_dic[h] = {}
            for s in group.services:
                host_config_dic[h][s.name] = s
    for h,v in host_config_dic.items():
        print h ,v
    return host_config_dic


def data_process(main_ins):
    print '---going to handle monitor data----'
    all_host_configs = fetch_all_configs(hosts.monitored_groups)
    #while True:
    for ip,service_dic in all_host_configs.items():
        for service_name,s_instance in service_dic.items():
            service_redis_key = "ServiceData::%s::%s" %(ip,service_name)
            s_data = main_ins.r.get(service_redis_key)
            if s_data:
                s_data = json.loads(s_data)
                #print '###>',s_data
                time_stamp = s_data['time_stamp']
                if time.time() - time_stamp < s_instance.interval:
                    if s_data['data']['status'] ==0:#data valid
                        print "\033[32;1mHost[%s]  Service[%s] data valid\033[0m"%(ip,service_name)
                        #print service_name,s_data['data']
                        for item_key,val_dic in s_instance.triggers.items():
                            service_item_handle(main_ins,item_key,val_dic,s_data)
                    else:
                        print "\033[31;1mHost[%s]  Service[%s] plugin error" %(ip,service_name)

                else:#data expired
                    expired_time = time.time() - time_stamp - s_instance.interval
                    print "\033[31;1mHost[%s]  Service[%s] data expired[%s] secs" %(ip,service_name,expired_time)

            else:
                print "\033[31;1mNo data found in redis for service [%s] host[%s]\033[0m" %(service_name,ip)
        #time.sleep(1)

def service_item_handle(main_ins,item_key,val_dic,client_service_data ):
    print '===>',item_key,client_service_data['data'][item_key]
    item_data = client_service_data['data'][item_key]

    warning_val = val_dic['warning']
    critical_val = val_dic['critical']
    oper =  val_dic['operator']
    print type(item_data),oper
    oper_func = getattr(operator,oper)

    if val_dic['data_type'] is float:
        item_data = float(item_data)
        warning_res = oper_func(item_data, warning_val)
        critical_res = oper_func(item_data, critical_val)
        print "warinng: [%s] critical:[%s]" %(warning_val,critical_val)
        print 'warining critical', warning_res,critical_res
        if critical_res:
            print u"\033[41;1mCRITICAL::\033[0mHost[%s] Service[%s] 法治[%s] 当前值[%s]" %(
                client_service_data['host'],client_service_data['service'],critical_val,item_data
            )
        elif warning_res:
            print u"\033[43;1mWARNING::\033[0mHost[%s] Service[%s] 法治[%s] 当前值[%s]" %(
                client_service_data['host'],client_service_data['service'],critical_val,item_data
            )
        else:
            print u"\033[42;1mNORMAL::\033[0mHost[%s] Service[%s] 法治[%s] 当前值[%s]" %(
                client_service_data['host'],client_service_data['service'],critical_val,item_data
            )