import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
import threading


#색상 정보
#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)


class Board:
    #충돌에러
    COLLIDE_ERROR = {'no_error' : 0, 'right_wall':1, 'left_wall':2,
                     'bottom':3, 'overlap':4}

    def __init__(self, screen):
        self.screen = screen
        self.width = 10  #맵의 좌에서 우로 사이즈
        self.height = 20 #맵 위에서 아래로 사이즈
        self.block_size = 25  #바꾸면 맵 블럭크기 변경
        self.init_board() # 보드 생성 메소드 실행
        self.generate_piece() # 블럭 생성 메소드 실행

    def init_board(self):
        self.board = []
        self.score = 0 #시작 점수
        self.level = 1 #시작 level
        self.goal = 5  #level up 도달 목표
        self.skill = 0 #skill 퍼센트
        self.combo=0 # combo 수

        for _ in range(self.height):
            self.board.append([0]*self.width)

    def generate_piece(self):
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = 3, 0

    def nextpiece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.piece_x, self.piece_y = 3, 0

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.nextpiece()
        self.score += self.level

        #스킬 점수 설정 , 제거해야할 부분
        if self.skill < 100:
            self.skill += 2


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

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
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

#아래로 한칸 내려가는 것
    def can_drop_piece(self):
        return self.can_move_piece(dx=0, dy=1)

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
#블럭 움직이기
    def move_piece(self, dx, dy):
        #만약 움직이는 가능하다면
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy
#블럭 내리기
    def drop_piece(self):
        if self.can_drop_piece():
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()

# 블럭 완전히 밑으로 내리기(내릴 수 없을떄 까지)
    def full_drop_piece(self):
        while self.can_drop_piece():
            self.drop_piece()
        self.drop_piece()

#블럭 회전 시키기
    def rotate_piece(self, clockwise=True):
        self.try_rotate_piece(clockwise)


    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y-2)

    def pos_to_pixel_next(self, x, y):
        return self.block_size*x*0.6, self.block_size*(y-2)*0.6


    def delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

# 라인 삭제하기
    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            #라인 제거 할떄 소리
            line_sound = pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
            line_sound.play()
            #라인 삭제 실행
            self.delete_line(y)

            #라인 삭제시 콤보 점수 1 증가
            self.combo+=1

            #콤보 *level * 10 만큼 점수 올려주기
            self.score=self.level*self.combo*10

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
            pygame.time.set_timer(pygame.USEREVENT, (750 - 60 * self.level))
        else :
            pygame.time.set_time(pygame.USEREVENT, 150)





    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

#블럭 모양 만들어주기 ?
    def draw_blocks(self, array2d, color=WHITE, dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        tmp = 1
                        while self.can_move_piece(0, tmp):
                            tmp += 1
                        x_s, y_s = self.pos_to_pixel(x, y+tmp-1)
                        pygame.draw.rect(self.screen, self.piece.T_COLOR[7],
                                        (x_pix, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
                                        (x_pix, y_s, self.block_size, self.block_size),1)
                        pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), 1)

#다음 블럭 모양 만들어 주기 ?
    def draw_next_piece(self, array2d, color=WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, self.piece.T_COLOR[block-1],
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, BLACK,
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5),1)


#보드 내 필요한 내용 들 넣어주기
    def draw(self):
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        self.screen.fill(BLACK)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, (26,26,26),
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)

        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)

        self.draw_blocks(self.board)
        pygame.draw.rect(self.screen, WHITE, Rect(250, 0, 350, 450))
        self.draw_next_piece(self.next_piece)
        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('NEXT', True, BLACK)
        skill_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SKILL', True, BLACK)
        skill_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.skill)+'%', True, BLACK)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SCORE', True, BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.score), True, BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('LEVEL', True, BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.level), True, BLACK)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('GOAL', True, BLACK)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.goal), True, BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', 14).render(str(nowTime), True, BLACK)

        #콤보 값 넣어주기

        combo_text=pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('COMBO', True, BLACK)
        combo_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(self.combo), True, BLACK)




        self.screen.blit(next_text, (255, 20))
        self.screen.blit(skill_text, (255, 120))
        self.screen.blit(skill_value, (255, 140))
        self.screen.blit(score_text, (255, 180))
        self.screen.blit(score_value, (255,200))
        self.screen.blit(level_text, (255, 240))
        self.screen.blit(level_value, (255,260))
        self.screen.blit(goal_text, (255, 300))
        self.screen.blit(goal_value, (255,320))
        # 콤보 화며면에 표시
        self.screen.blit(combo_text, (255, 360))
        self.screen.blit(combo_value, (255, 380))
        self.screen.blit(time_text, (255, 430))

    #게임 일시정지
    def pause(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32) #글씨 폰트 설정
        textSurfaceObj = fontObj.render('Paused', True, GREEN)  #위 폰트로 초록색 글씨
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)

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
                    running = False
#게임 오버 배경
    def GameOver(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Game over', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
        self.screen.blit(textSurfaceObj, textRectObj)
        self.screen.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN: #아무 거나 누르면 다시 시작
                    running = False

#새로운 게임 시작하기 배경
    def newGame(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
        textSurfaceObj = fontObj.render('Tetris', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (175, 185)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (175, 235)
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

#가장 높은 점수 보여주기 배경
    def HS(self, txt="no"):
        if txt != "no":
            fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', 32)
            textSurfaceObj = fontObj.render('HighScore : '+txt, True, GREEN)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (175, 185)
            fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16)
            textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
            textRectObj2 = textSurfaceObj2.get_rect()
            textRectObj2.center = (175, 235)
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

#스킬 사용
    def ultimate(self):
        if self.skill == 100:
            bomb = pygame.image.load("assets/images/bomb.jpg")
            bomb = pygame.transform.scale(bomb, (350, 450))
            bomb_sound = pygame.mixer.Sound('assets/sounds/bomb.wav')
            self.screen.blit(bomb, (0, 0))
            pygame.display.update()
            bomb_sound.play()
            time.sleep(1)
            self.board = []
            self.skill = 0
            for _ in range(self.height):
                self.board.append([0]*self.width)
