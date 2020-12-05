import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
import threading
from variable import Var


class Board:
    #충돌에러
    COLLIDE_ERROR = {'no_error' : 0, 'right_wall':1, 'left_wall':2,'bottom':3, 'overlap':4}

    def __init__(self,  mode):
        self.mode = mode

        if (mode=='basic'):
            self.width = 10  #맵의 좌에서 우로 사이즈
            self.height = 18 #맵 위에서 아래로 사이즈
            self.block_size = Var.basic_block_size  #바꾸면 맵 블럭크기 변경
            self.status_size = 4
            self.display_width = (self.width + self.status_size) * self.block_size
        if(mode=='mini'):
            self.width = 5  #맵의 좌에서 우로 사이즈
            self.height = 15 #맵 위에서 아래로 사이즈
            self.block_size = Var.mini_block_size  #바꾸면 맵 블럭크  기 변경
            self.status_size = 4
            self.display_width = (self.width + self.status_size) * self.block_size
        if(mode=='two'):
            self.width = 20  # 맵의 좌에서 우로 사이즈
            self.height = 18  # 맵 위에서 아래로 사이즈
            self.block_size = Var.basic_block_size   # 바꾸면 맵 블럭크기 변경
            self.status_size = 6
            self.display_width = (self.width + self.status_size) * self.block_size
        if(mode == "ai"):
            self.width = 10  # 맵의 좌에서 우로 사이즈
            self.height = 18  # 맵 위에서 아래로 사이즈
            self.block_size = Var.basic_block_size   # 바꾸면 맵 블럭크기 변g경
            self.status_size = 4
            self.display_width = (self.width + self.status_size) * self.block_size*2



        self.display_height = self.height * self.block_size
        self.screen = pygame.display.set_mode((self.display_width, self.display_height), RESIZABLE)

        self.screen = pygame.display.set_mode((self.display_width, self.display_height), RESIZABLE)


        self.init_board() # 보드 생성 메소드 실행
        self.generate_piece(self.mode) # 블럭 생성 메소드 실행
        if(mode=='two'):
            self.generate_piece2()
        #self.database = Database()


        # 상태 줄 정보
        #(self.width*self.block_size) = self.width * self.block_size
        self.start_status_bar_y = 0
        if mode=='two':
            self.status_width = self.block_size * self.status_size
        else:
            self.status_width = self.block_size * self.status_size
        #(self.height*self.block_size) = self.height * self.block_size

        #(self.width * self.block_size + self.display_width / 2) = self.width * self.block_size + self.display_width / 2
        self.ai_start_status_bar_y = 0

        self.font_size_small_in = Var.font_size_small
        self.font_size_middle_in = Var.font_size_middle
        self.font_size_big_in = Var.font_size_big

        pygame.event.set_blocked(pygame.MOUSEMOTION)

    def init_board(self):
        self.board = []
        self.score = Var.initial_score #시작 점수
        self.level = Var.initial_level #시작 level
        self.goal = Var.initial_goal  #level up 도달 목표 a

        self.combo = Var.initial_combo # combo 수
        self.timer0 = threading.Timer(10, self.combo_null)
        self.timer1 = threading.Timer(10, self.combo_null)
        self.timer2 = threading.Timer(10, self.combo_null)
        self.timer3 = threading.Timer(10, self.combo_null)
        self.timer4 = threading.Timer(10, self.combo_null)
        self.timer5 = threading.Timer(10, self.combo_null)
        self.timer6 = threading.Timer(10, self.combo_null)
        self.timer7 = threading.Timer(10, self.combo_null)
        self.timer8 = threading.Timer(10, self.combo_null)
        self.timer9 = threading.Timer(10, self.combo_null)
        self.timer_list=[self.timer0,self.timer1,self.timer2,self.timer3,self.timer4,self.timer5,self.timer6,self.timer7,self.timer8,self.timer9]
        for _ in range(self.height):
            self.board.append([0]*self.width)

    def generate_piece(self, mode):
        self.piece = Piece()
        self.next_piece = Piece()

        if(mode=='basic' or 'two' or 'ai'):
            self.piece_x, self.piece_y = Var.block_start_basic_x , Var.block_start_y

        if(mode=='mini'):
            self.piece_x, self.piece_y = Var.block_start_mini_x, Var.block_start_y

    def generate_piece2(self):
        self.piece2 = Piece()
        self.next_piece2 = Piece()
        self.piece_x2, self.piece_y2 = Var.block_start_two_x, Var.block_start_y

    def nextpiece(self, mode):  #다음에 나올 블럭 그려주기
        self.piece = self.next_piece
        self.next_piece = Piece()

        if(mode=='basic' or 'two' or 'ai'):
            self.piece_x, self.piece_y = Var.block_start_basic_x , Var.block_start_y
        if(mode=='mini'):
            self.piece_x, self.piece_y = Var.block_start_mini_x, Var.block_start_y

    def nextpiece2(self):  # 다음에 나올 블럭 그려주
        self.piece2 = self.next_piece2
        self.next_piece2 = Piece()
        self.piece_x2, self.piece_y2 =  Var.block_start_two_x, Var.block_start_y

    def absorb_piece(self, mode):
        Var.block_fall.play()
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.nextpiece(self.mode)
        self.score += self.level


    def absorb_piece2(self):
        Var.block_fall.play()
        for y, row in enumerate(self.piece2):
            for x, block in enumerate(row):
                if block:
                    self.board[y + self.piece_y2][x + self.piece_x2] = block
        self.nextpiece2()
        self.score += self.level


