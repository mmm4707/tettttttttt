import random
from ai import Ai
import pygame, sys
from gui import Gui

# The configuration
cell_size =    25
cols =        10
rows =        18

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

# Define the shapes of the single parts
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

#블럭을 시계 방향으로 회전하기
def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

#벽과 부딪히는지 확인하기
def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

#행 지우기
def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board

#매트릭스 합치기 (생성된 블럭과 + 배경 보드)에 사용
def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1

#새로운 보드 생성
def new_board():
    board = [ [ 0 for x in range(cols) ] for y in range(rows) ]
    #board += [[ 1 for x in range(cols)]]
    return board

class TetrisApp(object):
    def __init__(self, seed):
        random.seed(seed)
        self.width = cell_size*(cols+4) # 게임의 너비
        self.height = cell_size*rows
        self.next_stone = tetris_shapes[random.randint(0, len(tetris_shapes)-1)] #다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.gui = Gui()
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = tetris_shapes[random.randint(0, len(tetris_shapes)-1)] #다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.stone_x = int(cols / 2 - len(self.stone[0])/2) #cols 기준 스톤의 위치 x
        self.stone_y = 0
        if check_collision(self.board,self.stone,(self.stone_x, self.stone_y)):
            self.gameover = True # 블럭이 부딪히는 판단, 새로 생성한 블럭이 벽에 부딪히면은 게임 종료

    def init_game(self):
        self.board = new_board()#새로운 게임 보드 생성
        self.new_stone()     #새로운 블럭 생성
        self.level = 1       #시작 레벨
        self.score = 0       # 시작 스코어
        self.lines = 0        # 지운 라인의 개수

    # 라인 지운 것에 대한 점수 및 지운 개수 추가
    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n  #지운 개수 추가하기
        self.score += linescores[n] * self.level #점수  = 원래 점수 + 한번에지운 라인개수에 해당하는 점수 * 레벨
        if self.lines >= self.level*6: # 지운 라인의 개수 >= 레벨*6 이되면 레벨 +1 하기
            self.level += 1

    # 블럭을 delta_x 만큼 움직이기
    def move(self, delta_x):
        if not self.gameover and not self.paused:  #게임 종료, 정지 상태가 아니라면
            new_x = self.stone_x + delta_x        #새로운 x 좌표는   기존의 stone의 x좌표 + 이동좌표수
            if new_x < 0:                        # 새로운 좌표가 0보다 작다면
                new_x = 0                         # 새로운 좌표는 0 ( 변경 없음 )
            if new_x > cols - len(self.stone[0]):   # 새로운 좌표 > 열의개수(10) - 블럭의 x축 길이
                new_x = cols - len(self.stone[0])  # 이동 불가 (변경 없음)
            if not check_collision(self.board, self.stone,(new_x, self.stone_y)):    #벽과 부딪히지 않는 다면
                self.stone_x = new_x   #새로운 좌표로 이동

    def drop(self, manual):
        if not self.gameover and not self.paused:   #게임 종료, 정지 상태가 아니라면
            self.score += 1 if manual else 0    #내릴 수 있다면  스코어+1, 내릴수 없다면 +0
            self.stone_y += 1                   # y축 좌표 +1
            if check_collision(self.board,self.stone,(self.stone_x, self.stone_y)):      #벽에 부딪히지 않는 경우에는
                self.board = join_matrixes(self.board,self.stone,(self.stone_x, self.stone_y))  # 새로운 보드는   블럭의 새로운 좌표를 포합한 보드로 갱신
                self.new_stone()  #새로운 블럭 생성하기
                cleared_rows = 0  #지운 행의 개수 초기화

                for i, row in enumerate(self.board):  # 모든 행마다 검사    i는 행의 번호
                    if 0 not in row:               # 행에 빈공간이 없다면 (0은 빈공간의 의미한다.)
                        self.board = remove_row( self.board, i) # ai보드를 i행을 지운 보드로 업데이트
                        cleared_rows += 1 # 지운개수 +1  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                self.add_cl_lines(cleared_rows)  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                return True  # 게임 종료 상태가 아니 었다면,  true 반환
        return False     # 게임이 정지, 종료 상태 였다면 false 반환

    #블럭 회전
    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    # 게임 시작
    def start_game(self):
        if self.gameover: # 게임이 종료된 상태라면
            self.init_game()  # 초기화 진행하기
            self.gameover = False #게임 종료는 false로 바꿔주기

    # 게임 종료
    def quit(self):
        pygame.display.update() #게임 화면 업데이트해주기
        sys.exit()  #시스템 종료 하기

    # 키에 해당하는 동작 지정해 주기 (ai가 동작 할 것 지정해 줄때 사용)
    def executes_moves(self, moves):
        key_actions = {
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        lambda:self.drop(True),
            'UP':        self.rotate_stone,
           # 'p':        self.toggle_pause,
            'SPACE':    self.start_game
        }
        # 받아온 moves에 저장되어 있는 동작 수행하기  -- (ai에서 학습된 것을 통해 결정 되는 부분)
        for action in moves:
            key_actions[action]()

    # 게임 시작 하기  (학습되어 있는 weight값 받아오기)
    def run(self, weights):
        self.gameover = False
        self.paused = False

        #dont_burn_my_cpu = pygame.time.Clock()
        while 1:



            self.gui.update(self)

            if self.gameover:
                return self.lines*1000


            Ai.choose(self.board, self.stone, self.next_stone, self.stone_x, weights, self)


            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                #elif event.type == pygame.KEYDOWN:
                 #    if event.key == eval("pygame.K_p"):
                  #      self.toggle_pause()

            #dont_burn_my_cpu.tick(maxfps)


if __name__ == '__main__':
    weights = [3.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093, -2.9262681134021786, -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861, -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956, -2.684925769670947, -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828, 0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105, -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306, 17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875] #21755 lignes
    TetrisApp( 4).run(weights)

