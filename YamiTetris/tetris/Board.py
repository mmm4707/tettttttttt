import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
from Menu import *
import threading
#from Database import Database



#색상 정보
#               R    G    B
BLACK = (0, 0, 0)
RED = (225, 13, 27)
GREEN = (98, 190, 68)
BLUE = (64, 111, 249)
ORANGE = (253, 189, 53)
YELLOW = (246, 227, 90)
PINK = (242, 64, 235)
CYON = (70, 230, 210)
GRAY = (26, 26, 26)
WHITE = (255, 255, 255)

max_speed = 750
min_speed = 150

# 나중에 사용할 사이즈 조절용 변수임
resize = 1

class Board:
    #충돌에러
    COLLIDE_ERROR = {'no_error' : 0, 'right_wall':1, 'left_wall':2,'bottom':3, 'overlap':4}

    def __init__(self, screen, mode):
        self.screen = screen
        self.mode = mode
        if (mode=='basic'):
            self.width = 10  #맵의 좌에서 우로 사이즈
            self.height = 18 #맵 위에서 아래로 사이즈
            self.block_size = 25*resize  #바꾸면 맵 블럭크기 변경
        if(mode=='mini'):
            self.width = 5  #맵의 좌에서 우로 사이즈
            self.height = 15 #맵 위에서 아래로 사이즈
            self.block_size = 35*resize  #바꾸면 맵 블럭크  기 변경
        if(mode=='two'):
            self.width = 20  # 맵의 좌에서 우로 사이즈
            self.height = 20  # 맵 위에서 아래로 사이즈
            self.block_size = 25  # 바꾸면 맵 블럭크기 변g경
        self.init_board() # 보드 생성 메소드 실행
        self.generate_piece(self.mode) # 블럭 생성 메소드 실행
        if(mode=='two'):
            self.generate_piece2()
        #self.database = Database()

        # 상태 줄 정보
        self.start_status_bar_x = self.width * self.block_size
        self.start_status_bar_y = 0
        if mode=='two':
            self.status_width = self.block_size * 6
        else:
            self.status_width = self.block_size * 4
        self.status_height = self.height * self.block_size
        self.font_size_small = 14
        self.font_size_middle = 16
        self.font_size_big = 18




    def level(self):
        return self.level


    def init_board(self):
        self.board = []
        self.score = 0 #시작 점수
        self.level = 1 #시작 level
        self.goal = 5  #level up 도달 목표 a
        self.skill = 0 #skill 퍼센트
        self.combo=0 # combo 수
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
        if(mode=='basic' or 'two'):
            self.piece_x, self.piece_y = 3, 0
        if(mode=='mini'):
            self.piece_x, self.piece_y = 0, 0

    def generate_piece2(self):
        self.piece2 = Piece()
        self.next_piece2 = Piece()
        self.piece_x2, self.piece_y2 = 12, 0

    def nextpiece(self, mode):  #다음에 나올 블럭 그려주기
        self.piece = self.next_piece
        self.next_piece = Piece()
        if(mode=='basic' or 'two'):
            self.piece_x, self.piece_y = 3, 0
        if(mode=='mini'):
            self.piece_x, self.piece_y = 0, 0

    def nextpiece2(self):  # 다음에 나올 블럭 그려주
        self.piece2 = self.next_piece2
        self.next_piece2 = Piece()
        self.piece_x2, self.piece_y2 = 12, 0

    def absorb_piece(self, mode):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.nextpiece(self.mode)
        self.score += self.level

    def absorb_piece2(self):
        for y, row in enumerate(self.piece2):
            for x, block in enumerate(row):
                if block:
                    self.board[y + self.piece_y2][x + self.piece_x2] = block
        self.nextpiece2()
        self.score += self.level


        #스킬 점수 설정 , 제거해야할 부분
        '''if self.skill < 100:
            self.skill += 2'''


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
        return self.can_move_piece(dx=0, dy=1)

    def can_drop_piece2(self):
        return self.can_move_piece2(dx=0, dy=1)

