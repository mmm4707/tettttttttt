import pygame, sys, time

from ai_Board import *
import random
from ai import Ai



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
WHITE = (255, 255, 255)
colors = [BLACK, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, CYON, GRAY]

cell_size = 25
cols = 10
rows = 18
base_width = 350
base_height = 450
fps = 200

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


# 블럭을 시계 방향으로 회전하기
def ai_rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


# 벽과 부딪히는지 확인하기
def ai_check_collision(ai_board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and ai_board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


# 행 지우기
def ai_remove_row(ai_board, row):
    del ai_board[row]
    return [[0 for i in range(cols)]] + ai_board


# 매트릭스 합치기 (생성된 블럭과 + 배경 보드)에 사용
def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1][cx + off_x] += val
    return mat1



class AITetris(object):
    #생성자
    def __init__(self, seed):
        self.screen = pygame.display.set_mode((base_width*2, base_height)) # 고정 크기의 창을 만들어준다.  350 450
        self.clock = pygame.time.Clock()
        self.board = AIBoard(self.screen)
        self.music_on_off = True
        self.check_reset = True
        random.seed(seed)
        self.width = cell_size * (cols + 4)  # 게임의 너비
        self.height = cell_size * rows
        self.next_stone = ai_tetris_shapes[random.randint(0, len(ai_tetris_shapes) - 1)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.ai_init_game()

    def ai_new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = ai_tetris_shapes[
            random.randint(0, len(ai_tetris_shapes) - 1)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.stone_x = int(cols / 2 - len(self.stone[0]) / 2)  # cols 기준 스톤의 위치 x
        self.stone_y = 0
        if ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True  # 블럭이 부딪히는 판단, 새로 생성한 블럭이 벽에 부딪히면은 게임 종료

    #초기화 부분
    def ai_init_game(self):
        self.ai_board = [[0 for x in range(cols)] for y in range(rows)] # 새로운 게임 보드 생성
        self.ai_new_stone()  # 새로운 블럭 생성
        self.ai_level = 1  # 시작 레벨
        self.ai_score = 0  # 시작 스코어
        self.ai_lines = 0  # 지운 라인의 개수

        # 라인 지운 것에 대한 점수 및 지운 개수 추가

    def ai_add_cl_lines(self, n):
        linescores = [0, 20, 30, 40, 50]
        self.ai_lines += n  # 지운 개수 추가하기
        self.ai_score += linescores[n] * self.ai_level  # 점수  = 원래 점수 + 한번에지운 라인개수에 해당하는 점수 * 레벨
        if self.ai_lines >= self.ai_level * 6:  # 지운 라인의 개수 >= 레벨*6 이되면 레벨 +1 하기
            self.ai_level += 1

        # 블럭을 delta_x 만큼 움직이기

    def ai_move(self, delta_x):
        if not self.gameover and not self.paused:  # 게임 종료, 정지 상태가 아니라면
            new_x = self.stone_x + delta_x  # 새로운 x 좌표는   기존의 stone의 x좌표 + 이동좌표수
            if new_x < 0:  # 새로운 좌표가 0보다 작다면
                new_x = 0  # 새로운 좌표는 0 ( 변경 없음 )
            if new_x > cols - len(self.stone[0]):  # 새로운 좌표 > 열의개수(10) - 블럭의 x축 길이
                new_x = cols - len(self.stone[0])  # 이동 불가 (변경 없음)
            if not ai_check_collision(self.ai_board, self.stone, (new_x, self.stone_y)):  # 벽과 부딪히지 않는 다면
                self.stone_x = new_x  # 새로운 좌표로 이동

    def ai_drop(self, manual):
        if not self.gameover and not self.paused:  # 게임 종료, 정지 상태가 아니라면
            self.ai_score += 1 if manual else 0  # 내릴 수 있다면  스코어+1, 내릴수 없다면 +0
            self.stone_y += 1  # y축 좌표 +1
            if ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):  # 벽에 부딪히지 않는 경우에는
                self.ai_board = join_matrixes(self.ai_board, self.stone,
                                           (self.stone_x, self.stone_y))  # 새로운 보드는   블럭의 새로운 좌표를 포합한 보드로 갱신
                self.ai_new_stone()  # 새로운 블럭 생성하기
                cleared_rows = 0  # 지운 행의 개수 초기화

                for i, row in enumerate(self.ai_board):  # 모든 행마다 검사    i는 행의 번호
                    if 0 not in row:  # 행에 빈공간이 없다면 (0은 빈공간의 의미한다.)
                        self.ai_board = ai_remove_row(self.ai_board, i)  # ai보드를 i행을 지운 보드로 업데이트
                        cleared_rows += 1  # 지운개수 +1  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                self.ai_add_cl_lines(cleared_rows)  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                return True  # 게임 종료 상태가 아니 었다면,  true 반환
        return False  # 게임이 정지, 종료 상태 였다면 false 반환

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            ai_new_stone = ai_rotate_clockwise(self.stone)
            if not ai_check_collision(self.ai_board,
                                   ai_new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = ai_new_stone

    def ai_start_game(self):
        if self.gameover:  # 게임이 종료된 상태라면
            self.ai_init_game()  # 초기화 진행하기
            self.gameover = False  # 게임 종료는 false로 바꿔주기

    def ai_executes_moves(self, ai_moves):
        ai_key_actions = {
            'LEFT': lambda: self.ai_move(-1),
            'RIGHT': lambda: self.ai_move(+1),
            'DOWN': lambda: self.ai_drop(True),
            'UP': self.rotate_stone,
            # 'p':        self.toggle_pause,
            'SPACE': self.ai_start_game
        }
        # 받아온 moves에 저장되어 있는 동작 수행하기  -- (ai에서 학습된 것을 통해 결정 되는 부분)
        for ai_action in ai_moves:
            ai_key_actions[ai_action]()


    ###############################################################################
    #각 키를 누를떄 실행되는 method
    def handle_key(self, event_key):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece()
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()
        elif event_key == K_q: #스킬 부분
            self.board.ultimate()
        elif event_key == K_m: # 소리 설정
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()


    #실행하기
    def run(self, weights):
        pygame.init()
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')

        self.board.level_speed()

        #start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        #start_sound.play()
        #bgm = pygame.mixer.music.load('assets/sounds/bensound-ukulele.mp3')  # (기존 파일은 소리가 안남) 다른 mp3 파일은 소리 난다. 게임진행 bgm변경
        self.gameover = False
        self.paused = False
        delay = 150
        interval = 100
        pygame.key.set_repeat(delay, interval)

        while True:

            if self.check_reset:
                self.board.newGame()
                self.ai_init_game()
                self.check_reset = False
                #pygame.mixer.music.play(-1, 0.0)  ## 수정 필요 오류 나서 일단 빼둠

            #게임 종료시 어떻게 할건가
            if self.board.game_over() or self.board.score  < self.ai_score:
                self.screen.fill(BLACK) #게임 오버 배경 색
                #pygame.mixer.music.stop() #음악 멈추기     오류나서 일단 뺴
                #pygame.mixer.music.stop() #음악 멈추기     오류나서 일단 뺴
                self.board.GameOver()  #게임 오버 보드 불러오기
                self.board.show_my_score()


                #점수 저장 및 데이터 베이스에 저장 기능 추가하기

                self.check_reset = True
                self.board.init_board()

            Ai.choose(self.ai_board, self.stone, self.next_stone, self.stone_x, weights, self)

            for event in pygame.event.get(): #게임진행중 - event는 키보드 누를떄 특정 동작 수할떄 발생
                if event.type == QUIT: #종류 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종
                    sys.exit() #게임을 종료한다ㅏ.
                elif event.type == KEYUP and event.key == K_p: # 일시 정지 버튼 누르면
                    self.screen.fill(BLACK)         #일시 정지 화면
                    #pygame.mixer.music.stop()       #일시 정지 노래 중둠    오류나서 일단 뺴
                    self.board.pause()
                    #pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN: #키보드를 누르면
                    self.handle_key(event.key) #handle 메소드 실행
                elif event.type == pygame.USEREVENT or event.type == pygame.USEREVENT+1:
                    self.board.drop_piece()
                    self.ai_drop(False)

            self.board.draw(self)
            self.board.draw_AI(self)
            pygame.display.update() #이게 나오면 구현 시
            self.clock.tick(fps) # 초당 프레임 관련

if __name__ == '__main__':
    weights = [0.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093, -2.9262681134021786,
               -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861,
               -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956, -2.684925769670947,
               -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828,
               0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105,
               -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306,
               17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875]  # 21755 lignes
    AITetris(4).run(weights)




import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
import threading


tetris_shapes = [
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


#색상 정보
#               R    G    B
BLACK =  (0, 0, 0)
RED =  (225, 13, 27)
GREEN = (98, 190, 68)
BLUE = (64, 111, 249)
ORANGE = (253, 189, 53)
YELLOW = (246, 227, 90)
PINK  = (242, 64, 235)
CYON =  (70, 230, 210)
GRAY =  (23,23,23 )
WHITE = (255,255,255)

colors = [ BLACK, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, CYON, GRAY]


max_speed = 500
min_speed = 150

resize = 1

class AIBoard:
    #충돌에러
    COLLIDE_ERROR = {'no_error' : 0, 'right_wall':1, 'left_wall':2,'bottom':3, 'overlap':4}

    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.width = 10  #맵의 좌에서 우로 사이즈
        self.height = 18 #맵 위에서 아래로 사이즈
        self.block_size = 25*resize  #바꾸면 맵 블럭크기 변경
        self.init_board() # 보드 생성 메소드 실행
        self.generate_piece() # 블럭 생성 메소드 실행

        #화면 크기
        self.display_width = (self.width + 4) * self.block_size*2
        self.display_height = self.height * self.block_size

        #기존
        self.start_status_bar_x = self.width * self.block_size
        self.start_status_bar_y = 0
        self.status_width = self.block_size * 4
        self.status_height = self.height * self.block_size

        #ai용
        self.ai_start_status_bar_x = self.width * self.block_size +self.display_width/2
        self.ai_start_status_bar_y = 0


        #폰트 사이즈
        self.font_size_small = 14
        self.font_size_middle = 16
        self.font_size_big = 18

        pygame.event.set_blocked(pygame.MOUSEMOTION)


    def init_board(self):
        self.board = []
        self.score = 0 #시작 점수
        self.level = 1 #시작 level
        self.goal = 5  #level up 도달 목표
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


    def generate_piece(self):
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = 3, 0


    def nextpiece(self):  #다음에 나올 블럭 그려주
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



#충돌 관련
    def block_collide_with_board(self, x, y):
        #왼쪽 끝점 기준 (0,0)
        if x < 0:               # 왼쪽 벽
            return AIBoard.COLLIDE_ERROR['left_wall']
        elif x >= self.width:   #가로 길이 넘어가면
            return AIBoard.COLLIDE_ERROR['right_wall']
        elif y >= self.height:  #세로 기리 넘어가면
            return AIBoard.COLLIDE_ERROR['bottom']
        elif self.board[y][x]: #블럭이 다 쌓이면 ??
            return AIBoard.COLLIDE_ERROR['overlap']
        return AIBoard.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return AIBoard.COLLIDE_ERROR['no_error']

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
        elif collide == AIBoard.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self.can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)

        #오른쪽 벽과 충돌하는 경우
        elif collide == AIBoard.COLLIDE_ERROR['right_wall']:
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
            line_sound = pygame.mixer.Sound("assets/sounds/Line_Clear.wav")
            line_sound.play()
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
            pygame.time.set_timer(pygame.USEREVENT, (max_speed - 60 * self.level))
        else :
            pygame.time.set_time(pygame.USEREVENT, min_speed)


    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0


    #블럭 모양 만들어주기 ?
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

        # 다음 블럭 모양 만들어 주기 ?
    def draw_next_piece(self, array2d, color=WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x, y)
                    pygame.draw.rect(self.screen, self.piece.T_COLOR[block - 1], (
                    x_pix + self.start_status_bar_x, y_pix + self.block_size * 2, self.block_size * 0.5,
                    self.block_size * 0.5))
                    pygame.draw.rect(self.screen, BLACK, (
                    x_pix + self.start_status_bar_x, y_pix + self.block_size * 2, self.block_size * 0.5,
                    self.block_size * 0.5), 1)


    ###### AI 관련
    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,colors[val], pygame.Rect((off_x+x) *self.block_size,(off_y+y) *self.block_size,self.block_size,self.block_size),0)

    # 블럭을 시계 방향으로 회전하기
    def ai_rotate_clockwise(shape):
        return [[shape[y][x]
                 for y in range(len(shape))]
                for x in range(len(shape[0]) - 1, -1, -1)]

    # 벽과 부딪히는지 확인하기
    def ai_check_collision(ai_board, shape, offset):
        off_x, off_y = offset
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and ai_board[cy + off_y][cx + off_x]:
                        return True
                except IndexError:
                    return True
        return False

    # 행 지우기
    def ai_remove_row(ai_board, row):
        del ai_board[row]
        return [[0 for i in range(cols)]] + ai_board

    # 매트릭스 합치기 (생성된 블럭과 + 배경 보드)에 사용
    def join_matrixes(mat1, mat2, mat2_off):
        off_x, off_y = mat2_off
        for cy, row in enumerate(mat2):
            for cx, val in enumerate(row):
                mat1[cy + off_y - 1][cx + off_x] += val
        return mat1












#보드 내 필요한 내용 들 넣어주기
    def draw(self,tetris):
        now = datetime.datetime.now()
        nowTime = now.strftime('%H:%M:%S')
        self.screen.fill(GRAY)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, GRAY,
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)

        self.draw_shadow(self.piece, dx = self.piece_x, dy=self.piece_y) #그림자 기능 추가
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board)
        pygame.draw.rect(self.screen, WHITE, Rect(self.start_status_bar_x, self.start_status_bar_y,
                                                  self.status_width,
                                                  self.status_height))
        self.draw_next_piece(self.next_piece)


        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big * resize).render('NEXT', True, BLACK)
        # skill_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18*resize).render('SKILL', True, BLACK)
        # skill_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16*resize).render(str(self.skill)+'%', True, BLACK)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big * resize).render('SCORE', True,BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle * resize).render(str(self.score),True, BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big * resize).render('LEVEL', True,BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle * resize).render(str(self.level),True, BLACK)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big * resize).render('GOAL', True, BLACK)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle * resize).render(str(self.goal),True, BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_small * resize).render(str(nowTime), True,BLACK)
        # 콤보 값 넣어주기

        combo_text = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big * resize).render('COMBO', True,BLACK)
        combo_value = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle * resize).render(str(self.combo),True, BLACK)

        self.screen.blit(next_text,(self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size))
        # self.screen.blit(skill_text, (255, 120))
        # self.screen.blit(skill_value, (255, 140))
        self.screen.blit(score_text, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 5))
        self.screen.blit(score_value, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 6))
        self.screen.blit(level_text, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 8))
        self.screen.blit(level_value, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 9))
        self.screen.blit(goal_text, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 11))
        self.screen.blit(goal_value, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 12))

        # 콤보 화며면에 표시
        self.screen.blit(combo_text, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 14))
        self.screen.blit(combo_value, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 15))
        self.screen.blit(time_text, (self.start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 17))


        # AI관련 화면
    def draw_AI(self,tetris):
        pygame.draw.rect(self.screen, WHITE, Rect(self.ai_start_status_bar_x, self.ai_start_status_bar_y,self.ai_start_status_bar_x + self.status_width,self.ai_start_status_bar_y + self.status_height))

        ai_score_text = pygame.font.Font('ai_v2/python3_v/tetris/assets/Roboto-Bold.ttf', self.font_size_big * resize).render('SCORE', True,BLACK)  # 점수 글씨
        ai_score_value = pygame.font.Font('ai_v2/python3_v/tetris/assets/Roboto-Bold.ttf', self.font_size_middle * resize).render(str(tetris.ai_score), True, BLACK)  # 점수 표시해주기

        self.screen.blit(ai_score_text, (self.ai_start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 9))  # 정해둔 값을 화면에 올리기
        self.screen.blit(ai_score_value, (self.ai_start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 11))

            #  self.ai_draw_matrix(self.bground_grid, (0,0))   #(0,0) 부터 내가 설정한 격자 그려주기
        self.draw_matrix(tetris.ai_board, (self.width + (self.status_width / self.block_size),0))  # (0.0) 부터  보드 업데이트 해주기 ####################################### 블럭이 쌓이는 위치 알려줌
        self.draw_matrix(tetris.stone, (tetris.stone_x + self.width + (self.status_width / self.block_size), tetris.stone_y))  # 테트리스 블럭을 그려준다. 블럭의 왼쪽 끝 좌표부터 - 시작 블럭

        computer_said1 = pygame.font.Font('ai_v2/python3_v/tetris/assets/Roboto-Bold.ttf', self.font_size_middle * resize).render("YOU CAN'T", True,BLACK)
        computer_said2 = pygame.font.Font('ai_v2/python3_v/tetris/assets/Roboto-Bold.ttf', self.font_size_middle * resize).render("DEFEAT ME", True, BLACK)

        self.screen.blit(computer_said1, (self.ai_start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 1))
        self.screen.blit(computer_said2, (self.ai_start_status_bar_x + self.status_width / 15, self.start_status_bar_y + self.block_size * 2))
            # 배경에 라인 추가 하기 -> 테트리스 보드 칸을 나눠주는 선 만들기
        for i in range(self.width + 1):
            pygame.draw.line(self.screen, BLACK, ((self.block_size) * i + self.display_width/2, 0),((self.block_size) * i + self.display_width/2, self.display_height - 1), 2)
        for j in range(self.height + 1):
            pygame.draw.line(self.screen, BLACK, (self.display_width/2, (self.block_size) * j),(self.block_size * self.width - 1 + self.display_width/2, (self.block_size) * j), 2)


    #게임 일시정지
    def pause(self):
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*2* resize) #글씨 폰트 설정
        textSurfaceObj = fontObj.render('Paused', True, GREEN)  #위 폰트로 초록색 글씨
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle* resize)
        textSurfaceObj2 = fontObj2.render('Press p to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (self.display_width/2, self.start_status_bar_y + self.block_size *11 )

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
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*2* resize)
        textSurfaceObj = fontObj.render('Game over', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle* resize)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 11)
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
        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*2* resize)
        textSurfaceObj = fontObj.render('Tetris', True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle* resize)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 11)
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
    def show_my_score(self):

        fontObj = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle*2* resize)
        textSurfaceObj = fontObj.render('My Score : '+str(self.score), True, GREEN)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 8)
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle* resize)
        textSurfaceObj2 = fontObj2.render('Press a key to continue', True, GREEN)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (self.display_width/2, self.start_status_bar_y + self.block_size * 11)
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

#스킬 사용 remove