#충돌 관련
    def block_collide_with_board(self, x, y):
        #왼쪽 끝점 기준 (0,0)
        if x < 0:               # 왼쪽 벽
            return Board.COLLIDE_ERROR['left_wall']
        elif x >= self.width:   #가로 길이 넘어가면
            return Board.COLLIDE_ERROR['right_wall']
        elif y >= self.height:  #세로 기리 넘어가면
            return Board.COLLIDE_ERROR['bottom']
        elif self.board[y][x]: #블럭이 다 쌓이면 ??
            return Board.COLLIDE_ERROR['overlap']
        return Board.COLLIDE_ERROR['no_error']

    def block_collide_with_Two_Baord2(self, x, y):
        #왼쪽 끝점 기준 (0,0)
        if x < 0:               # 왼쪽 벽
            return Board.COLLIDE_ERROR['left_wall']
        elif x >= self.width:   #가로 길이 넘어가면
            return Board.COLLIDE_ERROR['right_wall']
        elif y >= self.height:  #세로 기리 넘어가면
            return Board.COLLIDE_ERROR['bottom']
        elif self.board[y][x]: #블럭이 다 쌓이면 ??
            return Board.COLLIDE_ERROR['overlap']
        return Board.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Board.COLLIDE_ERROR['no_error']


    def collide_with_Two_Board2(self, dx, dy):
        for y, row in enumerate(self.piece2):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_Two_Baord2(x=x + dx, y=y + dy)
                    if collide:
                        return collide
        return Board.COLLIDE_ERROR['no_error']

#블럭이 움직일 수 있는 경우 판단
    def can_move_piece(self, dx, dy):
        _dx = self.piece_x + dx
        _dy = self.piece_y + dy
        if self.collide_with_board(dx = _dx, dy = _dy):
            return False
        return True

    def can_move_piece2(self, dx, dy):
        _dx = self.piece_x2 + dx
        _dy = self.piece_y2 + dy
        if self.collide_with_Two_Board2(dx=_dx, dy=_dy):
            return False
        return True

#아래로 한칸 내려가는 것
    def can_drop_piece(self):
        return self.can_move_piece(dx=0, dy=Var.y_move_scale)

    def can_drop_piece2(self):
        return self.can_move_piece2(dx=0, dy=Var.y_move_scale)

