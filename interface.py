import pygame

### Functions ###
def menu_buttons(menu, connection):
    s_menu_bottom_border.fill(black)
    s_menu_bottom.fill(background)    
    s_display.fill(background)
    
    pos_zero_x = 125
    pos_x = pos_zero_x
    pos_y = ((int(MENU_BOTTOM_BORDER_HEIGHT / 3) + 2) + 13)
    button_size_pressed = 8
    button_size_nonpressed = 10

    #botton HOME
    pygame.draw.circle(s_display, black, (pos_x, pos_y), (button_size_nonpressed + 3))
    botton_display_0 = pygame.draw.circle(s_display, dark_sand, (pos_x, pos_y), button_size_nonpressed)
    #botton CPU
    pos_x += 50
    pygame.draw.circle(s_display, black, (pos_x, pos_y), (button_size_nonpressed + 3))
    botton_display_1 = pygame.draw.circle(s_display, dark_sand, (pos_x, pos_y), button_size_nonpressed)
    #botton FILES
    pos_x += 50
    pygame.draw.circle(s_display, black, (pos_x, pos_y), (button_size_nonpressed + 3))
    botton_display_2 = pygame.draw.circle(s_display, dark_sand, (pos_x, pos_y), button_size_nonpressed)
    #botton PROCESS
    pos_x += 50
    pygame.draw.circle(s_display, black, (pos_x, pos_y), (button_size_nonpressed + 3))
    botton_display_3 = pygame.draw.circle(s_display, dark_sand, (pos_x, pos_y), button_size_nonpressed)
    
    pos_x = pos_zero_x
    if menu == 'HOME':
        pygame.draw.circle(s_display, black, (pos_x,pos_y), (button_size_pressed + 3))
        botton_display_0 = pygame.draw.circle(s_display, grey1, (pos_x,pos_y), button_size_pressed)
    elif menu == 'CPU':
        pygame.draw.circle(s_display, black, ((pos_x + 50),pos_y), (button_size_pressed + 3))
        botton_display_1 = pygame.draw.circle(s_display, grey1, ((pos_x + 50),pos_y), button_size_pressed)
    elif menu =='FILES':
        pygame.draw.circle(s_display, black, ((pos_x + 100),pos_y), (button_size_pressed + 3))
        botton_display_2 = pygame.draw.circle(s_display, grey1, ((pos_x + 100),pos_y), button_size_pressed)
    elif menu == 'PROCESS':
        pygame.draw.circle(s_display, black, ((pos_x + 150),pos_y), (button_size_pressed + 3))
        botton_display_3 = pygame.draw.circle(s_display, grey1, ((pos_x + 150),pos_y), button_size_pressed)
    
    switch_button(connection)

    page_name = font_4.render("Home", 10, dark_sand)
    s_display.blit(page_name, (110, 13))
    page_name = font_4.render("CPU", 10, dark_sand)
    s_display.blit(page_name, (163, 13))
    page_name = font_4.render("Files", 10, dark_sand)
    s_display.blit(page_name, (212, 13))
    page_name = font_4.render("Network", 10, dark_sand)
    s_display.blit(page_name, (255, 13))
    version = font_4.render("Version: 7.0.0", 10, dark_sand)
    s_menu_bottom.blit(version, (710, 20))
    ass = font_4.render("Dev.: Fábio R. P. Nunes", 10, dark_sand)
    s_menu_bottom.blit(ass, (660, 45))
    window.blit(s_menu_bottom_border, (0, WINDOW_HEIGHT))
    window.blit(s_menu_bottom, (5, (WINDOW_HEIGHT + 5)))
    window.blit(s_display, (pos_x_s_display, pos_y_s_display))

    return botton_display_0, botton_display_1, botton_display_2, botton_display_3

