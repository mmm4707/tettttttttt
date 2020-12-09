import pygame
import pygame_menu
import random
import os
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
    O = (((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 1, 1, 0), (0, 0, 1, 1, 0), (0, 0, 0, 0, 0)),) * 4

    I = (((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 2, 2, 2, 2), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (2, 2, 2, 2, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 0, 0, 0)))

    L = (((0, 0, 0, 0, 0), (0, 0, 3, 0, 0), (0, 0, 3, 0, 0), (0, 0, 3, 3, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 3, 3, 3, 0), (0, 3, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 3, 3, 0, 0), (0, 0, 3, 0, 0), (0, 0, 3, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 3, 0), (0, 3, 3, 3, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    J = (((0, 0, 0, 0, 0), (0, 0, 4, 0, 0), (0, 0, 4, 0, 0), (0, 4, 4, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 4, 0, 0, 0), (0, 4, 4, 4, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 4, 4, 0), (0, 0, 4, 0, 0), (0, 0, 4, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 4, 4, 4, 0), (0, 0, 0, 4, 0), (0, 0, 0, 0, 0)))

    Z = (((0, 0, 0, 0, 0), (0, 0, 0, 5, 0), (0, 0, 5, 5, 0), (0, 0, 5, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 5, 5, 0, 0), (0, 0, 5, 5, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 5, 0, 0), (0, 5, 5, 0, 0), (0, 5, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 5, 5, 0, 0), (0, 0, 5, 5, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    S = (((0, 0, 0, 0, 0), (0, 0, 6, 0, 0), (0, 0, 6, 6, 0), (0, 0, 0, 6, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 6, 6, 0), (0, 6, 6, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 6, 0, 0, 0), (0, 6, 6, 0, 0), (0, 0, 6, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 6, 6, 0), (0, 6, 6, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    T = (((0, 0, 0, 0, 0), (0, 0, 7, 0, 0), (0, 0, 7, 7, 0), (0, 0, 7, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 7, 7, 7, 0), (0, 0, 7, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 7, 0, 0), (0, 7, 7, 0, 0), (0, 0, 7, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 7, 0, 0), (0, 7, 7, 7, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))


    weights = [3.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093,
               -2.9262681134021786,
               -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861,
               -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956,
               -2.684925769670947,
               -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828,
               0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105,
               -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306,
               17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875]  # 21755 lignes

    error_type = {'no_error': 0, 'right_wall': 1, 'left_wall': 2, 'bottom': 3, 'overlap': 4} # 충돌 에러 판단용
    shapes_rotation = {4: 4, 8: 2, 12: 2, 16: 4, 20: 4, 24: 2, 28: 1} #ai 블럭 회전 판단용



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


    T_COLOR = [w_pink, w_sky, z_blue, z_green, MAIN_VIOLET, y_violet, y_red]
    colors = [BLACK, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, CYON, GRAY]

    #keyboard_delay = 200
    #keyboard_interval = 150

    infoObject = () #디스플레이 사이즈 받는 용

    display_max_height = 792
    display_min_height = 450
    bar_size = 25

    x_move_scale = 1  # 블럭의 x축 이동 수
    y_move_scale = 1  # 블럭의 y축 이동 수
    collide_move_rate =2 #벽과 충돌하는 경우 움직이는 배수
    x_move_scale_zero = 0  # 블럭의 x축 이동 x
    y_move_scale_zero = 0 # 블럭의 y축 이동 x

    board_start_x = 0      # 보드의 시작점 x좌표
    board_start_y = 0      # 보드의 시작점 y좌표
    board_die_line=1      # 보드에서 다으면 죽는 라인 즉 맨 윗줄
    board_line_start = 1  # 보드 지울때 첫 줄
    delete_line=1         # 보드 지울때 한칸씩 지우기

    board_die_num=0    # 맨 위에서 보드가 몇개 이상이면 죽을 것인지
    line_size=1      # 그림자나 블록 라인 사이즈
    ai_matrix_line_size = 0 #ai  매트릭스를 만들때 라인 사이즈 
    ai_line_size = 2 # ai에서 board를 나누는 선의 두꼐 

    fps = 30  # 게임의 fps
    initial_score = 0   # 시작 점수
    initial_level = 1   # 시작 레벨
    count_level = 1     #레벨 증가률
    goal_zero_state = 0  # 골수가 0이 된 상태
    level_goal_per = 3   #레벨당 목표 goal수
    initial_combo = 0    # 시작 콤보 및 초기화
    count_combo = 1   #콤보 증가량
    count_goal = 1    #골수 증갈야
    initial_block_state= 0  #처음 블럭의 회전 상태
    ai_score_weight = 2     #ai점수 가중치
    board_empty_state = 0 #보드 처음 상태

    rotate_start = 0      #회전 인덱스 시작값
    rotate_cycle = 4      #회전 사이클
    next_block_shape = 1  #다음 회전한 모양 블럭 기준
    block_start_index = 0 #블럭 인덱스 시작점

    # 현재 블럭의 x축 기준 길이
    def piece_length(piece):
        return piece[0]

    initial_page = 'page0'
    initial_mode = 0  # 모드 초기값
    initial_id = 0  # id 초기값

    ai_event = pygame.USEREVENT + 1
    ai_diplay_width_rate = 2
    ai_random_seed = 6  # ai랜덤 시드값
    ai_stone_start_x_rate = 1 / 2  # x축 기준 새로운 블럭 시작 위치 비율
    ai_stone_start_y = 0  # 블록의 y좌표 시작점
    ai_blockdown_score_per = 0  # 블록을 내릴때 마다 추가되는 점수
    ai_no_blockdown_score_per = 0  # 블럭을 내리지 못하는 경우의 추가 점수
    ai_block_choice_start = 0  # ai블럭을 선택하기 위한 시작 인덱스
    ai_block_choice_end = len(ai_tetris_shapes) - 1  # ai블럭을 선택하기 위한 끝  인덱스
    ai_initial_completLine = 0  # ai 지운 라인수 초기값
    ai_count_completLine = 1  # 지운 라인수 증가율
    ai_initial_numberOfHoles = 0  # 구멍의 개수 초기값
    ai_count_numberOfHoles = 1  # 구멍 개수 증가율
    ai_initial_bestscore = -10000  # 베스트 스코어 초기값
    ai_best_fix_level = 2  # ai best용 고정 레벨값
    ai_choice_fix_level = 1  # ai choice용 고정 레벨값
    ai_working_piece_index = 0  # 현재 내려오는 블럭의 인덱스값
    ai_line_reset = 0  # 한번에 지운 라인 개수 초기
    ai_lineclear_per = 1  # 한줄 지울때마다 올라가는 한번에 지운 개수
    ai_linescores = [0, 10, 15, 20, 25]  # 한번에 제거하는 줄의 개수에 따른 점수
    ai_draw_space = 1  # 그림, 선이 잘 보이도록 여유 공간 빼주기
    for_index_var = 1  # 인덱스값을 맞추기 위한 변수
    search_rotate_next_index = -1  # 다음 인덴스를 찾아가기 (뒤에서 부터)
    last_rotate_index_prev = -1  # 마지막 인덴스의 다음 인덱스(여기 전까지 진행)
    field_up_line = 0  # 필드의 맨 윗줄
    ai_display_middle_rate = 0.5
    ai_text_loc_x = 0.15  # ai상태 창에서 글씨가 시간하는 부분의 비율 (상태창길이)
    ai_score_text_loc = 9  # 디스플에의 높이 기준, 몇번째 블럭에 해당되는 곳의 옆에 있는가 
    ai_score_loc = 10
    ai_said1_loc = 1
    ai_said2_loc = 2
 
    user_start_speed = 600  #유저의 시작 스피드(몇초에 한번 이벤트가 진행되는가)
    AI_start_speed = int(user_start_speed / 2)   #ai의 시작 스피드
    user_per_speed = 40   #레벨에 따른 유저의 속도 증가
    AI_per_speed = int(user_per_speed / 2)  #레벨에 따른 ai의 속도 증가

    combo_max=9
    combo_reset=0

    basic_block_size = 25   #미니 모드 제외 나머지의 블록 사이즈
    basic_next_block_size_rate = 0.6  #화면에 표시되는 다음 블럭의 사이즈 비율
    mini_block_size = int(basic_block_size*7/5)  #미니 모드의 블럭 사이즈

    basic_block_size = 25   #미니 모드 제외 나머지의 블록 사이즈
    basic_next_block_size_rate = 0.6  #화면에 표시되는 다음 블럭의 사이즈 비율
    mini_block_size = int(basic_block_size*7/5)  #미니 모드의 블럭 사이즈
    min_mini_block_size = int(basic_block_size*6/5) #미니 모드의 최소 블럭사이즈

    two_board_two = 2 #보드 크기가 두 배인 모드에 곱하는 용
    center_divide = 2 # center 위치를 지정하기 위해 나누는 용
    board_text_divide = 7 #board text 위치 조정을 위함
    rect2_margin = 0.5 # 두번째 board칸 네모를 위한 margin
    rect2_margin_double = rect2_margin*2 #margin 두 배
    next_block_margin = 0.2 #next 블럭 보여줄 위치에 margin 추가
    next_block_margin_y = 1.5 #next 블럭 y좌표를 위한 비율
    next_block_size = 0.5 #next 블럭 사이즈 조절을 위한 비율
    next_block2_margin = 0.45 # 두번째 next 블럭 위치 조절 비율

    next_loc = 0.05
    score_loc = 0.3
    score_val_loc = 0.35
    level_loc = 0.45
    level_val_loc = 0.5
    goal_loc = 0.6
    goal_val_loc = 0.65
    combo_loc = 0.75
    combo_val_loc = 0.8
    time_loc = 0.92

    font_size_small = 14    #폰트 사이즈 작은거
    font_size_middle = 16   #중간
    font_size_big = 18      #큰거
    font_resize = 1
    font_size_double = 2 #fontsize 두 배

    block_start_basic_x = 3  #몇번 쨰 칸에서 블럭이 시작 하는가
    block_start_two_x = 12
    block_start_mini_x = 0
    block_start_y = -2

    combo_score_rate = 10  #콤보에 따른 점수 가중치
    level_score_rate = 10  # 레벨에 따른 점수 가중치
    max_level = 10         #최대 레벨

    menu_display_w = 600  # 메뉴 시작시 처음 가로 크기
    menu_display_h = 600  # 메뉴 시작시 처음 세로 크기

    myscore_display=(160,270)
    myscore_font=50
    combo_reset_time=10  # 콤보 초기화 시간

    # 기본 사이즈 조정
    basic_width = 10  #맵의 좌에서 우로 사이즈
    basic_height = 18 #맵 위에서 아래로 사이즈
    basic_block_size = basic_block_size  #바꾸면 맵 블럭크기 변경
    basic_status_size = 6   #상태 바 사이즈 (블럭의 개수 기준으로 )
    basic_display_width = (basic_width + basic_status_size) * basic_block_size

    mini_width = 5  #맵의 좌에서 우로 사이즈
    mini_height = 15 #맵 위에서 아래로 사이즈
    mini_block_size = mini_block_size  #바꾸면 맵 블럭크  기 변경
    mini_status_size = 5  #상태 바 사이즈 (블럭의 개수 기준으로 )
    mini_display_width = (mini_width + mini_status_size) * mini_block_size

    two_width = 20  # 맵의 좌에서 우로 사이즈
    two_height = 18  # 맵 위에서 아래로 사이즈
    two_block_size = basic_block_size   # 바꾸면 맵 블럭크기 변경
    two_status_size = 8  #상태 바 사이즈 (블럭의 개수 기준으로 )
    two_display_width = (two_width + two_status_size) * two_block_size

    ai_width = 10  # 맵의 좌에서 우로 사이즈
    ai_height = 18  # 맵 위에서 아래로 사이즈
    ai_block_size = basic_block_size   # 바꾸면 맵 블럭크기 변g경
    ai_status_size = 5  #상태 바 사이즈 (블럭의 개수 기준으로 )
    ai_display_width = (ai_width + ai_status_size) * ai_block_size*2


    current_w = 1855
    resize_cut_up = 1.001
    resize_cut_down = 1.0
    start_status_bar_y = 0 #상태표시 바 시작 y 좌표
    resize_basic = 1 # 리사이징 관련 고정 변수 

######################메뉴 관련 #########################
##########################################################################################
    ## 메뉴 부분
    ## 메뉴 이미지 추가 부분
    menu_image = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/메인메뉴2.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL	)
    widget_image = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/메인위젯.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
    widget_image2 = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/위젯3.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
    PATH=os.path.join('assets/images/메인메뉴2.png')


    #메뉴 기본 테마 만들기

    mytheme=pygame_menu.themes.THEME_ORANGE.copy()                  # 메뉴 기본 테마 설정
    mytheme.widget_font_color=MAIN_VIOLET                         # 메뉴 위젯 폰트 컬러
    mytheme.background_color = menu_image                           # 메뉴 배경 설정
    #mytheme.widget_background_color = widget_image                 # 메뉴 위젯 배경 설정
    mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정
    mytheme.widget_alignment=pygame_menu.locals.ALIGN_CENTER        # 메뉴 가운데 정렬 설정
    mytheme.widget_font =pygame_menu.font.FONT_NEVIS                # 메뉴 폰트 설정
    mytheme.widget_margin=(0,40)

    #HELP 메뉴 만들
    mytheme_help = pygame_menu.themes.THEME_ORANGE.copy()  # 메뉴 기본 테마 설정
    mytheme_help.background_color = widget_image2  # 메뉴 배경 설정
    mytheme_help.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정



    rank_id_max=3           #랭크 ID 최대 이름 수
    rank_max=5              # 랭크 보여주는 창 최대 갯수 -1
    min_display_w =400      # 메뉴 최소 사이즈 가로
    min_display_h =400      # 메뉴 최소 사이즈 세로
    widget_center = 0
    sleep_time = 0.3
    initial_page = 'page0'  # 메뉴 시작 페이지

    # 리사이징 시 변하는 비율
    font_rate_main = 15
    font_rate_sub = 20
    widget_rate_main = 15
    widget_rate_showpage = 30
    widget_rate_rank = 60
    rate_main=6
    rate_show=40
    rate_rank=30
    rate_help=1.25

    #폰트 사이즈
    font_main = int((menu_display_h) / font_rate_main)   # 메뉴 기본 폰트 사이즈
    font_sub = int((menu_display_h) / font_rate_sub)     # 메뉴 서브 폰트 사이즈

    # 위젯 사이 간격
    widget_margin_main = (0,int((menu_display_h)/widget_rate_main))         #  메인 화면
    widget_margin_showpage=(0,int((menu_display_h)/widget_rate_showpage))   #게임 선택 랭킹 선택
    widget_margin_rank=(0,int((menu_display_h)/widget_rate_rank))           # 랭크 보기 화면

    #마진 시작 가로 세로  좌표
    margin_main = int((menu_display_h)/rate_main)   # 메인 화면
    margin_show = int((menu_display_h)/rate_show)   #SHOW 화면
    margin_rank =int((menu_display_h)/rate_rank)    #RANK 화면
    margin_help=int((menu_display_h)/rate_help)     #HELP 화면

