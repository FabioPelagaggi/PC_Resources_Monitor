import socket, psutil, pickle, platform, cpuinfo, os, nmap, threading, subprocess, datetime

### Functions ###
def subnetwork_mapping(operational_system_data, subnetwork):
    hosts = hosts_scan(operational_system_data, subnetwork)
    IPs = ips_scan(hosts)
    hosts_data.append(hosts)
    ips_data.append(IPs)

def get_ip_addresses(family):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family:
                yield (interface, snic.address)

def ping(operational_system_data, hostname):
    args = []
    if operational_system_data == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]
    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]
    ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    return ret_cod

def hosts_scan(operational_system_data, subnetwork):
    print("Mapping", subnetwork, "subnetwork...\r")
    hosts_list = []
    return_codes = dict()
    for i in range(1, 255):
        host_test = (subnetwork + '{0}'.format(i))
        return_codes[subnetwork + '{0}'.format(i)] = ping(operational_system_data, host_test)
        if i %20 == 0:
            print(".", end = "")
        if return_codes[subnetwork + '{0}'.format(i)] == 0:
            hosts_list.append(subnetwork + '{0}'.format(i))
    print("\nMapping ready.")
    print("Hosts found:", hosts_list)
    return hosts_list

def ips_scan(hosts_list):
    nm = nmap.PortScanner()
    IPs = dict()
    for i in hosts_list: 
        try:
            print("Scanning", i, "IP...")     
            nm.scan(i)
            IPs[i] = nm[i]
            print("IP", i,"Scanned.")
        except:
            print("IP", i,"Failed.")
            continue
    print("Scanning Ready.")
    return IPs

def hosts_info(hosts_data, ips_data):
    IPs = dict()
    IPs_Info = ips_data[0]
    hosts = hosts_data[0]
    for i in hosts:
        IPs[i] = dict()
        try:
            IPs[i]['mac'] = IPs_Info[i]['addresses']['mac']
        except:
            pass
        try:
            IPs[i]['vendor'] = IPs_Info[i]['vendor'][IPs_Info[i]['addresses']['mac']]
        except:
            pass
        try:
            IPs[i]['response'] = IPs_Info[i]['status']['reason']
        except:
            pass
        try:
            IPs[i]['product'] = IPs_Info[i]['product']
            print(IPs[i]['product'])
        except:
            pass
    return IPs

def traffic_interface_scanner():
    io_status = psutil.net_io_counters(pernic=True)
    interface_names = list()
    for i in io_status:
        interface_names.append(str(i))
    interfaces_traffic = dict()
    for j in interface_names:
        interfaces_traffic[j] = dict()
        interfaces_traffic[j]['bytes_sent'] = io_status[j][0]
        interfaces_traffic[j]['bytes_recv'] = io_status[j][1]
        interfaces_traffic[j]['packets_sent'] = io_status[j][2]
        interfaces_traffic[j]['packets_recv'] = io_status[j][3]
    return interfaces_traffic

def scan_files(local_data):
    lista = os.listdir(local_data)
    files = dict()
    for i in lista:
        filepath = os.path.join(local_data, i)
        if os.path.isfile(filepath):
            files[i] = dict()
            files[i]['Size'] = os.stat(filepath).st_size
            files[i]['Created'] = datetime.datetime.fromtimestamp(os.stat(filepath).st_ctime).strftime("%d-%m-%Y %H:%M:%S")
            files[i]['Mod'] = datetime.datetime.fromtimestamp(os.stat(filepath).st_mtime).strftime("%d-%m-%Y %H:%M:%S")
    return files

