import functions

import psutil
import platform
import os
import socket
import cpuinfo

### Mapping Function ###
def subnetwork_mapping(operational_system_data, subnetwork):
    hosts = functions.hosts_scan(operational_system_data, subnetwork)
    IPs = functions.ips_scan(hosts)
    hosts_data.append(hosts)
    ips_data.append(IPs)

### Network ###
ipv4s_data = list(functions.get_ip_addresses(socket.AF_INET))
ipv6s_data = list(functions.get_ip_addresses(socket.AF_INET6))
mac_address_data = list(functions.get_ip_addresses(psutil.AF_LINK))
subnetwork = ".".join(ipv4s_data[0][1].split('.')[0:3]) + '.'
hosts_data = list()
ips_data = list()
traffic_interface_data = functions.traffic_interface_scanner()

### PC ###
pc_name_data = platform.node()
operational_system_data = platform.system()
os_version_data = platform.version()
arc_data = platform.machine()

### CPU ###
cpu_data = cpuinfo.get_cpu_info()
p_cores_data = psutil.cpu_count(logical=False)
l_cores_data = psutil.cpu_count(logical=True)
cpu_percent_data = psutil.cpu_percent(interval=1)
cpu_cores_percent_data = psutil.cpu_percent(interval=1, percpu=True)
cpu_max_freq_data =  psutil.cpu_freq().max

### Memory ###
mem_data = psutil.virtual_memory()

### HD ###
pc_partitions_data = psutil.disk_partitions(all)
primary_storage_data = pc_partitions_data[0][0]
hd_data = psutil.disk_usage(str(primary_storage_data))

### Files Page ###
local_data = os.path.dirname(os.path.realpath(__file__))

## Process
processes_data = functions.scann_process_data()