__author__ = 'alex'


import templates


web_clusters = templates.LinuxGenericTemplate()
web_clusters.hosts = ['192.168.2.230',
                      '10.0.4.102',
                      '172.23.2.33',
                      '192.168.1.199'
                      ]
mysql_groups = templates.Linux2()
mysql_groups.hosts = ['192.168.4.88',
                      '10.0.4.102'
                      ]

monitored_groups = [mysql_groups,web_clusters]

if __name__ == "__main__":
    host_config_dic = {}
    for group in monitored_groups:
        #print group.name
        for h in group.hosts:
            #print h ,group.services
            if h not in host_config_dic:
                host_config_dic[h] = {}
            for s in group.services:
                host_config_dic[h][s.name] = [s.plugin_name, s.interval]
    for h,v in host_config_dic.items():
        print h ,v