import interface

import pygame
import psutil
import os
import datetime
import socket
import subprocess
import nmap

## Network
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

def connection_check(status):
    if status == 'OK':
        return 'ONLINE'
    elif status == 'ERROR':
        return 'OFFLINE'

## CPU
def cpu_graph_1(connection, cpu_percent_data, cpu_max_freq_data):
    # Data
    if connection == 'ONLINE':
        freq_per_cent = int(cpu_percent_data)
        freq_max = cpu_max_freq_data
    else:
        freq_per_cent = int(psutil.cpu_percent(interval=1))
        freq_max = psutil.cpu_freq().max
    
    freq_current = ((freq_max * freq_per_cent)/100)

    # Display
    interface.s.fill(interface.background)
    
    width_bar_1 = int(interface.WINDOW_WIDTH - 2*20)
    pygame.draw.rect(interface.s, interface.black, (25, 70, width_bar_1, 70))
    pygame.draw.rect(interface.s, interface.grey_blue2, (20, 65, width_bar_1, 70))
    width_bar_2 = int((width_bar_1*freq_per_cent) / 100)
    pygame.draw.rect(interface.s, interface.black, (25, 70, width_bar_2, 70))
    pygame.draw.rect(interface.s, interface.red, (20, 65, width_bar_2, 70))

    pygame.draw.rect(interface.s, interface.black, ((558), (15), (129), (29)))
    pygame.draw.rect(interface.s, interface.background, ((560), (17), (125), (25)))
    pygame.draw.rect(interface.s, interface.black, ((683), (15), (99), (29)))
    pygame.draw.rect(interface.s, interface.background, ((685), (17), (95), (25)))

    pygame.draw.line(interface.s, interface.black, (0,0), ((interface.WINDOW_WIDTH), 0), 8)
    pygame.draw.line(interface.s, interface.black, (0,0), (0, (interface.WINDOW_HEIGHT)), 8)
    pygame.draw.line(interface.s, interface.black, ((interface.WINDOW_WIDTH),0), ((interface.WINDOW_WIDTH), (interface.WINDOW_HEIGHT)), 12)
    pygame.draw.line(interface.s, interface.black, (15,54), ((interface.WINDOW_WIDTH - 15), 54), 6)
    
    bar_text_1 = "CPU Usage"
    bar_text_2 = "Current Frequency"
    bar_text_3 = str(freq_current) + " MHz"
    bar_text_inside_1 = str(freq_per_cent) + "%"
    bar_text_inside_2 = str((100 - freq_per_cent)) + "%"
    interface.s.blit(interface.font_1.render(bar_text_1, 10, interface.grey), (20, 18))
    interface.s.blit(interface.font_3.render(bar_text_2, 10, interface.grey), (565, 23))
    interface.s.blit(interface.font_3.render(bar_text_3, 10, interface.dark_sand), (700, 23))
    interface.s.blit(interface.font_2.render(bar_text_inside_1, 10, interface.sand2), (35, 110))
    interface.s.blit(interface.font_2.render(bar_text_inside_2, 10, interface.dark_sand), (730, 110))
    
    interface.window.blit(interface.s, (0, 0))