#블럭 회전 시도
    def try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        #충돌하지 않는 다면 패스
        if not collide:
            pass

        #왼쪽벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=Var.x_move_scale, dy=0):
                self.move_piece(dx=Var.x_move_scale, dy=0)
            elif self.can_move_piece(dx=Var.x_move_scale*2, dy=0):
                self.move_piece(dx=Var.x_move_scale*2, dy=0)
            else:
                self.piece.rotate(not clockwise)

        #오른쪽 벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece(dx=-Var.x_move_scale, dy=0):
                self.move_piece(dx=-Var.x_move_scale, dy=0)
            elif self.can_move_piece(dx=-Var.x_move_scale*2, dy=0):
                self.move_piece(dx=-Var.x_move_scale*2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)


    def try_rotate_piece2(self, clockwise=True):
        self.piece2.rotate(clockwise)
        collide = self.collide_with_Two_Board2(dx=self.piece_x2, dy=self.piece_y2)
        # 충돌하지 않는 다면 패스
        if not collide:
            pass

        # 왼쪽벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece2(dx=Var.x_move_scale, dy=0):
                self.move_piece2(dx=Var.x_move_scale, dy=0)
            elif self.can_move_piece2(dx=Var.x_move_scale*2, dy=0):
                self.move_piece2(dx=Var.x_move_scale*2, dy=0)
            else:
                self.piece2.rotate(not clockwise)

            # 오른쪽 벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece2(dx=-Var.x_move_scale, dy=0):
                self.move_piece2(dx=-Var.x_move_scale, dy=0)
            elif self.can_move_piece2(dx=-Var.x_move_scale*2, dy=0):
                self.move_piece2(dx=-Var.x_move_scale*2, dy=0)
            else:
                self.piece2.rotate(not clockwise)

        else:
            self.piece2.rotate(not clockwise)

#블럭 움직이기
    def move_piece(self, dx, dy):
        #만약 움직이는 가능하다면
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def move_piece2(self, dx, dy):

        if self.can_move_piece2(dx, dy):
            self.piece_x2 += dx

            self.piece_y2 += dy

#블럭 내리기
    def drop_piece(self, mode):
        if self.can_drop_piece():
            self.move_piece(dx=0, dy=Var.y_move_scale)
        else:
            self.absorb_piece(self.mode)
            self.delete_lines()

    def drop_piece2(self):
        if self.can_drop_piece2():
            self.move_piece2(dx=0, dy=Var.y_move_scale)
        else:
            self.absorb_piece2()
            self.delete_lines()


# 블럭 완전히 밑으로 내리기(내릴 수 없을떄 까지)
    def full_drop_piece(self, mode):
        while self.can_drop_piece():
            self.drop_piece(self.mode)
        self.drop_piece(self.mode)

    def full_drop_piece2(self):
        while self.can_drop_piece2():
            self.drop_piece2()
        self.drop_piece2()


