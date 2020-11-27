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

resize = 1

block_size = 25 * resize
width = 10
height = 18

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
    return [[0 for i in range(width)]] + ai_board


# 매트릭스 합치기 (생성된 블럭과 + 배경 보드)에 사용
def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy + off_y - 1][cx + off_x] += val
    return mat1


# 새로운 보드 생성
def ai_new_board():
    ai_board = [[0 for x in range(height)] for y in range(height)]
    return ai_board


class AITetris(object):
    #생성자
    def __init__(self, seed):
        random.seed(seed)
        self.width = 10  # 가로 칸수
        self.height = 18  # 세로 칸 수
        self.block_size = 25 * resize  # 블럭 하나당 크기
        self.display_width = (self.width + 4) * self.block_size * 2
        self.display_height = self.height * self.block_size

        self.screen = pygame.display.set_mode((self.display_width, self.display_height))  # 고정 크기의 창을 만들어준다.  350 450
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.music_on_off = True
        self.check_reset = True

        #self.width = cell_size * (cols + 4)  # 게임의 너비
        #self.height = cell_size * rows
        self.next_stone = ai_tetris_shapes[random.randint(0, len(ai_tetris_shapes) - 1)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.ai_init_game()

        # 초기화 부분
    def ai_init_game(self):
        self.ai_board = ai_new_board()  # 새로운 게임 보드 생성
        self.ai_new_stone()  # 새로운 블럭 생성
        self.ai_level = 1  # 시작 레벨
        self.ai_score = 0  # 시작 스코어
        self.ai_lines = 0  # 지운 라인의 개수


            # 라인 지운 것에 대한 점수 및 지운 개수 추가
    def ai_new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = ai_tetris_shapes[
            random.randint(0, len(ai_tetris_shapes) - 1)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.stone_x = int(self.width / 2 - len(self.stone[0]) / 2)  # cols 기준 스톤의 위치 x
        self.stone_y = 0
        if ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True  # 블럭이 부딪히는 판단, 새로 생성한 블럭이 벽에 부딪히면은 게임 종료


    def ai_add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
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
            if new_x > self.width - len(self.stone[0]):  # 새로운 좌표 > 열의개수(10) - 블럭의 x축 길이
                new_x = self.width - len(self.stone[0])  # 이동 불가 (변경 없음)
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

    def ai_quit(self):
        pygame.display.update()  # 게임 화면 업데이트해주기
        sys.exit()  # 시스템 종료 하기

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

    #가장 높은 점수 불러 오는 부분
    def HighScore(self):
        try:
            f = open('assets/ai_save.txt', 'r')
            l = f.read()
            f.close()
            if int(l) < self.board.score:
                h_s = self.board.score
                f = open('assets/ai_save.txt', 'w')
                f.write(str(self.board.score))
                f.close()
            else:
                h_s = l
            self.board.HS(str(h_s))
        except:
            f = open('assets/ai_save.txt', 'w')
            f.write(str(self.board.score))
            f.close()
            self.board.HS(str(self.board.score))

    #실행하기
    def run(self, weights):
        pygame.init()
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('AITetris')

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
                self.ai_init_game()
                self.check_reset = False
                #pygame.mixer.music.play(-1, 0.0)  ## 수정 필요 오류 나서 일단 빼둠

            #게임 종료시 어떻게 할건가
            if self.board.game_over() or self.board.score  < self.ai_score:
                pygame.quit()
                break

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
            pygame.display.update() #이게 나오면 구현 시
            self.clock.tick(fps) # 초당 프레임 관련