def cpu_graph_2(connection, cpu_cores_percent_data):
    # Data
    if connection == 'ONLINE':
        cores_percent = cpu_cores_percent_data
    else:
        cores_percent = psutil.cpu_percent(interval=1, percpu=True)

    cores = len(cores_percent)

    # Display
    interface.s_cpu.fill(interface.background)

    x = y = shift = 10
    d = x + shift
    height = int(interface.s_cpu.get_height() - 2*y)
    width = int((interface.s_cpu.get_width() - 2*y - (cores + 1)*shift ) / cores)
    cores_count = 1
    for i in cores_percent:
        pygame.draw.rect(interface.s_cpu, interface.black, (d+5, y+5, width, height))
        pygame.draw.rect(interface.s_cpu, interface.red, (d, y, width, height))
        pygame.draw.rect(interface.s_cpu, interface.grey_blue2, (d, y, width, ((1-i/100)*height)))
        
        bar_text_inside = str(int(i)) + "%"
        interface.s_cpu.blit(interface.font_3.render(bar_text_inside, 10, interface.sand2), ((d + (width/3)), (height - 10)))
        bar_text_inside = "#"+str(cores_count) 
        interface.s_cpu.blit(interface.font_3.render(bar_text_inside, 10, interface.dark_sand), ((d + (width/3)), y+10))
        
        cores_count += 1
        d = d + width + shift
    
    pygame.draw.line(interface.s_cpu, interface.black, (0,0), (0, (interface.WINDOW_HEIGHT)), 8)
    pygame.draw.line(interface.s_cpu, interface.black, ((interface.WINDOW_WIDTH),0), ((interface.WINDOW_WIDTH), (interface.WINDOW_HEIGHT)), 12)
    interface.window.blit(interface.s_cpu, (0, (interface.WINDOW_HEIGHT)/4))

## Memory
def mem_graph(connection, mem_data):
    # Data
    if connection == 'ONLINE':
        mem = mem_data
    else:
        mem = psutil.virtual_memory()

    mem_total = round((mem.total / (1024*1024*1024)), 2)
    mem_used = round((mem.used / (1024*1024*1024)), 2)
    mem_free = round((mem.free / (1024*1024*1024)), 2)
    mem_percent = int(mem.percent)
    
    # Display
    interface.s.fill(interface.background)

    width_bar_1 = int(interface.WINDOW_WIDTH - 2*20)
    pygame.draw.rect(interface.s, interface.black, (25, 70, width_bar_1, 70))
    pygame.draw.rect(interface.s, interface.grey_blue2, (20, 65, width_bar_1, 70))
    width_bar_2 = int((width_bar_1*mem.percent) / 100)
    pygame.draw.rect(interface.s, interface.black, (25, 70, width_bar_2, 70))
    pygame.draw.rect(interface.s, interface.red, (20, 65, width_bar_2, 70))

    pygame.draw.rect(interface.s, interface.black, ((643), (10), (49), (29)))
    pygame.draw.rect(interface.s, interface.background, ((645), (12), (45), (25)))
    pygame.draw.rect(interface.s, interface.black, ((688), (10), (79), (29)))
    pygame.draw.rect(interface.s, interface.background, ((690), (12), (75), (25)))

    pygame.draw.line(interface.s, interface.black, (0,0), ((interface.WINDOW_WIDTH), 0), 8)
    pygame.draw.line(interface.s, interface.black, (0,0), (0, (interface.WINDOW_HEIGHT)), 8)
    pygame.draw.line(interface.s, interface.black, ((interface.WINDOW_WIDTH),0), ((interface.WINDOW_WIDTH), (interface.WINDOW_HEIGHT)), 12)
    pygame.draw.line(interface.s, interface.black, (15,45), ((interface.WINDOW_WIDTH -15), 45), 6)

    bar_text_1 = "Memory Usage"
    bar_text_2 = "Total"
    bar_text_3 = str(mem_total) + " GB"
    bar_text_inside_1 = str(mem_used) + " Used"
    bar_text_inside_2 = str(mem_free) + " Free"
    bar_text_inside_3 = str(mem_percent) + "%"
    bar_text_inside_4 = str(100 - mem_percent) + "%"
    interface.s.blit(interface.font_1.render(bar_text_1, 10, interface.grey), (20, 13))
    interface.s.blit(interface.font_3.render(bar_text_2, 10, interface.grey), (653, 18))    
    interface.s.blit(interface.font_3.render(bar_text_3, 10, interface.dark_sand), (700, 18))    
    interface.s.blit(interface.font_2.render(bar_text_inside_1, 10, interface.sand2), (35, 110))
    interface.s.blit(interface.font_2.render(bar_text_inside_2, 10, interface.dark_sand), (675, 110))
    interface.s.blit(interface.font_2.render(bar_text_inside_3, 10, interface.sand2), (35, 75))
    interface.s.blit(interface.font_2.render(bar_text_inside_4, 10, interface.dark_sand), (730, 75))
    
    interface.window.blit(interface.s, (0, ((interface.WINDOW_HEIGHT)/4)))