#블럭 회전 시키기
    def rotate_piece(self, clockwise=True):
        self.try_rotate_piece(clockwise)

    def rotate_piece2(self, clockwise=True):
        self.try_rotate_piece2(clockwise)

    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y)

    def pos_to_pixel_next(self, x, y):
        return self.block_size*x*Var.basic_next_block_size_rate, self.block_size*(y)*Var.basic_next_block_size_rate


    def delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def combo_null(self):
        self.combo=0

    def combo_null_start(self):
        for i in range(9):
            if self.combo==i:
                self.timer_list[i]=threading.Timer(10, self.combo_null)
                self.timer_list[i].start()
                for j in range(9):
                    if i != j :
                        self.timer_list[j].cancel()
    # 라인 삭제하기
    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            #라인 제거 할떄 소리

            #콤보 사운드 할거면 여기
            Var.line_clear.play()

            #라인 삭제 실행
            self.delete_line(y)
            self.combo_null_start()
            #라인 삭제시 콤보 점수 1 증가
            self.combo+=1

            #콤보 *level * 10 만큼 점수 올려주기
            self.score += self.level*self.combo*Var.combo_score_rate
            #level * 10 만큼 점수 올려주기
            self.score += Var.level_score_rate * self.level
            #level up까지 목표 골수 1만큼 내려주기
            self.goal -= 1

            if self.goal == 0:  # 만약 골이 0이된다면
                if self.level < Var.max_level:  #레벨이 10보다 작다면
                    self.level += 1  #레햣 벨 올려주고
                    self.goal = Var.initial_goal * self.level  #레벨 * 5 만큼 골 수 변경

                    Var.level_up.play()
                else:  #레벨 10부터느 골수는 없음 ( - ) 로 표시
                    self.goal = '-'
            self.level_speed()  #추가 - level증가에 따른 속도 증가

        # 추가 - 레벨별 스피드 조절
    def level_speed(self):
        if self.level < Var.max_level:
            pygame.time.set_timer(pygame.USEREVENT, (Var.user_start_speed -  Var.user_per_speed * self.level))
            pygame.time.set_timer(pygame.USEREVENT + 1, (Var.AI_start_speed -  Var.AI_per_speed * self.level))
        else:
            pygame.time.set_timer(pygame.USEREVENT, (Var.user_start_speed -  Var.user_per_speed * self.level))
            pygame.time.set_timer(pygame.USEREVENT + 1, (Var.AI_start_speed -  Var.AI_per_speed * self.level))

    def game_over(self):

        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

   # 현재 내려오고 있는 블럭 그려주기
    def draw_blocks(self, array2d, color=Var.WHITE, dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 0 and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        tmp = 1
                        while self.can_move_piece(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y+tmp-1)
                        pygame.draw.rect(self.screen, Var.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Var.BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), 1)

    def draw_blocks2(self, array2d, color=Var.WHITE, dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 0 and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        tmp = 1
                        while self.can_move_piece2(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y+tmp-1)
                        pygame.draw.rect(self.screen, Var.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Var.BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), 1)


    def draw_shadow(self, array2d, dx, dy):  # 그림자 오류 디버깅     #########
        for y, row in enumerate(array2d):
            y += dy
            if y >= 0 and y < self.height:
                for x, block in enumerate(row):
                    x += dx
                    if block:
                        tmp = 1
                        while self.can_move_piece(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y + tmp - 1)
                        pygame.draw.rect(self.screen, Var.T_COLOR[7],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Var.BLACK,
                                         (x_s, y_s, self.block_size, self.block_size), 1)

    def draw_shadow2(self, array2d, dx, dy):  # 그림자 오류 디버깅     #########
        for y, row in enumerate(array2d):
            y += dy
            if y >= 0 and y < self.height:
                for x, block in enumerate(row):
                    x += dx
                    if block:
                        tmp = 1
                        while self.can_move_piece2(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y + tmp - 1)
                        pygame.draw.rect(self.screen, Var.T_COLOR[7],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Var.BLACK,
                                         (x_s, y_s, self.block_size, self.block_size), 1)


    #다음 블럭 모양 만들어 주기 ?
    def draw_next_piece(self, array2d, color=Var.WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, Var.T_COLOR[block-1],(x_pix+(self.width*self.block_size),   y_pix+self.block_size*1.5, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, Var.BLACK, (x_pix+(self.width*self.block_size),   y_pix+self.block_size*1.5, self.block_size * 0.5, self.block_size * 0.5),1)

    def draw_next_piece2(self, array2d, color=Var.WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, Var.T_COLOR[block-1],(x_pix+(self.width*self.block_size)+self.status_width*0.45,   y_pix+self.block_size*1.5, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, Var.BLACK, (x_pix+(self.width*self.block_size)+self.status_width*0.45,   y_pix+self.block_size*1.5, self.block_size * 0.5, self.block_size * 0.5),1)

    ###### AI 관련
    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, Var.colors[val],
                                    pygame.Rect((off_x + x) * self.block_size, (off_y + y) * self.block_size,
                                    self.block_size, self.block_size), 0)

    ###### AI 관련
    # 블럭을 시계 방향으로 회전하기
    def ai_rotate_clockwise(self, shape):
        return [[shape[y][x]for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

    ###### AI 관련
    # 벽과 부딪히는지 확인하기
    def ai_check_collision(self, ai_board, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and ai_board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                        return True
        return False

    ###### AI 관련
    # 행 지우기
    def ai_remove_row(self, ai_board, row):
        del ai_board[row]
        return [[0 for i in range(self.width)]] + ai_board

        ###### AI 관련
        # 매트릭스 합치기 (생성된 블럭과 + 배경 보드)에 사용
    def join_matrixes(self, mat1, mat2, mat2_off):
        off_x, off_y = mat2_off
        for cy, row in enumerate(mat2):
            for cx, val in enumerate(row):
                mat1[cy + off_y - 1][cx + off_x] += val
        return mat1


#보드 내 필요한 내용 들 넣어주기
    def draw(self,tetris, mode):
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        if self.mode == 'basic' or self.mode == 'two' or self.mode == 'mini':
            self.screen.fill(Var.BLACK)
        elif self.mode == 'ai':
            self.screen.fill(Var.GRAY)

        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, Var.GRAY,
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, Var.BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)

        self.draw_shadow(self.piece, dx = self.piece_x, dy=self.piece_y) #그림자 기능 추가
        self.draw_blocks(self.piece, dx = self.piece_x, dy=self.piece_y)

        if self.mode=='two':
            self.draw_shadow2(self.piece2, dx=self.piece_x2, dy=self.piece_y2)  # 그림자 기능 추가
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)

        if self.mode=='two':
            self.draw_blocks2(self.piece2, dx=self.piece_x2, dy=self.piece_y2)

        self.draw_blocks(self.board)
        pygame.draw.rect(self.screen, Var.MAIN_WHITE, Rect((self.width*self.block_size), self.start_status_bar_y,self.status_width,(self.height*self.block_size)))

        self.draw_next_piece(self.next_piece)
        if self.mode=='two':
            self.draw_next_piece2(self.next_piece2)


        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in).render('NEXT', True, Var.MAIN_BLUE)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in).render('SCORE', True, Var.MAIN_BLUE)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle_in).render(str(self.score), True, Var.MAIN_BLUE)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in).render('LEVEL', True, Var.MAIN_BLUE)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle_in).render(str(self.level), True, Var.MAIN_BLUE)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in).render('GOAL', True, Var.MAIN_BLUE)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle_in).render(str(self.goal), True, Var.MAIN_BLUE)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_small_in).render(str(nowTime), True, Var.MAIN_BLUE)
        #콤보 값 넣어주기

        combo_text=pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in).render('COMBO', True, Var.MAIN_BLUE)
        combo_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle_in).render(str(self.combo), True, Var.MAIN_BLUE)


        self.screen.blit(next_text, ((self.width*self.block_size) + self.status_width/15 , self.block_size*self.height*0.05 ))

        self.screen.blit(score_text, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.3 ))

        self.screen.blit(score_value, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.35 ))
        self.screen.blit(level_text, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.45 ))
        self.screen.blit(level_value, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.5 ))
        self.screen.blit(goal_text, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.6 ))
        self.screen.blit(goal_value, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.65 ))
        # 콤보 화며면에 표시
        self.screen.blit(combo_text, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.75 ))
        self.screen.blit(combo_value, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.8 ))
        self.screen.blit(time_text, ((self.width*self.block_size) + self.status_width/15, self.block_size*self.height*0.95 ))
        if self.mode == 'ai':
            pygame.draw.rect(self.screen, Var.MAIN_WHITE, Rect((self.width * self.block_size + self.display_width / 2), self.ai_start_status_bar_y,
                                                      (self.width * self.block_size + self.display_width / 2) + self.status_width,
                                                      self.ai_start_status_bar_y + (self.height*self.block_size)))

            ai_score_text = pygame.font.Font('assets/Roboto-Bold.ttf',
                                             self.font_size_big_in).render('SCORE', True, Var.BLACK)  # 점수 글씨
            ai_score_value = pygame.font.Font('assets/Roboto-Bold.ttf',
                                              self.font_size_middle_in).render(str(tetris.ai_score), True,
                                                                                     Var.BLACK)  # 점수 표시해주기

            self.screen.blit(ai_score_text, ((self.width * self.block_size + self.display_width / 2) + self.status_width / 15,
                                             self.start_status_bar_y + self.block_size * 9))  # 정해둔 값을 화면에 올리기
            self.screen.blit(ai_score_value, (
            (self.width * self.block_size + self.display_width / 2) + self.status_width / 15, self.start_status_bar_y + self.block_size * 11))

            #  self.ai_draw_matrix(self.bground_grid, (0,0))   #(0,0) 부터 내가 설정한 격자 그려주기
            self.draw_matrix(tetris.ai_board, (self.width + (self.status_width / self.block_size),
                                               0))  # (0.0) 부터  보드 업데이트 해주기 ####################################### 블럭이 쌓이는 위치 알려줌
            self.draw_matrix(tetris.stone, (tetris.stone_x + self.width + (self.status_width / self.block_size),
                                            tetris.stone_y))  # 테트리스 블럭을 그려준다. 블럭의 왼쪽 끝 좌표부터 - 시작 블럭

            computer_said1 = pygame.font.Font('assets/Roboto-Bold.ttf',
                                              self.font_size_middle_in).render("YOU CAN'T", True, Var.BLACK)
            computer_said2 = pygame.font.Font('assets/Roboto-Bold.ttf',
                                              self.font_size_middle_in).render("DEFEAT ME", True, Var.BLACK)

            self.screen.blit(computer_said1, (
            (self.width * self.block_size + self.display_width / 2) + self.status_width / 15, self.start_status_bar_y + self.block_size * 1))
            self.screen.blit(computer_said2, (
            (self.width * self.block_size + self.display_width / 2) + self.status_width / 15, self.start_status_bar_y + self.block_size * 2))
            # 배경에 라인 추가 하기 -> 테트리스 보드 칸을 나눠주는 선 만들기
            for i in range(self.width + 1):
                pygame.draw.line(self.screen, Var.BLACK, ((self.block_size) * i + self.display_width / 2, 0),
                                 ((self.block_size) * i + self.display_width / 2, self.display_height - 1), 2)
            for j in range(self.height + 1):
                pygame.draw.line(self.screen, Var.BLACK, (self.display_width / 2, (self.block_size) * j),
                                 (self.block_size * self.width - 1 + self.display_width / 2, (self.block_size) * j), 2)

    #게임 일시정지
    def pause(self):

        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in*2) #글씨 폰트 설정
        textSurfaceObj = fontObj.render('Paused', True, Var.GREEN)  #위 폰트로 초록색 글씨

        textRectObj = textSurfaceObj.get_rect()
        if self.mode == 'ai':
            textRectObj.center = (((self.width*self.block_size)+self.status_width)/2, self.block_size*8)
        else:
            textRectObj.center = (self.display_width / 2, self.start_status_bar_y + self.block_size * 8)

        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big_in*2)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, Var.GREEN)

        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (((self.width*self.block_size)+self.status_width)/2,self.block_size*12)
        if self.mode == 'ai':
            textRectObj2.center = (self.display_width / 2, self.start_status_bar_y + self.block_size * 11)
        else:
            textRectObj.center = (self.display_width / 2, self.start_status_bar_y + self.block_size * 8)

        #스크린에 표시
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p: #p 누르면 다싯 시작
                    if self.mode == 'ai':
                        Var.ai_bgm.play()
                    else:
                        Var.base_bgm.play()
                    running = False
