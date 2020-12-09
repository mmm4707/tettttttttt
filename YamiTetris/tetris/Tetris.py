import pygame, sys, time
from pygame.locals import *
from Board import *
import random
from ai import Ai
from variable import Var

class Tetris:

    #생성자
    def __init__(self):
        self.mode = 'basic'
        self.clock = pygame.time.Clock()
        self.music_on_off = True
        self.check_reset = True
        self.Score = Var.initial_score
        self.game=False

        random.seed(Var.ai_random_seed)
        self.max_height = Var.display_max_height
        self.min_height = Var.display_min_height
        font_resize = Var.font_resize


    #각 키를 누를떄 실행되는 method
    def handle_key(self, event_key, mode):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece(mode)
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-Var.x_move_scale, dy=Var.y_move_scale_zero)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=Var.x_move_scale, dy=Var.y_move_scale_zero)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece(mode)
        elif event_key == K_m: # 소리 설정
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                if self.mode == 'ai':
                    Var.ai_bgm.play()
                else:
                    Var.base_bgm.play()
            else:
                Var.base_bgm.stop()
                Var.ai_bgm.stop()


    def ai_new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = Var.ai_tetris_shapes[random.randint(Var.ai_block_choice_start, Var.ai_block_choice_end) ]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.stone_x = int((self.board.width  - len(Var.piece_length(self.stone)))*Var.ai_stone_start_x_rate) # self.width 기준 스톤의 위치 x
        self.stone_y = Var.ai_stone_start_y
        if self.board.ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True  # 블럭이 부딪히는 판단, 새점로 생성한 블럭이 벽에 부딪히면은 게임 종료


    def ai_init_game(self):
        self.ai_board = [[Var.board_empty_state for x in range(self.board.width)] for y in range(self.board.height)] # 새로운 게임 보드 생성
        self.ai_new_stone()  # 새로운 블럭 생성
        self.ai_score = Var.initial_score  # 시작 스코어
        self.ai_lines = Var.ai_line_reset  # 지운 라인의 개수


    def ai_add_cl_lines(self, n):
        self.ai_lines += n  # 지운 개수 추가하기
        self.ai_score += Var.ai_linescores[n] * self.board.level * Var.ai_score_weight  # 점수  = 원래 점수 + 한번에지운 라인개수에 해당하는 점수 * 레벨

    def ai_move(self, delta_x):
        if not self.gameover and not self.paused:  # 게임 종료, 정지 상태가 아니라면
            new_x = self.stone_x + delta_x  # 새로운 x 좌표는   기존의 stone의 x좌표 + 이동좌표수
            if new_x < Var.board_start_x:  # 새로운 좌표가 0보다 작다면
                new_x = Var.board_start_x  # 새로운 좌표는 0 ( 변경 없음 )
            if new_x > self.board.width - len(Var.piece_length(self.stone)):  # 새로운 좌표 > 열의개수(10) - 블럭의 x축 길이
                new_x = self.board.width - len(Var.piece_length(self.stone))  # 이동 불가 (변경 없음)
            if not self.board.ai_check_collision(self.ai_board, self.stone, (new_x, self.stone_y)):  # 벽과 부딪히지 않는 다면
                self.stone_x = new_x  # 새로운 좌표로 이동

    def ai_drop(self, manual):
        if not self.gameover and not self.paused:  # 게임 종료, 정지 상ef태가 아니라면
            self.ai_score += Var.ai_blockdown_score_per if manual else Var.ai_no_blockdown_score_per  # 내릴 수 있다면  스코어+1, 내릴수 없다면 +0
            self.stone_y += Var.y_move_scale  # y축 좌표 +1
            if self.board.ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):  # 벽에 부딪히지 않는 경우에는
                self.ai_board = self.board.join_matrixes(self.ai_board, self.stone,
                                           (self.stone_x, self.stone_y))  # 새로운 보드는   블럭의 새로운 좌표를 포합한 보드로 갱신
                self.ai_score += Var.ai_blockdown_score_per # 블럭이 밑에 내려가면 점수 추가
                self.ai_new_stone()  # 새로운 블럭 생성하기
                cleared_rows = Var.ai_line_reset  # 지운 행의 개수 초기화

                for i, row in enumerate(self.ai_board):  # 모든 행마다 검사    i는 행의 번호
                    if Var.board_empty_state not in row:  # 행에 빈공간이 없다면 (0은 빈공간의 의미한다.)
                        self.ai_board = self.board.ai_remove_row(self.ai_board, i)  # ai보드를 i행을 지운 보드로 업데이트
                        cleared_rows += Var.ai_lineclear_per  # 지운개수 +1  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                self.ai_add_cl_lines(cleared_rows)  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                return True  # 게임 종료 상태가 아니 었다면,  true 반환
        return False  # 게임이 정지, 종료 상태 였다면 false 반환

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            ai_new_stone = self.board.ai_rotate_clockwise(self.stone)
            if not self.board.ai_check_collision(self.ai_board,
                                   ai_new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = ai_new_stone

    def ai_start_game(self):
        if self.gameover:  # 게임이 종료된 상태라면
            self.ai_init_game()  # 초기화 진행하기
            self.gameover = False  # 게임 종료는 false로 바꿔주기

    def ai_executes_moves(self, ai_moves):
        ai_key_actions = {
            'LEFT': lambda: self.ai_move(-Var.x_move_scale),
            'RIGHT': lambda: self.ai_move(+Var.x_move_scale),
            'DOWN': lambda: self.ai_drop(True),
            'UP': self.rotate_stone,
            'SPACE': self.ai_start_game
        }
        # 받아온 moves에 저장되어 있는 동작 수행하기  -- (ai에서 학습된 것을 통해 결정 되는 부분)
        for ai_action in ai_moves:
            ai_key_actions[ai_action]()

    def handle_key2(self, event_key, mode):
        if event_key == K_s:
            self.board.drop_piece(mode)
        elif event_key == K_a:
            self.board.move_piece(dx=-Var.x_move_scale, dy=Var.y_move_scale_zero)
        elif event_key == K_d:
            self.board.move_piece(dx=Var.x_move_scale, dy=Var.y_move_scale_zero)
        elif event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_e:
            self.board.full_drop_piece(mode)
        if event_key == K_DOWN:
            self.board.drop_piece2()
        elif event_key == K_LEFT:
            self.board.move_piece2(dx=-Var.x_move_scale, dy=Var.y_move_scale_zero)
        elif event_key == K_RIGHT:
            self.board.move_piece2(dx=Var.x_move_scale, dy=Var.y_move_scale_zero)
        elif event_key == K_UP:
            self.board.rotate_piece2()
        elif event_key == K_SPACE:
            self.board.full_drop_piece2()


    def vdresize2(self, resize, evheight):
        if (evheight>Var.display_min_height):
            font_resize = evheight/Var.display_min_height
            self.board.block_size = int(self.board.block_size*resize)
            if self.mode=='ai':
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size * Var.two_board_two
            else:
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size
            self.board.status_width = self.board.block_size * self.board.status_size
            self.board.font_size_big_in = int(Var.font_size_big*font_resize)
            self.board.font_size_middle_in = int(Var.font_size_middle*font_resize)
            self.board.font_size_small_in = int(Var.font_size_small*font_resize)
            self.board.display_height = self.board.height * self.board.block_size
            pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE )

    def vdresize(self, resize, evwidth):
        self.max_height = Var.infoObject.current_h - Var.bar_size
        font_resize = Var.font_resize
        if (self.board.height*int(self.board.block_size*resize)<self.min_height) :
            if self.mode == 'basic':
                if (self.board.height*int(self.board.block_size*resize)<self.min_height):
                    self.board.block_size = Var.basic_block_size
                    font_resize = Var.font_resize
                    pygame.display.set_mode((int(self.min_height*(self.board.width+self.board.status_size)/self.board.height),self.min_height), RESIZABLE)
            elif self.mode == 'mini':
                if (self.board.height*int(self.board.block_size*resize)<self.min_height):
                    self.board.block_size = Var.min_mini_block_size
                    font_resize = self.min_height/(Var.mini_block_size*self.board.height)
                    pygame.display.set_mode((int(self.min_height*(self.board.width+self.board.status_size)/self.board.height), self.min_height), RESIZABLE)
            else:
                self.board.block_size = Var.basic_block_size
                font_resize = Var.font_resize
                if self.mode == 'two':
                    pygame.display.set_mode((int(self.min_height*(self.board.width+self.board.status_size)/self.board.height), self.min_height), RESIZABLE)
                else:
                    pygame.display.set_mode((int(self.min_height*(self.board.width*Var.two_board_two+self.board.status_size*Var.two_board_two)/self.board.height), self.min_height), RESIZABLE)
            if self.mode=='ai':
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size * Var.two_board_two
            else:
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size
            print(font_resize, "1")
            self.board.status_width = self.board.block_size * self.board.status_size
            self.board.font_size_big_in = int(Var.font_size_big*font_resize)
            self.board.font_size_middle_in = int(Var.font_size_middle*font_resize)
            self.board.font_size_small_in = int(Var.font_size_small*font_resize)
            self.board.display_height = self.board.height * self.board.block_size


        elif (self.board.height*int(self.board.block_size*resize)>(self.max_height)):
            print(self.max_height)
            resize = self.max_height / self.board.display_height
            print(resize)
            self.board.block_size = int(self.board.block_size * resize)
            if self.mode == 'ai':
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size * Var.two_board_two
            else:
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size
            self.board.status_width = self.board.block_size * self.board.status_size
            font_resize = self.max_height / Var.display_min_height
            print(font_resize, '2')
            self.board.font_size_big_in = int(Var.font_size_big * font_resize)
            self.board.font_size_middle_in = int(Var.font_size_middle * font_resize)
            self.board.font_size_small_in = int(Var.font_size_small * font_resize)
            self.board.display_height = self.board.height * self.board.block_size
            info = pygame.display.Info()
            print(info.current_w, info.current_h)
            pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE)

        elif resize > Var.resize_cut_up or resize < Var.resize_cut_down:
            print('bas')
            if self.mode=='basic':
                font_resize = evwidth/(Var.basic_block_size*(self.board.width+self.board.status_size))
            if self.mode=='mini':
                font_resize = evwidth/(Var.mini_block_size*(self.board.width+self.board.status_size))
            if self.mode=='two':
                font_resize = evwidth/(Var.basic_block_size*(self.board.width+self.board.status_size))
            if self.mode=='ai':
                font_resize = evwidth/(Var.basic_block_size*(self.board.width*2+self.board.status_size*Var.two_board_two))
            self.board.block_size = int(self.board.block_size*resize)
            if self.mode=='ai':
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size * Var.two_board_two
            else:
                self.board.display_width = (self.board.width + self.board.status_size) * self.board.block_size
            print(font_resize, '3')
            self.board.status_width = self.board.block_size * self.board.status_size
            self.board.font_size_big_in = int(Var.font_size_big*font_resize)
            self.board.font_size_middle_in = int(Var.font_size_middle*font_resize)
            self.board.font_size_small_in = int(Var.font_size_small*font_resize)
            self.board.display_height = self.board.height * self.board.block_size
            pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE)


                #실행하기
    def run(self):
        pygame.init()
        (width, height) = pygame.display.get_surface().get_size()
        pygame.display.set_mode((width, height),RESIZABLE).fill(Var.BLACK)
        print(width, height)
        self.board = Board(self.mode)
        self.board.screen.fill(Var.BLACK)
        resize = height/self.board.display_height
        self.vdresize2(resize, height)
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')
        self.board.level_speed() #추가 - level1에서 속도
        self.gameover =False # ai 관련
        self.paused= False # ai 관련
        if self.mode=='ai':
            Var.ai_bgm.play()
        else:
            Var.base_bgm.play()
        if self.mode == 'ai':
            self.next_stone = Var.ai_tetris_shapes[
                random.randint(Var.ai_block_choice_start, Var.ai_block_choice_end)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        while True:
            if self.mode =='ai':
                Ai.choose(self.ai_board, self.stone, self.next_stone, self.stone_x, Var.weights, self)
            if self.check_reset:
                self.check_reset = False

            if self.mode =='ai':
                if self.board.game_over() or self.board.score < self.ai_score:
                    Var.ai_bgm.stop()
                    self.board.show_my_score()
                    break
                    
            if self.board.game_over():
                Var.base_bgm.stop()
                Var.ai_bgm.stop()
                Var.game_over.play()
                self.Score=self.board.score
                self.board.show_my_score()
                break

            for event in pygame.event.get():
                 #게임진행중 - event는 키보드 누를떄 특정 동작 수할떄 발생
                if event.type == QUIT: #종류 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종
                    sys.exit() #게임을 종료한다ㅏ.
                elif event.type == KEYUP and event.key == K_p: # 일시 정지 버튼 누르면
                    Var.base_bgm.stop()
                    Var.ai_bgm.stop()  #일시 정지 노래 중둠    오류나서  일단 뺴
                    self.board.pause()
                elif event.type == KEYDOWN: #키보드를 누르면
                    if self.mode=='two':
                        self.handle_key2(event.key, self.mode)  # handle 메소드 실행
                    else:
                        self.handle_key(event.key, self.mode) #handle 메소드 실행
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece(self.mode)
                    if self.mode=='two':
                        self.board.drop_piece2()

                elif event.type == Var.ai_event:
                    if self.mode == 'ai' :
                        self.ai_drop(False)
                #화면 크기 조절해 보기
                elif event.type == VIDEORESIZE:
                    info = pygame.display.Info()
                    print(info.current_w, info.current_h, "kkk")
                    resize = event.w/self.board.display_width
                    if event.h != self.board.display_height:
                        pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE)
                    if resize!=1:
                        self.vdresize(resize, event.w)
                        if info.current_w == (Var.current_w):
                            pygame.display.set_mode((info.current_w, info.current_h), RESIZABLE).fill(Var.BLACK)
                    print(self.board.display_width, self.board.display_height)
                    info = pygame.display.Info()
                    print(info.current_w, info.current_h, "dd")

                    #pygame.display.set_mode((300, 500),pygame.RESIZABLE)
            # self.screen.fill(BLACK)
            self.board.draw(self, self.mode)
            pygame.display.update() #이게 나오면 구현 시
            self.clock.tick(Var.fps) # 초당 프레임 관련