## HD
def hd_graph(connection, hd_data):
    # Data
    if connection == 'ONLINE':
        hd = hd_data
    else:
        hd = hd_data

    hd_total = round((hd.total / (1024*1024*1024)), 2)
    hd_used = round((hd.used / (1024*1024*1024)), 2)
    hd_free = round((hd.free / (1024*1024*1024)), 2)
    hd_percent = int(hd.percent)

    # Display
    interface.s.fill(interface.background)

    width_bar_1 = int(interface.WINDOW_WIDTH - 2*20)  
    pygame.draw.rect(interface.s, interface.black, (25, 70, width_bar_1, 70))
    pygame.draw.rect(interface.s, interface.grey_blue2, (20, 65, width_bar_1, 70))
    width_bar_2 = int((width_bar_1*hd.percent) / 100)
    pygame.draw.rect(interface.s, interface.black, (25, 70, width_bar_2, 70))
    pygame.draw.rect(interface.s, interface.red, (20, 65, width_bar_2, 70))
    
    pygame.draw.rect(interface.s, interface.black, ((643), (10), (49), (29)))
    pygame.draw.rect(interface.s, interface.background, ((645), (12), (45), (25)))
    pygame.draw.rect(interface.s, interface.black, ((688), (10), (84), (29)))
    pygame.draw.rect(interface.s, interface.background, ((690), (12), (80), (25)))

    pygame.draw.line(interface.s, interface.black, (0,0), ((interface.WINDOW_WIDTH), 0), 8)
    pygame.draw.line(interface.s, interface.black, (0,0), (0, (interface.WINDOW_HEIGHT)), 8)
    pygame.draw.line(interface.s, interface.black, ((interface.WINDOW_WIDTH),0), ((interface.WINDOW_WIDTH), (interface.WINDOW_HEIGHT)), 12)
    pygame.draw.line(interface.s, interface.black, (15,45), ((interface.WINDOW_WIDTH -15), 45), 6)
    
    bar_text_1 = "Primary Storage Usage"
    bar_text_2 = "Total"
    bar_text_3 = str(hd_total) + " GB"
    bar_text_inside_01 = str(hd_used) + " Used"
    bar_text_inside_02 = str(hd_free) + " Free"
    bar_text_inside_03 = str(hd_percent) + "%"
    bar_text_inside_04 = str(100 - hd_percent) + "%"
    interface.s.blit(interface.font_1.render(bar_text_1, 10, interface.grey), (20, 13))
    interface.s.blit(interface.font_3.render(bar_text_2, 10, interface.grey), (653, 18))    
    interface.s.blit(interface.font_3.render(bar_text_3, 10, interface.dark_sand), (700, 18))
    interface.s.blit(interface.font_2.render(bar_text_inside_01, 10, interface.sand2), (35, 110))
    interface.s.blit(interface.font_2.render(bar_text_inside_02, 10, interface.dark_sand), (675, 110))
    interface.s.blit(interface.font_2.render(bar_text_inside_03, 10, interface.sand2), (35, 75))
    interface.s.blit(interface.font_2.render(bar_text_inside_04, 10, interface.dark_sand), (730, 75))
    
    interface.window.blit(interface.s, (0, ((((interface.WINDOW_HEIGHT)/4)*2))))