def switch_button(connection):  
    pos_zero_x = 50
    pos_x = pos_zero_x
    pos_y = ((int(MENU_BOTTOM_BORDER_HEIGHT / 3) + 2) + 13)
    button_size_pressed = 8
    button_size_nonpressed = 10

    pygame.draw.line(s_menu_bottom, black, (pos_x,pos_y), (pos_x+25, pos_y), 20)

    #botton ONLINE
    pygame.draw.circle(s_menu_bottom, black, (pos_x, pos_y), (button_size_nonpressed + 3))
    botton_online = pygame.draw.circle(s_menu_bottom, dark_sand, (pos_x, pos_y), button_size_nonpressed)
    #botton OFFLINE
    pos_x += 25
    pygame.draw.circle(s_menu_bottom, black, (pos_x, pos_y), (button_size_nonpressed + 3))
    botton_offline = pygame.draw.circle(s_menu_bottom, dark_sand, (pos_x, pos_y), button_size_nonpressed)
    
    pos_x = pos_zero_x
    if connection == 'ONLINE':
        pygame.draw.circle(s_menu_bottom, black, (pos_x,pos_y), (button_size_pressed + 3))
        botton_online = pygame.draw.circle(s_menu_bottom, grey_blue2, (pos_x,pos_y), button_size_pressed)
        status_txt = font_4.render("Online", 10, grey_blue1)
        s_menu_bottom.blit(status_txt, (60, 9))
    elif connection == 'OFFLINE':
        pygame.draw.circle(s_menu_bottom, black, ((pos_x + 25),pos_y), (button_size_pressed + 3))
        botton_offline = pygame.draw.circle(s_menu_bottom, red, ((pos_x + 25),pos_y), button_size_pressed)
        status_txt = font_4.render("Offline", 10, red2)
        s_menu_bottom.blit(status_txt, (60, 9))
    
    mode_txt = font_4.render("Mode", 10, grey)
    s_menu_bottom.blit(mode_txt, (25, 9))

    return botton_online, botton_offline

def display_next_page_buttom():
    text_button = "Next"
    buttom = pygame.draw.circle(s_header, background, ((WINDOW_WIDTH-50),40), 20)
    pygame.draw.polygon(s_header, black, ((WINDOW_WIDTH-35,45),(WINDOW_WIDTH-55,35),(WINDOW_WIDTH-55,55)))
    pygame.draw.polygon(s_header, dark_sand, ((WINDOW_WIDTH-40,40),(WINDOW_WIDTH-60,30),(WINDOW_WIDTH-60,50)))
    s_header.blit(font_3.render(text_button, 10, dark_sand), ((WINDOW_WIDTH-70), 10))
    return buttom

def display_back_page_buttom():
    text_button = "Back"
    buttom = pygame.draw.circle(s_header, background, ((WINDOW_WIDTH-100),40), 20)
    pygame.draw.polygon(s_header, black, ((WINDOW_WIDTH-110,45),(WINDOW_WIDTH-90,35),(WINDOW_WIDTH-90,55)))
    pygame.draw.polygon(s_header, dark_sand, ((WINDOW_WIDTH-115,40),(WINDOW_WIDTH-95,30),(WINDOW_WIDTH-95,50)))
    s_header.blit(font_3.render(text_button, 10, dark_sand), ((WINDOW_WIDTH-120), 10))
    return buttom

def display_pg_end_buttom():
    text_button = "End"
    buttom = pygame.draw.circle(s_header, background, ((WINDOW_WIDTH-50),40), 20)
    pygame.draw.polygon(s_header, black, ((WINDOW_WIDTH-35,35),(WINDOW_WIDTH-55,35),(WINDOW_WIDTH-45,55)))
    pygame.draw.polygon(s_header, dark_sand, ((WINDOW_WIDTH-40,30),(WINDOW_WIDTH-60,30),(WINDOW_WIDTH-50,50)))
    pygame.draw.line(s_header, black, (WINDOW_WIDTH-55,55), (WINDOW_WIDTH-35, 55), 3)
    pygame.draw.line(s_header, dark_sand, (WINDOW_WIDTH-60,50), (WINDOW_WIDTH-40, 50), 3)
    s_header.blit(font_3.render(text_button, 10, dark_sand), ((WINDOW_WIDTH-61), 10))
    return buttom

def display_pg_dowm_buttom():
    text_button = "Down"
    buttom = pygame.draw.circle(s_header, background, ((WINDOW_WIDTH-90),40), 20)
    pygame.draw.polygon(s_header, black, ((WINDOW_WIDTH-75,35),(WINDOW_WIDTH-95,35),(WINDOW_WIDTH-85,55)))
    pygame.draw.polygon(s_header, dark_sand, ((WINDOW_WIDTH-80,30),(WINDOW_WIDTH-100,30),(WINDOW_WIDTH-90,50)))
    s_header.blit(font_3.render(text_button, 10, dark_sand), ((WINDOW_WIDTH-107), 10))
    return buttom

def display_pg_up_buttom():
    text_button = "Up"
    buttom = pygame.draw.circle(s_header, background, ((WINDOW_WIDTH-130),40), 20)
    pygame.draw.polygon(s_header, black, ((WINDOW_WIDTH-115,55),(WINDOW_WIDTH-135,55),(WINDOW_WIDTH-125,35)))
    pygame.draw.polygon(s_header, dark_sand, ((WINDOW_WIDTH-120,50),(WINDOW_WIDTH-140,50),(WINDOW_WIDTH-130,30)))
    s_header.blit(font_3.render(text_button, 10, dark_sand), ((WINDOW_WIDTH-138), 10))
    return buttom

