import functions, interface, database

import pygame
import time
import threading
import socket
import pickle
import os # Only used for os._exit(0)

def main():
    pygame.display.set_caption("PC Resources Monitor")
    pygame.display.init()
    ### Display ###
    clock = pygame.time.Clock()
    count = 0
    close = False
    files_page_menu_offline = '1'
    files_page_menu_online = '1'
    processes_page_menu = '1'
    processes_page_scroll_y = 5
    hosts_mapped = False
    first_connection = True
    connection_status = ' '
    data_ready = False
    while not close:
        if not hosts_mapped:
            thread_mapping = threading.Thread(target=database.subnetwork_mapping, args=[database.operational_system_data, database.subnetwork])
            thread_mapping.start()
            hosts_mapped = True
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                close = True
                os._exit(0)
            # Keyboard Inputs
            if event.type == pygame.KEYDOWN:    
                if ((event.key == pygame.K_RIGHT) and (interface.menu == 'HOME')) or ((event.key == pygame.K_LEFT) and (interface.menu == 'FILES')):
                    interface.menu = 'CPU'
                elif ((event.key == pygame.K_RIGHT) and (interface.menu == 'CPU')) or ((event.key == pygame.K_LEFT) and (interface.menu == 'PROCESS')):
                    interface.menu = 'FILES'
                elif ((event.key == pygame.K_RIGHT) and (interface.menu == 'FILES')) or ((event.key == pygame.K_LEFT) and (interface.menu == 'HOME')):               
                    interface.menu = 'PROCESS'
                elif ((event.key == pygame.K_RIGHT) and (interface.menu == 'PROCESS')) or ((event.key == pygame.K_LEFT) and (interface.menu == 'CPU')) or ((event.key == pygame.K_SPACE)):
                    interface.menu = 'HOME'
                if ((event.key == pygame.K_TAB) and (interface.connection == 'OFFLINE')):               
                    interface.connection = 'ONLINE'
                elif ((event.key == pygame.K_TAB) and (interface.connection == 'ONLINE')):               
                    interface.connection = 'OFFLINE'
            # Mouse Inputs
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if interface.botton_display_0.collidepoint(((pos[0] - interface.pos_x_s_display), (pos[1] - interface.pos_y_s_display))):
                    interface.menu = 'HOME'
                elif interface.botton_display_1.collidepoint(((pos[0] - interface.pos_x_s_display), (pos[1] - interface.pos_y_s_display))):
                    interface.menu = 'CPU'
                elif interface.botton_display_2.collidepoint(((pos[0] - interface.pos_x_s_display), (pos[1] - interface.pos_y_s_display))):
                    interface.menu = 'FILES'
                elif interface.botton_display_3.collidepoint(((pos[0] - interface.pos_x_s_display), (pos[1] - interface.pos_y_s_display))):
                    interface.menu = 'PROCESS'
                
                if interface.botton_online.collidepoint(((pos[0] - 5), (pos[1] - interface.pos_y_s_display))):
                    interface.connection = 'ONLINE'

                elif interface.botton_offline.collidepoint(((pos[0] - 5), (pos[1] - interface.pos_y_s_display))):
                    interface.connection = 'OFFLINE'
        # Pages Display
        count += 1
        if count == 5:
            if interface.connection == 'OFFLINE':
                if interface.menu == 'HOME':
                    functions.cpu_graph_1(interface.connection, database.cpu_percent_data, database.cpu_max_freq_data)
                    functions.mem_graph(interface.connection, database.mem_data)
                    functions.hd_graph(interface.connection, database.hd_data)
                    functions.pc_cpu_inf(database.pc_name_data, database.operational_system_data, database.os_version_data, database.cpu_data, database.arc_data, database.p_cores_data, database.l_cores_data)
                elif interface.menu == 'CPU':
                    CPU_thrad_1 = threading.Thread(target=functions.cpu_graph_1, args=[interface.connection, database.cpu_percent_data, database.cpu_max_freq_data])
                    CPU_thrad_2 = threading.Thread(target=functions.cpu_graph_2, args=[interface.connection, database.cpu_cores_percent_data])
                    functions.pc_cpu_inf(database.pc_name_data, database.operational_system_data, database.os_version_data, database.cpu_data, database.arc_data, database.p_cores_data, database.l_cores_data)
                    CPU_thrad_1.start()
                    CPU_thrad_2.start()
                    CPU_thrad_1.join()
                    CPU_thrad_2.join()
                elif interface.menu =='FILES':
                    files_data = functions.scan_files(database.local_data)
                    files_pages_data = functions.create_files_pages(files_data)
                    files_pages_count_data = functions.files_pages_count(files_pages_data)
                    functions.files_display(files_pages_data, files_page_menu_offline)
                    functions.files_page_header(database.local_data, files_pages_count_data, files_page_menu_offline)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if interface.next_page_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                            if (int(files_page_menu_offline) + 1) <= functions.files_pages_count(files_pages_data):
                                newpage = int(files_page_menu_offline) + 1
                                files_page_menu_offline = str(newpage)
                        if interface.back_page_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                            if (int(files_page_menu_offline) - 1) > 0:
                                newpage = int(files_page_menu_offline) - 1
                                files_page_menu_offline = str(newpage)
                elif interface.menu == 'PROCESS':
                    end_pos_y = functions.network_and_processes_display(interface.connection, database.hosts_data, database.ips_data, database.processes_data, database.traffic_interface_data, database.ipv4s_data, database.mac_address_data, processes_page_scroll_y, processes_page_menu)
                    functions.network_and_processes_page_header(processes_page_menu)
                    #print("IPV4s -", database.ipv4s_data)
                    #print("MAC -", database.mac_address_data)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if  event.button == 4:
                            processes_page_scroll_y = min(processes_page_scroll_y + 10, 0)
                        if  event.button == 5:
                            processes_page_scroll_y = max(processes_page_scroll_y - 10, -(end_pos_y - 600))
                    if event.type == pygame.KEYDOWN:    
                        if event.key == pygame.K_PAGEUP:
                            processes_page_scroll_y = min(processes_page_scroll_y + 60, 0)
                        elif event.key == pygame.K_PAGEDOWN:
                            processes_page_scroll_y = max(processes_page_scroll_y - 60, -(end_pos_y - 600))
                        elif event.key == pygame.K_HOME:
                            processes_page_scroll_y = 0
                        elif event.key == pygame.K_END:
                            processes_page_scroll_y = -(end_pos_y - 600)                        
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        if interface.pg_end_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                            processes_page_scroll_y = -(end_pos_y - 600)
                        elif interface.pg_top_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                            processes_page_scroll_y = 0
                        elif interface.pg_dowm_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                            processes_page_scroll_y = max(processes_page_scroll_y - 60, -(end_pos_y - 600))
                        elif interface.pg_up_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                            processes_page_scroll_y = min(processes_page_scroll_y + 60, 0)
            
            elif interface.connection == 'ONLINE':
                if first_connection:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        s.connect((socket.gethostname(), 666))
                        print("Connected.")
                        connection_status = 'OK'
                        first_connection = False
                    except Exception as error:
                        print(str(error))
                        connection_status = 'ERROR'
                    interface.connection = functions.connection_check(connection_status)
                else:
                    data_ready = False
                    try:
                        s.send(interface.menu.encode('utf-8'))
                        bytes = s.recv(51200)
                        data = pickle.loads(bytes)
                        data_ready = True
                        connection_status = 'OK'
                    except Exception as error:
                        print(str(error))
                        connection_status = 'ERROR'
                    interface.connection = functions.connection_check(connection_status)
                if data_ready:   
                    if interface.menu == 'HOME':
                        functions.cpu_graph_1(interface.connection, data['cpu_percent'], data['cpu_max_freq'])
                        functions.mem_graph(interface.connection, data['mem'])
                        functions.hd_graph(interface.connection, data['hd'])
                        functions.pc_cpu_inf(data['pc_name'], data['os'], data['os_version'], data['cpu_info'], data['cpu_arc'], data['cpu_pcores'], data['cpu_lcores'])    
                    elif interface.menu == 'CPU':
                        functions.cpu_graph_1(interface.connection, data['cpu_percent'], data['cpu_max_freq'])
                        functions.cpu_graph_2(interface.connection, data['cpu_cores_percent'])
                        functions.pc_cpu_inf(data['pc_name'], data['os'], data['os_version'], data['cpu_info'], data['cpu_arc'], data['cpu_pcores'], data['cpu_lcores'])   
                    elif interface.menu == 'FILES':
                        files_data = data['files']
                        files_pages_data = functions.create_files_pages(files_data)
                        files_pages_count_data = functions.files_pages_count(files_pages_data)
                        functions.files_display(files_pages_data, files_page_menu_online)
                        functions.files_page_header(data['local'], files_pages_count_data, files_page_menu_online)
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if interface.next_page_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                                if (int(files_page_menu_online) + 1) <= functions.files_pages_count(files_pages_data):
                                    newpage = int(files_page_menu_online) + 1
                                    files_page_menu_online = str(newpage)
                            if interface.back_page_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                                if (int(files_page_menu_online) - 1) > 0:
                                    newpage = int(files_page_menu_online) - 1
                                    files_page_menu_online = str(newpage)
                    elif interface.menu == 'PROCESS':
                        end_pos_y = functions.network_and_processes_display(interface.connection, data['hosts'], data['ips'], data['processes'], data['traffic_interface'], data['ipv4s'], data['mac_address'], processes_page_scroll_y, processes_page_menu)
                        functions.network_and_processes_page_header(processes_page_menu)
                        if event.type == pygame.MOUSEBUTTONUP:
                            if  event.button == 4:
                                processes_page_scroll_y = min(processes_page_scroll_y + 10, 0)
                            if  event.button == 5:
                                processes_page_scroll_y = max(processes_page_scroll_y - 10, -(end_pos_y - 600))
                        if event.type == pygame.KEYDOWN:    
                            if event.key == pygame.K_PAGEUP:
                                processes_page_scroll_y = min(processes_page_scroll_y + 60, 0)
                            elif event.key == pygame.K_PAGEDOWN:
                                processes_page_scroll_y = max(processes_page_scroll_y - 60, -(end_pos_y - 600))
                            elif event.key == pygame.K_HOME:
                                processes_page_scroll_y = 0
                            elif event.key == pygame.K_END:
                                processes_page_scroll_y = -(end_pos_y - 600)                        
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if interface.pg_end_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                                processes_page_scroll_y = -(end_pos_y - 600)
                            elif interface.pg_top_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                                processes_page_scroll_y = 0
                            elif interface.pg_dowm_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                                processes_page_scroll_y = max(processes_page_scroll_y - 60, -(end_pos_y - 600))
                            elif interface.pg_up_buttom.collidepoint(((pos[0] - interface.pos_x_s_header), (pos[1] - interface.pos_y_s_header))):
                                processes_page_scroll_y = min(processes_page_scroll_y + 60, 0)
            interface.menu_buttons(interface.menu, interface.connection)    
            count = 0
        pygame.display.update()
        clock.tick(60)
    pygame.display.quit()
if __name__ == "__main__":
    main()