import pygame
import pygame_menu

class Var:
    pygame.mixer.init()

    # 사운드 관련
    ai_bgm = pygame.mixer.Sound('assets/sounds/ai_sound.wav')
    ai_bgm.set_volume(0.1)

    base_bgm = pygame.mixer.Sound('assets/sounds/base_sound.wav')
    base_bgm.set_volume(0.1)

    block_fall = pygame.mixer.Sound('assets/sounds/block_fall.wav')
    block_fall.set_volume(0.1)

    click = pygame.mixer.Sound('assets/sounds/click.wav')
    click.set_volume(1)

    game_over = pygame.mixer.Sound('assets/sounds/game_over.wav')
    game_over.set_volume(0.05)

    line_clear = pygame.mixer.Sound('assets/sounds/Line_Clear.wav')
    line_clear.set_volume(0.2)

    level_up = pygame.mixer.Sound('assets/sounds/level_up.wav')
    level_up.set_volume(0.2)

    #ai 블럭 모양
    ai_tetris_shapes = [
        [[1, 1, 1],
         [0, 1, 0]],

        [[0, 2, 2],
         [2, 2, 0]],

        [[3, 3, 0],
         [0, 3, 3]],

        [[4, 0, 0],
         [4, 4, 4]],

        [[0, 0, 5],
         [5, 5, 5]],

        [[6, 6, 6, 6]],

        [[7, 7],
         [7, 7]]
    ]

    weights = [3.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093,
               -2.9262681134021786,
               -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861,
               -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956,
               -2.684925769670947,
               -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828,
               0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105,
               -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306,
               17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875]  # 21755 lignes

    keyboard_delay = 200
    keyboard_interval = 150

    display_max_height = 792
    display_min_height = 450


    #            R    G    B
    BLACK = (0, 0, 0)
    RED = (225, 13, 27)
    GREEN = (98, 190, 68)
    BLUE = (64, 111, 249)
    ORANGE = (253, 189, 53)
    YELLOW = (246, 227, 90)
    PINK = (242, 64, 235)
    CYON = (70, 230, 210)
    GRAY = (26, 26, 26)
    DARK_GRAY = (55, 55, 55)
    WHITE = (255, 255, 255)
    MAIN_BLUE = (62, 149, 195)
    MAIN_WHITE = (228, 230, 246)
    MAIN_VIOLET  = (153, 153, 255)
    MAIN_VIOLET_W = (153, 153, 255, 50)
    MAIN_YELLOW = (255, 217, 90)
    w_pink = (231, 59, 109)
    w_sky = (165, 216, 243)
    z_yellow = (252, 215, 2)
    z_green = (185, 205, 12)
    z_blue = (159, 68, 145)
    y_red = (241, 141, 56)
    y_violet = (96, 57, 140)

    T_COLOR = [w_pink, w_sky, z_blue, z_green, z_yellow, y_violet, y_red, DARK_GRAY]
    colors = [BLACK, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, CYON, GRAY]


    x_move_scale = 1
    y_move_scale = 1

    initial_score = 0
    initial_level = 1
    initial_goal = 2
    initial_combo = 0
    initial_page = 0
    initial_mode = 0
    initial_id = 0

    ai_linescores = [0, 20, 25, 30, 35]

    fps = 30

    user_start_speed = 600
    AI_start_speed = int(user_start_speed / 2)
    user_per_speed = 40
    AI_per_speed = int(user_per_speed / 2)





    basic_block_size = 25
    basic_next_block_size_rate = 0.6
    mini_block_size = int(basic_block_size*7/5)

    font_size_small = 14
    font_size_middle = 16
    font_size_big = 18

    block_start_basic_x = 3
    block_start_two_x = 12
    block_start_mini_x = 0
    block_start_y = -2

    combo_score_rate = 10
    level_score_rate = 10
    max_level = 10

    menu_display_w = 600
    menu_display_h = 600

    combo_reset_time=10  # 콤보 초기화 시간 

    # 기본 사이즈 조정
    basic_width = 10  #맵의 좌에서 우로 사이즈
    basic_height = 18 #맵 위에서 아래로 사이즈
    basic_block_size = basic_block_size  #바꾸면 맵 블럭크기 변경
    basic_status_size = 6
    basic_display_width = (basic_width + basic_status_size) * basic_block_size

    mini_width = 5  #맵의 좌에서 우로 사이즈
    mini_height = 15 #맵 위에서 아래로 사이즈
    mini_block_size = mini_block_size  #바꾸면 맵 블럭크  기 변경
    mini_status_size = 5
    mini_display_width = (mini_width + mini_status_size) * mini_block_size

    two_width = 20  # 맵의 좌에서 우로 사이즈
    two_height = 18  # 맵 위에서 아래로 사이즈
    two_block_size = basic_block_size   # 바꾸면 맵 블럭크기 변경
    two_status_size = 8
    two_display_width = (two_width + two_status_size) * two_block_size

    ai_width = 10  # 맵의 좌에서 우로 사이즈
    ai_height = 18  # 맵 위에서 아래로 사이즈
    ai_block_size = basic_block_size   # 바꾸면 맵 블럭크기 변g경
    ai_status_size = 5
    ai_display_width = (ai_width + ai_status_size) * ai_block_size*2



    ## 메뉴 부분
    ## 메뉴 이미지 추가 부분
    menu_image = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/메인메뉴2.PNG',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL	)
    widget_image = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/메인위젯.PNG',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)


    mytheme=pygame_menu.themes.THEME_ORANGE.copy()                  # 메뉴 기본 테마 설정
    mytheme.widget_font_color=(153,153,255)                         # 메뉴 위젯 폰트 컬러
    mytheme.background_color = menu_image                           # 메뉴 배경 설정
    #mytheme.widget_background_color = widget_image                 # 메뉴 위젯 배경 설정
    mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정
    mytheme.widget_alignment=pygame_menu.locals.ALIGN_CENTER        # 메뉴 가운데 정렬 설정
    mytheme.widget_font =pygame_menu.font.FONT_NEVIS                # 메뉴 폰트 설정
    mytheme.widget_margin=(0,40)                                    # 메뉴 위젯 사이 간격 설정


    size=int((menu_display_h)/15)                                      # 기본 폰트 사이즈 변경시
    size2=int((menu_display_h)/20)                                     # 랭크창 폰트 사이즈 변경
    margin=int((menu_display_h)/6)                                     # 위에서 부터 처음 위젯 까지 사이 간격 조정
    margin2=(0,int((menu_display_h)/30))                               # 게임 선택 및 랭크 선택 위젯 사이 간격
    margin3=(0,int((menu_display_h)/15))                               # 위젯 3개 있는 곳 사이 간격
    margin4=(0,int((menu_display_h)/60))                               # 랭크 창 위젯 사이 간격