## Informations
def pc_cpu_inf(pc_name_data, operational_system_data, os_version_data, cpu_data, arc_data, p_cores_data, l_cores_data):
    # Data
    inf = cpu_data
    cpu_name = inf['brand_raw']
    cpu_arch = inf['arch']
    cpu_bits = inf['bits']
    p_cores = p_cores_data
    l_cores = l_cores_data

    # Diplay
    interface.s_info.fill(interface.background)
    interface.s.fill(interface.black)
    
    text = "PC & CPU Information"
    interface.s_info.blit(interface.font_1.render(text, 10, interface.grey), (20, 10))
    pygame.draw.line(interface.s_info, interface.black, (10,45), ((interface.WINDOW_WIDTH -20), 45), 6)
    
    pos_zero_x = 20
    pos_zero_y = 55
    box_zero_size_x = 73
    box_zero_size_y = 15
    pos_x = pos_zero_x
    pos_y = pos_zero_y
    box_size_x = box_zero_size_x
    box_size_y = box_zero_size_y

    box_size_x = 65
    text = "PC Name"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(pc_name_data)
    box_size_x = 213
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = pos_zero_x

    pos_y += 17
    box_size_x = 110
    text = "Operating System"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(operational_system_data) + " " + str(os_version_data)
    box_size_x = 175
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = pos_zero_x
    
    pos_y += 17
    box_size_x = box_zero_size_x
    text = "CPU Name"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(cpu_name)
    box_size_x = 225
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = pos_zero_x

    pos_y += 17
    box_size_x = 80
    text = "Architecture"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(cpu_arch) + " (" + str(arc_data) + ")"
    box_size_x = 105
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = pos_zero_x

    pos_y += 17
    box_size_x = 85
    text = "Word Length"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(cpu_bits) + " bits"
    box_size_x = 65
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = (pos_zero_x + 400)

    pos_y = pos_zero_y
    box_size_x = 45
    text = "Cores"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_y += 17
    box_size_x = 60
    text = "Physical"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(p_cores)
    box_size_x = 20
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = (pos_zero_x + 400)
    pos_y += 17
    box_size_x = 55
    text = "Logical"
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.dark_sand), ((pos_x + 5), (pos_y + 3)))
    pos_x += box_size_x
    text = str(l_cores)
    box_size_x = 25
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x + 1), (pos_y + 1), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.black, ((pos_x - 2), (pos_y - 2), (box_size_x + 4), (box_size_y + 4)))
    pygame.draw.rect(interface.s_info, interface.background, ((pos_x), (pos_y), (box_size_x), (box_size_y)))
    interface.s_info.blit(interface.font_4.render(text, 10, interface.grey), ((pos_x + 5), (pos_y + 3)))
    pos_x = (pos_zero_x + 400)

    interface.window.blit(interface.s, (0, ((((interface.WINDOW_HEIGHT)/4)*3))))
    interface.window.blit(interface.s_info, (5, (((((interface.WINDOW_HEIGHT)/4)*3)+5))))

## Files Page
def files_page_header(local_data, files_page_number_data, files_page_menu):
    interface.s_header.fill(interface.background)
    
    if (((files_page_number_data) > (1)) and ((int(files_page_menu)) < (files_page_number_data))):
        interface.display_next_page_buttom()
    if files_page_menu != '1':
        interface.display_back_page_buttom()

    pos_x = 20
    pos_y = 10
    text_0 = "Local Files"
    interface.s_header.blit(interface.font_1.render(text_0, 10, interface.grey), (pos_x, pos_y))
    pos_y += 30
    text_1 = str(local_data)
    interface.s_header.blit(interface.font_3.render(text_1, 10, interface.grey), (pos_x, pos_y))
    pos_y += 28

    pygame.draw.line(interface.s_header, interface.black, (0,0), ((interface.WINDOW_WIDTH), 0), 8)
    pygame.draw.line(interface.s_header, interface.black, (10,60), ((interface.WINDOW_WIDTH -20), 60), 6)

    interface.window.blit(interface.s_header, (interface.pos_x_s_header, interface.pos_y_s_header))

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