def display_pg_top_buttom():
    text_button = "Top"
    buttom = pygame.draw.circle(s_header, background, ((WINDOW_WIDTH-170),40), 20)
    pygame.draw.line(s_header, black, (WINDOW_WIDTH-175,35), (WINDOW_WIDTH-155, 35), 3)
    pygame.draw.polygon(s_header, black, ((WINDOW_WIDTH-155,55),(WINDOW_WIDTH-175,55),(WINDOW_WIDTH-165,35)))
    pygame.draw.polygon(s_header, dark_sand, ((WINDOW_WIDTH-160,50),(WINDOW_WIDTH-180,50),(WINDOW_WIDTH-170,30)))
    pygame.draw.line(s_header, dark_sand, (WINDOW_WIDTH-180,30), (WINDOW_WIDTH-160, 30), 3)
    s_header.blit(font_3.render(text_button, 10, dark_sand), ((WINDOW_WIDTH-180), 10))
    return buttom

### Windows Config. ###
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MENU_BOTTOM_BORDER_WIDTH = WINDOW_WIDTH
MENU_BOTTOM_BORDER_HEIGHT = 70
MENU_BOTTOM_WIDTH = (MENU_BOTTOM_BORDER_WIDTH - 10)
MENU_BOTTOM_HEIGHT = (MENU_BOTTOM_BORDER_HEIGHT - 10)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + MENU_BOTTOM_BORDER_HEIGHT))

### Surfaces ###
s_menu_bottom = pygame.surface.Surface((MENU_BOTTOM_WIDTH, MENU_BOTTOM_HEIGHT))
s_menu_bottom_border = pygame.surface.Surface((MENU_BOTTOM_BORDER_WIDTH, MENU_BOTTOM_BORDER_HEIGHT))
s_display = pygame.surface.Surface((int(MENU_BOTTOM_WIDTH / 2), MENU_BOTTOM_HEIGHT))
s = pygame.surface.Surface((WINDOW_WIDTH, int((WINDOW_HEIGHT)/4)))
s_header = pygame.surface.Surface((WINDOW_WIDTH-10, 65))
s_pag = pygame.surface.Surface((WINDOW_WIDTH-10, WINDOW_HEIGHT-5))
s_pag_scroll = pygame.surface.Surface((WINDOW_WIDTH-10, 50000))
s_pag_border = pygame.surface.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
s_info = pygame.surface.Surface(((WINDOW_WIDTH - 10), int((WINDOW_HEIGHT)/4) - 5))
s_cpu = pygame.surface.Surface((WINDOW_WIDTH, int(((WINDOW_HEIGHT)/4)*2)))

### Colors ###
red = (150,0,0)
red2 = (200,0,0)
green = (255,0,0)
blue = (0,0,255)
light_blue = (0,200,255)
black = (0,0,0)
white = (255, 255, 255)
grey = (150, 150, 150)
grey1 = (80, 80, 80)
grey2 = (45, 45, 45)
grey2 = (55, 55, 55)
grey_blue1 = (156, 181, 201)
grey_blue2 = (0, 55, 130)
dark_blue = (0, 0, 50)
sand = (255, 230, 185)
sand2 = (225, 190, 145)
dark_sand = (165, 145, 110)
background = (45, 45, 45)

### Fonts ###
pygame.font.init()
font_1 = pygame.font.SysFont('', 36)
font_2 = pygame.font.SysFont('', 24)
font_3 = pygame.font.SysFont('', 20)
font_4 = pygame.font.SysFont('', 16)

### Menu Settings ###
connection = 'OFFLINE'
menu = 'HOME'
pos_x_s_display = 200
pos_y_s_display = WINDOW_HEIGHT + 5
pos_x_s_header = 5
pos_y_s_header = 0
# Buttons
botton_display_0 = menu_buttons(menu, connection)[0]
botton_display_1 = menu_buttons(menu, connection)[1]
botton_display_2 = menu_buttons(menu, connection)[2]
botton_display_3 = menu_buttons(menu, connection)[3]

botton_online = switch_button(connection)[0]
botton_offline = switch_button(connection)[1]

next_page_buttom = display_next_page_buttom()
back_page_buttom = display_back_page_buttom()
pg_dowm_buttom = display_pg_dowm_buttom()
pg_up_buttom = display_pg_up_buttom()
pg_end_buttom = display_pg_end_buttom()
pg_top_buttom = display_pg_top_buttom()