def scann_process_data():
    processes = psutil.pids()
    process_data = dict()
    for i in processes:
        try:
            p = psutil.Process(i)
            proc_name = str(p.name())
            if proc_name not in process_data:
                process_data[proc_name] = dict()
                process_data[proc_name]['Status'] = list()
                process_data[proc_name]['PIDs'] = list()
                process_data[proc_name]['Create Time'] = list()
                process_data[proc_name]['Connections'] = list()
            process_data[proc_name]['Status'].append(p.status())
            process_data[proc_name]['PIDs'].append(i)
            process_data[proc_name]['Create Time'].append(datetime.datetime.fromtimestamp(p.create_time()).strftime("%d-%m-%Y %H:%M:%S"))
            if p.connections() != []:
                process_data[proc_name]['Connections'].append(p.connections())
            else:
                process_data[proc_name]['Connections'].append('OFFLINE')
        except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
            continue

    all_process_data = dict()
    for i in process_data:
        all_process_data[i] = dict()
        all_process_data[i]['Qty PIDs'] = len(process_data[i]['PIDs'])
        all_process_data[i]['PIDs List'] = process_data[i]['PIDs']
        for j in range(all_process_data[i]['Qty PIDs']):
            all_process_data[i][process_data[i]['PIDs'][j]] = dict()
            all_process_data[i][process_data[i]['PIDs'][j]]['#'] = process_data[i]['PIDs'][j]
            all_process_data[i][process_data[i]['PIDs'][j]]['Status'] = process_data[i]['Status'][j]
            all_process_data[i][process_data[i]['PIDs'][j]]['Create Time'] = process_data[i]['Create Time'][j]
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections'] = dict()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Connections Status'] = list()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Address Family'] = list()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Packets Type'] = list()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['LIP'] = list()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['LPort'] = list()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['RIP'] = list()
            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['RPort'] = list()
            if process_data[i]['Connections'][j] != 'OFFLINE':
                for c in process_data[i]['Connections'][j]:
                    all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Connections Status'].append(c.status)
                    if c.family == socket.AF_INET:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Address Family'].append('IPv4')
                    elif c.family == socket.AF_INET6:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Address Family'].append('IPv6')
                    elif c.family == socket.AF_UNIX:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Address Family'].append('Unix')
                    else:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Address Family'].append('-')
                    
                    if c.type == socket.SOCK_STREAM:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Packets Type'].append('TCP')
                    elif c.type == socket.SOCK_DGRAM:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Packets Type'].append('UDP')
                    elif c.type == socket.SOCK_RAW:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Packets Type'].append('IP')
                    else:
                        all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Packets Type'].append('-')

                    d_count = 1
                    for d in c.laddr:
                        if d_count == 1:
                            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['LIP'].append(d)
                            d_count += 1
                        elif d_count == 2:
                            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['LPort'].append(d)
                            d_count = 1
                    for d in c.raddr:
                        if d_count == 1:
                            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['RIP'].append(d)
                            d_count += 1
                        elif d_count == 2:
                            all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['RPort'].append(d)
                            d_count = 1
            else:
                all_process_data[i][process_data[i]['PIDs'][j]]['Connections']['Connections Status'] = process_data[i]['Connections'][j]
    return all_process_data

### DATA ###
# Network
ipv4s_data = list(get_ip_addresses(socket.AF_INET))
ipv6s_data = list(get_ip_addresses(socket.AF_INET6))
mac_address_data = list(get_ip_addresses(psutil.AF_LINK))
subnetwork = ".".join(ipv4s_data[0][1].split('.')[0:3]) + '.'
hosts_data = list()
ips_data = list()
traffic_interface_data = traffic_interface_scanner()
# PC
pc_name_data = platform.node()
operational_system_data = platform.system()
os_version_data = platform.version()
arc_data = platform.machine()
# CPU
cpu_info_data = cpuinfo.get_cpu_info()
p_cores_data = psutil.cpu_count(logical=False)
l_cores_data = psutil.cpu_count(logical=True)
# HD
pc_partitions_data = psutil.disk_partitions(all)
primary_storage_data = pc_partitions_data[0][0]
# Files Page
local_data = os.path.dirname(os.path.realpath(__file__))
print(local_data)
## Process
processes_data = scann_process_data()

### Main Loop ###
def main():
    ### Server ###
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()                         
    port = 666
    socket_server.bind((host, port))

    socket_server.listen()
    print("Server", host, "ready for connection on", port,"port.")
    (socket_client, addr) = socket_server.accept()
    print("Connected to:", str(addr))

    hosts_mapped = False
    while True:
        try:
            if not hosts_mapped:
                thread_mapping = threading.Thread(target=subnetwork_mapping, args=[operational_system_data, subnetwork])
                thread_mapping.start()
                hosts_mapped = True
            pag_data = socket_client.recv(51200)
            data = dict()
            if pag_data.decode('utf-8') == 'HOME':
                data['cpu_percent'] = psutil.cpu_percent(interval=1)
                data['cpu_max_freq'] = psutil.cpu_freq().max
                data['mem'] = psutil.virtual_memory()
                data['hd'] = psutil.disk_usage(str(primary_storage_data))
                data['pc_name'] = pc_name_data
                data['os'] = operational_system_data
                data['os_version'] = os_version_data
                data['cpu_info'] = cpu_info_data
                data['cpu_arc'] = arc_data
                data['cpu_pcores'] = p_cores_data
                data['cpu_lcores'] = l_cores_data
            elif pag_data.decode('utf-8') == 'CPU':
                data['cpu_percent'] = psutil.cpu_percent(interval=1)
                data['cpu_max_freq'] = psutil.cpu_freq().max
                data['cpu_cores_percent'] = psutil.cpu_percent(interval=1, percpu=True)
                data['pc_name'] = pc_name_data
                data['os'] = operational_system_data
                data['os_version'] = os_version_data
                data['cpu_info'] = cpu_info_data
                data['cpu_arc'] = arc_data
                data['cpu_pcores'] = p_cores_data
                data['cpu_lcores'] = l_cores_data
            elif pag_data.decode('utf-8') == 'FILES':
                files_data = scan_files(local_data)
                data['local'] = local_data
                data['files'] = files_data
            elif pag_data.decode('utf-8') == 'PROCESS':
                data['hosts'] = hosts_data
                data['ips'] = ips_data
                data['processes'] = processes_data
                data['traffic_interface'] = traffic_interface_scanner()
                data['ipv4s'] = ipv4s_data
                data['mac_address'] = mac_address_data
            bytes_resp = pickle.dumps(data)
            socket_client.send(bytes_resp)
        except:
            os._exit(0)
            socket_client.close()
            socket_server.close()

if __name__ == "__main__":
    main()