#블럭 회전 시도
    def try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        #충돌하지 않는 다면 패스
        if not collide:
            pass

        #왼쪽벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self.can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)

        #오른쪽 벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece(dx=-1, dy=0):
                self.move_piece(dx=-1, dy=0)
            elif self.can_move_piece(dx=-2, dy=0):
                self.move_piece(dx=-2, dy=0)
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
            if self.can_move_piece2(dx=1, dy=0):
                self.move_piece2(dx=1, dy=0)
            elif self.can_move_piece2(dx=2, dy=0):
                self.move_piece2(dx=2, dy=0)
            else:
                self.piece2.rotate(not clockwise)

            # 오른쪽 벽과 충돌하는 경우
        elif collide == Board.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece2(dx=-1, dy=0):
                self.move_piece2(dx=-1, dy=0)
            elif self.can_move_piece2(dx=-2, dy=0):
                self.move_piece2(dx=-2, dy=0)
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
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece(self.mode)
            self.delete_lines()

    def drop_piece2(self):
        if self.can_drop_piece2():
            self.move_piece2(dx=0, dy=1)
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
        return self.block_size*x*0.6, self.block_size*(y)*0.6


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
            '''line_sound = pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
            line_sound.play()'''
            #라인 삭제 실행
            self.delete_line(y)

            self.combo_null_start()
            #라인 삭제시 콤보 점수 1 증가

            self.combo+=1



            #콤보 *level * 10 만큼 점수 올려주기
            self.score += self.level*self.combo*10

            #level * 10 만큼 점수 올려주기
            self.score += 10 * self.level

            #level up까지 목표 골수 1만큼 내려주기
            self.goal -= 1

            if self.goal == 0:  # 만약 골이 0이된다면
                if self.level < 10:  #레벨이 10보다 작다면
                    self.level += 1  #레햣 벨 올려주고
                    self.goal = 5 * self.level  #레벨 * 5 만큼 골 수 변경
                else:  #레벨 10부터느 골수는 없음 ( - ) 로 표시
                    self.goal = '-'
            self.level_speed()  #추가 - level증가에 따른 속도 증가

    #추가 - 레벨별 스피드 조절
    def level_speed(self):
        if self.level <= 9:
            speed_change_per_level = 60
            pygame.time.set_timer(pygame.USEREVENT, (max_speed - speed_change_per_level * self.level))
        else :
            pygame.time.set_time(pygame.USEREVENT, min_speed)





    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

   # 현재 내려오고 있는 블럭 그려주기
    def draw_blocks(self, array2d, color=WHITE, dx=0, dy=0):
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
                        pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), 1)

    def draw_blocks2(self, array2d, color=WHITE, dx=0, dy=0):
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
                        pygame.draw.rect(self.screen, self.piece2.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
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
                        pygame.draw.rect(self.screen, self.piece.T_COLOR[7],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
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
                        pygame.draw.rect(self.screen, self.piece2.T_COLOR[7],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
                                         (x_s, y_s, self.block_size, self.block_size), 1)


    #다음 블럭 모양 만들어 주기 ?
    def draw_next_piece(self, array2d, color=WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],(x_pix+self.start_status_bar_x,   y_pix+self.block_size*2, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, BLACK, (x_pix+self.start_status_bar_x,   y_pix+self.block_size*2, self.block_size * 0.5, self.block_size * 0.5),1)

    def draw_next_piece2(self, array2d, color=WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, self.piece2.T_COLOR[block-1],(x_pix+self.start_status_bar_x+50,   y_pix+self.block_size*2, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, BLACK, (x_pix+self.start_status_bar_x+50,   y_pix+self.block_size*2, self.block_size * 0.5, self.block_size * 0.5),1)



#보드 내 필요한 내용 들 넣어주기
    def draw(self,tetris, mode):
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        self.screen.fill(BLACK)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, GRAY,
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)

        self.draw_shadow(self.piece, dx = self.piece_x, dy=self.piece_y) #그림자 기능 추가
        if self.mode=='two':
            self.draw_shadow2(self.piece2, dx=self.piece_x2, dy=self.piece_y2)  # 그림자 기능 추가

        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y-2)
        if self.mode=='two':
            self.draw_blocks2(self.piece2, dx=self.piece_x2, dy=self.piece_y2)
        self.draw_blocks(self.board)
        pygame.draw.rect(self.screen, WHITE, Rect(self.start_status_bar_x, self.start_status_bar_y,self.status_width,self.status_height))

        self.draw_next_piece(self.next_piece)
        if self.mode=='two':
            self.draw_next_piece2(self.next_piece2)


        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*resize).render('NEXT', True, BLACK)
        #skill_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18*resize).render('SKILL', True, BLACK)
        #skill_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16*resize).render(str(self.skill)+'%', True, BLACK)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*resize).render('SCORE', True, BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*resize).render(str(self.score), True, BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*resize).render('LEVEL', True, BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*resize).render(str(self.level), True, BLACK)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*resize).render('GOAL', True, BLACK)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*resize).render(str(self.goal), True, BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_small*resize).render(str(nowTime), True, BLACK)
        #콤보 값 넣어주기

        combo_text=pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*resize).render('COMBO', True, BLACK)
        combo_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*resize).render(str(self.combo), True, BLACK)


        self.screen.blit(next_text, (self.start_status_bar_x + self.status_width/15 , self.start_status_bar_y+  self.block_size ))
        #self.screen.blit(skill_text, (255, 120))
        #self.screen.blit(skill_value, (255, 140))
        self.screen.blit(score_text, (self.start_status_bar_x + self.status_width/15, self.start_status_bar_y + self.block_size*5 ))
        self.screen.blit(score_value, (self.start_status_bar_x + self.status_width/15,self.start_status_bar_y +  self.block_size*6 ))
        self.screen.blit(level_text, (self.start_status_bar_x + self.status_width/15, self.start_status_bar_y +  self.block_size*8 ))
        self.screen.blit(level_value, (self.start_status_bar_x + self.status_width/15,self.start_status_bar_y +  self.block_size*9 ))
        self.screen.blit(goal_text, (self.start_status_bar_x + self.status_width/15, self.start_status_bar_y +  self.block_size*11 ))
        self.screen.blit(goal_value, (self.start_status_bar_x + self.status_width/15,self.start_status_bar_y +  self.block_size*12 ))
        # 콤보 화며면에 표시
        self.screen.blit(combo_text, (self.start_status_bar_x + self.status_width/15, self.start_status_bar_y +  self.block_size*14 ))
        self.screen.blit(combo_value, (self.start_status_bar_x + self.status_width/15, self.start_status_bar_y +  self.block_size*15 ))
        self.screen.blit(time_text, (self.start_status_bar_x + self.status_width/15, self.start_status_bar_y +  self.block_size*17 ))


    #게임 일시정지
    def pause(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*2*resize) #글씨 폰트 설정
        textSurfaceObj = fontObj.render('Paused', True, GREEN)  #위 폰트로 초록색 글씨
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = ((self.start_status_bar_x+self.status_width)/2, self.block_size*8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*2*resize)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = ((self.start_status_bar_x+self.status_width)/2,self.block_size*12)

        #스크린에 표시
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p: #p 누르면 다싯 시작
                    running = False
#게임 오버 배경
    def GameOver(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*2*resize)
        textSurfaceObj = fontObj.render('Game over', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = ((self.start_status_bar_x+self.status_width)/2, self.block_size*8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*resize)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = ((self.start_status_bar_x+self.status_width)/2, self.block_size*12)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()

    #게임 끝나면 점수 보여주는 곳
    def show_my_score(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big*2*resize)
        textSurfaceObj = fontObj.render('My Score : '+str(self.score), True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = ((self.start_status_bar_x+self.status_width)/2, self.block_size*8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*resize)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = ((self.start_status_bar_x+self.status_width)/2, self.block_size*12)
        self.screen.fill(BLACK)
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

    def save_score(self, game_mode, ID):
        self.database.add_data(game_mode, ID, self.score)