#게임 오버 배경
    def GameOver(self):

        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', Var.font_size_big*2*resize)
        textSurfaceObj = fontObj.render('Game over', True, Var.WHITE)

        textRectObj = textSurfaceObj.get_rect()
        if self.mode == 'ai':
            textRectObj.center = (((self.width*self.block_size)+self.status_width)/2, self.block_size*8)
        else:
            textRectObj.center = (self.display_width / 2, self.start_status_bar_y + self.block_size * 8)

        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', Var.font_size_middle*resize)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Var.WHITE)



        textRectObj2 = textSurfaceObj2.get_rect()
        if self.mode == 'ai':
            textRectObj2.center = (self.display_width/2, self.block_size*12)
        else:
            textRectObj2.center = (self.display_width / 2, self.start_status_bar_y + self.block_size * 11)

        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()

    #게임 끝나면 점수 보여주는 곳
    def show_my_score(self):

        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', int(self.font_size_big_in*2))

        textSurfaceObj = fontObj.render('My Score : '+str(self.score), True, Var.MAIN_BLUE)
        textRectObj = textSurfaceObj.get_rect()
        if self.mode == 'ai':
            textRectObj.center = (self.display_width/2, self.display_height*0.4)
        else:
            textRectObj.center = (self.display_width/2, self.display_height*0.4)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', int(self.font_size_middle_in))
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Var.MAIN_BLUE)
        textRectObj2 = textSurfaceObj2.get_rect()
        if self.mode == 'ai':
            textRectObj2.center = (self.display_width/2, self.display_height*0.7)
        else:
            textRectObj2.center = (self.display_width/2, self.display_height*0.7)
        self.screen.fill(Var.MAIN_WHITE)

        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False
                elif event.type == VIDEORESIZE:
                    done_resize = event.w/self.display_width
                    if event.h != self.display_height:
                        pygame.display.set_mode((self.display_width, self.display_height), RESIZABLE)
                    elif done_resize > 1.01 or done_resize < 1:
                        font_resize = event.w/((self.width*2+self.status_size*2)*self.block_size)
                        if self.mode=='basic':
                            font_resize = event.w/350
                        if self.mode=='mini':
                            font_resize = event.w/315
                        if self.mode=='two':
                            font_resize = event.w/650
                        if self.mode=='ai':
                            font_resize = event.w/700
                        self.font_size_big_in = int(self.font_size_big*font_resize)
                        self.font_size_middle_in = int(self.font_size_middle*font_resize)
                        self.block_size = int(self.block_size*done_resize)
                        if self.mode == 'ai':
                            self.display_width = (self.width + self.status_size) * self.block_size * 2
                        else:
                            self.display_width = (self.width + self.status_size) * self.block_size
                        self.display_height = self.height * self.block_size
                        pygame.display.set_mode((self.display_width, self.display_height), RESIZABLE)
                    fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', int(self.font_size_big_in*2))
                    textSurfaceObj = fontObj.render('My Score : '+str(self.score), True, Var.MAIN_BLUE)
                    textRectObj = textSurfaceObj.get_rect()
                    if self.mode == 'ai':
                        textRectObj.center = (self.display_width/2, self.display_height*0.4)
                    else:
                        textRectObj.center = (self.display_width/2, self.display_height*0.4)
                    fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', int(self.font_size_middle_in))
                    textSurfaceObj2 = fontObj2.render('Press a key to continue', True, Var.MAIN_BLUE)
                    textRectObj2 = textSurfaceObj2.get_rect()
                    if self.mode == 'ai':
                        textRectObj2.center = (self.display_width/2, self.display_height*0.7)
                    else:
                        textRectObj2.center = (self.display_width/2, self.display_height*0.7)
                    self.screen.fill(MAIN_WHITE)
                    self.screen.blit(textSurfaceObj, textRectObj)
                    self.screen.blit(textSurfaceObj2, textRectObj2)
                    pygame.display.update()
                    running = True


    def save_score(self, game_mode, ID):
        self.database.add_data(game_mode, ID, self.score)