def create_files_pages(files_data):
    files = files_data
    files_count = 1
    page_number = 1
    pages = dict()
    pages[page_number] = dict()
    for i in list(files):
        pages[page_number][i] = dict()
        pages[page_number][i]['Size'] = files[i]['Size']
        pages[page_number][i]['Created'] = files[i]['Created']
        pages[page_number][i]['Mod'] = files[i]['Mod']
        files_count += 1
        if files_count > 12:
            page_number += 1
            pages[page_number] = dict()
            files_count = 1
    return pages

def files_pages_count(files_pages_data):
    return len(files_pages_data)

def files_display(files_pages_data, files_page_menu):
    interface.s_pag.fill(interface.background)
    interface.s_pag_border.fill(interface.black)

    files = files_pages_data[int(files_page_menu)]

    pos_x_files = 47
    pos_y_files = 78
    files_count = 0
    for i in list(files):
        file_text = '{:^0.34}'.format(str(i))
        file_size_text = "Size: " + '{:^0.38}'.format(str(files[i]['Size']) + " bytes")
        file_created_text = "Created: " + '{:^0.38}'.format(str(files[i]['Created']))
        file_mod_text = "Modification: "+ '{:^0.38}'.format(str(files[i]['Mod']))

        pygame.draw.rect(interface.s_pag, interface.black, (pos_x_files, pos_y_files+3, int((interface.WINDOW_WIDTH)/2)-75, (73)))
        pygame.draw.rect(interface.s_pag, interface.black, (pos_x_files-5, pos_y_files-4, int((interface.WINDOW_WIDTH)/2)-75, (22)))
        pygame.draw.rect(interface.s_pag, interface.grey2, (pos_x_files-4, pos_y_files-3, int((interface.WINDOW_WIDTH)/2)-77, (20)))
        interface.s_pag.blit(interface.font_3.render(file_text, 10, interface.dark_sand), (pos_x_files + 8, pos_y_files))
        pygame.draw.circle(interface.s_pag, interface.black, ((pos_x_files-5),(pos_y_files + 8)), 8)
        pygame.draw.circle(interface.s_pag, interface.grey2, ((pos_x_files-5),(pos_y_files + 8)), 6)
        pos_y_files += 18
        pygame.draw.rect(interface.s_pag, interface.black, (pos_x_files-5, pos_y_files, int((interface.WINDOW_WIDTH)/2)-75, (53)))
        pygame.draw.rect(interface.s_pag, interface.grey2, (pos_x_files-4, pos_y_files+1, int((interface.WINDOW_WIDTH)/2)-77, (51)))
        pos_y_files += 5
        interface.s_pag.blit(interface.font_4.render(file_size_text, 10, interface.dark_sand), (pos_x_files, pos_y_files))
        pos_y_files += 15
        interface.s_pag.blit(interface.font_4.render(file_created_text, 10, interface.dark_sand), (pos_x_files, pos_y_files))
        pos_y_files += 15
        interface.s_pag.blit(interface.font_4.render(file_mod_text, 10, interface.dark_sand), (pos_x_files, pos_y_files))
        pos_y_files += 30
        
        files_count += 1
        if (files_count == 6):
            pos_x_files += int(((interface.WINDOW_WIDTH)/2)-22)
            pos_y_files = 78

    interface.window.blit(interface.s_pag_border, (0, 0))
    interface.window.blit(interface.s_pag, (5, 5))

#Processes
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

# Display Network and Processes
def network_and_processes_page_header(processes_page_menu):
    interface.s_header.fill(interface.background)
    
    interface.display_pg_dowm_buttom()
    interface.display_pg_up_buttom()
    interface.display_pg_end_buttom()
    interface.display_pg_top_buttom()

    pos_x = 20
    pos_y = 20
    text_0 = "Network & Process Information"
    interface.s_header.blit(interface.font_1.render(text_0, 10, interface.grey), (pos_x, pos_y))

    pygame.draw.line(interface.s_header, interface.black, (0,0), ((interface.WINDOW_WIDTH), 0), 8)
    pygame.draw.line(interface.s_header, interface.black, (10,60), ((interface.WINDOW_WIDTH -20), 60), 6)

    interface.window.blit(interface.s_header, (interface.pos_x_s_header, interface.pos_y_s_header))

def network_and_processes_display(connection, hosts_data, ips_data, processes_data, traffic_interface_data, ipv4s_data, mac_address_data, processes_page_scroll_y, processes_page_menu):  
    interface.s_pag_scroll.fill(interface.background)
    interface.s_pag_border.fill(interface.black)

    process_data = processes_data

    pos_zero_x_process = 450
    pos_zero_y_process = 75
    pos_x_process = pos_zero_x_process
    pos_y_process = pos_zero_y_process
    box_name_size_x = 250
    box_name_size_y = 20
    box_size_x = 46
    box_size_y = 19
    for i in process_data:
        pos_x_process = pos_zero_x_process

        Name_txt = str(i)
        pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_name_size_x + 2), (box_name_size_y + 2)))
        pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_name_size_x + 2), (box_name_size_y + 2)))
        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_name_size_x, box_name_size_y))
        interface.s_pag_scroll.blit(interface.font_3.render(Name_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 3)))
        
        pos_x_ball = pos_x_process
        pos_y_ball = pos_y_process
        pos_y_process += 21
        Head_txt = "Qty of PIDs:"
        box_size_x = 100
        pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
        pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
        interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
        pos_x_process += box_size_x
        
        Resut_txt = str(process_data[i]['Qty PIDs'])
        box_size_x = 55
        pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
        pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
        interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
        pos_x_process = pos_zero_x_process

        ### PIDs Horizontal Stats
        for f in process_data[i]['PIDs List']:
            pos_x_process = pos_zero_x_process
            pos_y_process += 20

            Head_txt = "PID"
            box_size_x = 55
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
            pos_y_process += 20

            Resut_txt = str(process_data[i][f]['#'])
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
            pos_x_process += box_size_x
            pos_y_process -= 20

            Head_txt = "Status"
            box_size_x = 73
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
            pos_y_process += 20

            Resut_txt = str(process_data[i][f]['Status'])
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
            pos_x_process += box_size_x
            pos_y_process -= 20

            Head_txt = "Create Time"
            box_size_x = 152
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
            pos_y_process += 20

            Resut_txt = str(process_data[i][f]['Create Time'])
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
            
            if process_data[i][f]['Connections']['Connections Status'] != 'OFFLINE':
                pygame.draw.circle(interface.s_pag_scroll, interface.black, ((pos_x_ball),(pos_y_ball + 10)), 8)
                pygame.draw.circle(interface.s_pag_scroll, interface.grey_blue2, ((pos_x_ball),(pos_y_ball + 10)), 6)
                
                for d in range(len(process_data[i][f]['Connections']['Connections Status'])):
                    pos_x_process = pos_zero_x_process
                    pos_y_process += 20
                    Head_txt = "Connection:"
                    box_size_x = 90
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_x_process += box_size_x
                    
                    Resut_txt = str(process_data[i][f]['Connections']['Connections Status'][d])
                    box_size_x = 100
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_x_process += box_size_x
                        
                    Resut_txt = str(process_data[i][f]['Connections']['Address Family'][d])
                    box_size_x = 50
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_x_process += box_size_x

                    Resut_txt = str(process_data[i][f]['Connections']['Packets Type'][d])
                    box_size_x = 40
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_y_process += 20
                    pos_x_process = pos_zero_x_process

                    Head_txt = "Local IP:"
                    box_size_x = 90
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_x_process += box_size_x
                    
                    Resut_txt = '{:.15}'.format(str(process_data[i][f]['Connections']['LIP'][d]))
                    box_size_x = 100
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_x_process += box_size_x

                    Resut_txt = str(process_data[i][f]['Connections']['LPort'][d])
                    box_size_x = 90
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                    interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                    pos_x_process = pos_zero_x_process

                    if process_data[i][f]['Connections']['RIP'] != []:
                        pos_y_process += 20
                        try:
                            Head_txt = "Remote IP:"
                            box_size_x = 90
                            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                            interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
                            pos_x_process += box_size_x
                           
                            Resut_txt = '{:.15}'.format(str(process_data[i][f]['Connections']['RIP'][d]))
                            box_size_x = 100
                            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                            interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                            pos_x_process += box_size_x
                            
                            Resut_txt = str(process_data[i][f]['Connections']['RPort'][d])
                            box_size_x = 90
                            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                            pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                            interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
                            pos_x_process = pos_zero_x_process
                        except:
                            continue
            else:
                pygame.draw.circle(interface.s_pag_scroll, interface.black, ((pos_x_ball),(pos_y_ball + 10)), 8)
                pygame.draw.circle(interface.s_pag_scroll, interface.red, ((pos_x_ball),(pos_y_ball + 10)), 6)

                pos_x_process = pos_zero_x_process
                pos_y_process += 20

                Head_txt = "Connection:"
                box_size_x = 90
                pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                interface.s_pag_scroll.blit(interface.font_4.render(Head_txt, 10, interface.dark_sand), ((pos_x_process + 10), (pos_y_process + 5)))
                pos_x_process += box_size_x
                
                Resut_txt = str(process_data[i][f]['Connections']['Connections Status'])
                box_size_x = 100
                pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process + 3), (pos_y_process + 3), (box_size_x + 2), (box_size_y + 2)))
                pygame.draw.rect(interface.s_pag_scroll, interface.black, ((pos_x_process - 1), (pos_y_process - 1), (box_size_x + 2), (box_size_y + 2)))
                pygame.draw.rect(interface.s_pag_scroll, interface.grey2, ((pos_x_process), (pos_y_process), box_size_x, box_size_y))
                interface.s_pag_scroll.blit(interface.font_4.render(Resut_txt, 10, interface.grey), ((pos_x_process + 10), (pos_y_process + 5)))
        pos_y_process += 30
    
    if connection == 'ONLINE':
        traffic = traffic_interface_data
    else:    
        traffic = traffic_interface_scanner()

    ip_mac_count = 0
    box_size_x = 43
    box_size_y = 19
    pos_x_traffic = 47
    pos_y_traffic = 78
    for i in list(traffic):
        if (str(i) != 'Loopback Pseudo-Interface 1'):
            pos_x_traffic = 47
            box_size_x = 43
            text = str(i)
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic-1, int((interface.WINDOW_WIDTH)/2)-155, (22)))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic-4, int((interface.WINDOW_WIDTH)/2)-155, (22)))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic-3, int((interface.WINDOW_WIDTH)/2)-157, (20)))
            interface.s_pag_scroll.blit(interface.font_3.render(text, 10, interface.dark_sand), (pos_x_traffic + 8, pos_y_traffic))
            
            pygame.draw.polygon(interface.s_pag_scroll, interface.black, (((pos_x_traffic-4),(pos_y_traffic+1)), (pos_x_traffic + 3, pos_y_traffic + 6), (pos_x_traffic-4, pos_y_traffic + 11)))

            pos_y_traffic += 18
            text = "Bytes"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            text = "Sent"
            box_size_x -= 3
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x += 50
            text = '{:^0.38}'.format(str(traffic[i]['bytes_sent']))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x -= 25
            text = "Received"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x += 30
            text = '{:^0.37}'.format(str(traffic[i]['bytes_recv']))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic = 47
            pos_y_traffic += 21
            box_size_x -= 40
            text = "Packets"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x -= 15
            text = "Sent"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic+3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x += 38
            text = '{:^0.38}'.format(str(traffic[i]['packets_sent']))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x -= 13
            text = "Received"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x += 30
            text = '{:^0.38}'.format(str(traffic[i]['packets_sent']))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic = 47
            pos_y_traffic += 21
            box_size_x -= 57
            text = "IPv4"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x += 50
            text = '{:^0.38}'.format(str(ipv4s_data[ip_mac_count][1]))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x -= 45
            text = "MAC"
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))

            pos_x_traffic += box_size_x + 2
            box_size_x += 80
            text = '{:^0.38}'.format(str(mac_address_data[ip_mac_count][1]))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
            pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
            interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))

            ip_mac_count += 1
            pos_x_traffic = 47
            pos_y_traffic += 50
    
    text = "Network Devices"
    interface.s_pag_scroll.blit(interface.font_2.render(text, 10, interface.grey), (pos_x_traffic - 15, pos_y_traffic))
    pos_y_traffic += 30
    pygame.draw.line(interface.s_pag_scroll, interface.black, (20, pos_y_traffic), (400, pos_y_traffic), 6)
    
    if (hosts_data != []) and (ips_data != []):
        IPs = hosts_info(hosts_data, ips_data)

        pos_y_traffic += 30
        box_size_x = 40
        box_size_y = 19     
        for i in list(IPs):
            try:
                if (IPs[i]['response'] != 'localhost-response'):
                    pos_x_traffic = 47
                    text = str(i)
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic-1, int((interface.WINDOW_WIDTH)/2)-255, (22)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic-4, int((interface.WINDOW_WIDTH)/2)-255, (22)))
                    pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic-3, int((interface.WINDOW_WIDTH)/2)-257, (20)))
                    interface.s_pag_scroll.blit(interface.font_3.render(text, 10, interface.dark_sand), (pos_x_traffic + 8, pos_y_traffic))
                    
                    pygame.draw.line(interface.s_pag_scroll, interface.black, (pos_x_traffic - 17,pos_y_traffic + 6), (pos_x_traffic + 3, pos_y_traffic + 6), 9)
                    pygame.draw.line(interface.s_pag_scroll, interface.grey_blue2, (pos_x_traffic - 15,pos_y_traffic + 5), (pos_x_traffic + 1, pos_y_traffic + 5), 6)

                    try:
                        pos_x_traffic = 47
                        pos_y_traffic += 18
                        box_size_x = 40
                        text = "MAC"
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
                        interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))
                        pos_x_traffic += box_size_x + 1
                        text = '{:^0.38}'.format(str(IPs[i]['mac']))
                        box_size_x = 115
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
                        interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))
                    except:
                        pass
                    try:
                        pos_x_traffic = 47
                        pos_y_traffic += 19
                        box_size_x = 55
                        text = "Vendor"
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
                        interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))
                        pos_x_traffic += box_size_x + 1
                        text = '{:.37}'.format(str(IPs[i]['vendor']))
                        box_size_x = 225
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
                        interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))
                    except:
                        pass
                    try:
                        pos_x_traffic = 47
                        pos_y_traffic += 20
                        box_size_x = 75
                        text = "Rensponse"
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
                        interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.dark_sand), (pos_x_traffic + 3, pos_y_traffic + 5))
                        pos_x_traffic += box_size_x + 1
                        text = '{:.38}'.format(str(IPs[i]['response']))
                        box_size_x = 150
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-2, pos_y_traffic+3, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.black, (pos_x_traffic-5, pos_y_traffic, box_size_x+2, box_size_y+2))
                        pygame.draw.rect(interface.s_pag_scroll, interface.grey2, (pos_x_traffic-4, pos_y_traffic+1, box_size_x, box_size_y))
                        interface.s_pag_scroll.blit(interface.font_4.render(text, 10, interface.grey), (pos_x_traffic + 3, pos_y_traffic + 5))
                        pos_y_traffic += 35
                    except:
                        pass
            except:
                continue
    else:
        mapping_text = "Mapping Network..."
        interface.s_pag_scroll.blit(interface.font_1.render(mapping_text, 10, interface.dark_sand), (100, pos_y_traffic + 100)) 

    interface.window.blit(interface.s_pag_border, (0, 0))
    interface.window.blit(interface.s_pag_scroll, (5, processes_page_scroll_y))

    return pos_y_process