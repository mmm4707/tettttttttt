import random
from ai import Ai
import pygame, sys
from ai_gui import ai_Gui

# The configuration
ai_cell_size =    25
ai_cols =        10
ai_rows =        18

BLACK =  (0, 0, 0),
RED =  (225, 13, 27), #레드
GREEN = (98, 190, 68), #그린
BLUE = (64, 111, 249), #블루
ORANGE = (253, 189, 53), # 오렌지
YELLOW = (246, 227, 90), #엘로우
PINK  = (242, 64, 235), #핑크
CYON =  (70, 230, 210), #사이온
GRAY =  (23,23,23 )  # Helper color for background grid
colors = [ BLACK, RED, GREEN, BLUE, ORANGE, YELLOW, PINK, CYON, GRAY]

# Define the shapes of the single parts
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

#블럭을 시계 방향으로 회적하기
def ai_rotate_clockwise(ai_shape):
    return [ [ ai_shape[y][x] for y in range(len(ai_shape)) ] for x in range(len(ai_shape[0]) - 1, -1, -1) ]

#벽과 부딪히는지 확인하기
def ai_check_collision(ai_board, ai_shape, ai_offset):
    off_x, off_y = ai_offset
    for cy, row in enumerate(ai_shape):
        for cx, cell in enumerate(row):
            try:
                if cell and ai_board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

#행 지우기
def ai_remove_row(ai_board, row):
    del ai_board[row]  #보드에서 row에 해당하는 부분의 내용들을 지우기
    return [[0 for i in range(ai_cols)]] + ai_board   #row에 해당하는 것을 지운 보드를 반환해주기

#매트릭스 합치기 (생성된 블럭과 + 배경 보드)에 사용
def ai_join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1

#새로운 보드 생성
def ai_new_board():
    #행의 개수만큼, 열의 개수 만크 -> 다 0으로 채워주기
    ai_board = [ [ 0 for x in range(ai_cols) ]
            for y in range(ai_rows) ]
    #board += [[ 1 for x in range(cols)]]
    return ai_board  #return으로 새롭게 정의된 보드 생성


class AITetris(object):
    def __init__(self, seed):
        random.seed(seed)
        self.ai_next_stone = ai_tetris_shapes[random.randint(0, len(ai_tetris_shapes)-1)] #다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.gui = ai_Gui() #gui 클래스 객체 생성
        self.init_game()
    #새로운 블럭 생성
    def ai_new_stone(self):
        self.stone = self.ai_next_stone[:]
        self.ai_next_stone = ai_tetris_shapes[random.randint(0, len(ai_tetris_shapes)-1)] #다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.stone_x = int((ai_cols / 2 - len(self.stone[0])/2))   #열크기/2 - 블럭의 크기/2    5 - 2
        self.stone_y = 0
        if ai_check_collision(self.ai_board,self.stone,(self.stone_x, self.stone_y)):  # 블럭이 부딪히는 판단, 새로 생성한 블럭이 벽에 부딪히면은 게임 종료
            self.gameover = True

     #게임 실행시 초기화 시켜주기!
    def init_game(self):
        self.ai_board = ai_new_board() #새로운 게임 보드 생성
        self.ai_new_stone()            #새로운 블럭 생성
        self.ai_level = 1              #시작 레벨
        self.ai_score = 0              # 시작 스코어
        self.ai_lines = 0              # 지운 라인의 개수

    #라인 지운 것에 대한 점수 및 지운 개수 추가
    def add_cl_lines(self, n):
        ai_linescores = [0, 40, 100, 300, 1200]
        self.ai_lines += n    #지운 개수 추가하기
        self.ai_score += ai_linescores[n] * self.ai_level   #점수  = 원래 점수 + 한번에지운 라인개수에 해당하는 점수 * 레벨
        if self.ai_lines >= self.ai_level*6: # 지운 라인의 개수 >= 레벨*6 이되면 레벨 +1 하기
            self.ai_level += 1

    #블럭을 delta_x 만큼 움직이기
    def ai_move(self, delta_x):
        if not self.gameover and not self.paused:      #게임 종료, 정지 상태가 아니라면
            new_x = self.stone_x + delta_x             #새로운 x 좌표는   기존의 stone의 x좌표 + 이동좌표수
            if new_x < 0:                              # 새로운 좌표가 0보다 작다면
                new_x = 0                              # 새로운 좌표는 0 ( 변경 없음 )
            if new_x > ai_cols - len(self.stone[0]):   # 새로운 좌표 > 열의개수(10) - 블럭의 x축 길이
                new_x = ai_cols - len(self.stone[0])    # 이동 불가 (변경 없음)
            if not ai_check_collision(self.ai_board,self.stone,(new_x, self.stone_y)):   #벽과 부딪히지 않는 다면
                self.stone_x = new_x                                                     #새로운 좌표로 이동

    #블럭 내리기
    def ai_drop(self, manual):
        if not self.gameover and not self.paused:   #게임 종료, 정지 상태가 아니라면
            self.ai_score += 1 if manual else 0     #내릴 수 있다면  스코어+1, 내릴수 없다면 +0
            self.stone_y += 1                       # y축 좌표 +1
            if ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):      #벽에 부딪히지 않는 경우에는
                self.ai_board = ai_join_matrixes(self.ai_board,self.stone,(self.stone_x, self.stone_y))  # 새로운 보드는   블럭의 새로운 좌표를 포합한 보드로 갱신
                self.ai_new_stone()  #새로운 블럭 생성하기
                cleared_rows = 0     #지운 행의 개수 초기화

                for i, row in enumerate(self.ai_board):  # 모든 행마다 검사    i는 행의 번호
                    if 0 not in row:                     # 행에 빈공간이 없다면 (0은 빈공간의 의미한다.)
                        self.ai_board = ai_remove_row(self.ai_board, i)    # ai보드를 i행을 지운 보드로 업데이트
                        cleared_rows += 1                                  # 지운개수 +1
                self.add_cl_lines(cleared_rows)                            # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                return True                                                # 게임 종료 상태가 아니 었다면,  true 반환
        return False                                                       # 게임이 정지, 종료 상태 였다면 false 반환

    # ai블럭 회전 시키기
    def ai_rotate_stone(self):
        if not self.gameover and not self.paused:     #게임 종료, 정지 상태가 아니라면
            ai_new_stone = ai_rotate_clockwise(self.stone)      #새로운 블럭을  기존의 블럭을 시계방향을 회전시킨 것으로 봐꿔준다.
            if not ai_check_collision(self.ai_board,ai_new_stone,(self.stone_x, self.stone_y)):   #회전 했을때 변에 부딪히지 않는다면, 회전 시킨 블럭을 선정하기
                self.stone = ai_new_stone


    #게임 시작하기
    def ai_start_game(self):
        if self.gameover:    # 게임이 종료된 상태라면
            self.init_game()  # 초기화 진행하기
            self.gameover = False  #게임 종료는 false로 바꿔주기

    # 게임 종료
    def ai_quit(self):
        pygame.display.update() #게임 화면 업데이트해주기
        sys.exit()              #시스템 종료 하기

    # 키에 해당하는 동작 지정해 주기 (ai가 동작 할 것 지정해 줄때 사용)
    def ai_executes_moves(self, moves):
        key_actions = {
            'LEFT':        lambda:self.ai_move(-1),  # 왼쪽 끝 기준 -1 만큼 이동
            'RIGHT':    lambda:self.ai_move(+1),     # 왼쪽 끝 기준 +1 만큼 이동
            'DOWN':        lambda:self.ai_drop(True),  # 블럭 내리기
            'UP':        self.ai_rotate_stone,        # 블럭 회전
            'SPACE':    self.ai_start_game,           # 게임 시작 하기
        }

        #받아온 moves에 저장되어 있는 동작 수행하기  -- (ai에서 학습된 것을 통해 결정 되는 부분)
        for action in moves:
            key_actions[action]()

    #게임 시작 하기  (학습되어 있는 weight값 받아오기)
    def run(self, weights):
        self.gameover = False   #게임이 끝난 상태가 아니라하기
        self.paused = False      # 정지 상태가 아니다고 표시

        #dont_burn_my_cpu = pygame.time.Clock()

        # 1 = ture   일단은 무한 반복
        while 1:

            # gui 최신화
            self.gui.update(self)  #객체 자신을 업데이트 하게 된다.

            # ai class의 choose 실행 (학습을 통해 최적화 된 동작 (회전, 왼쪽, 오른쪽 이동))
            Ai.choose(self.ai_board, self.stone, self.ai_next_stone, self.stone_x, weights, self)

            #pygame이 돌아가는 핵심 요소
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.ai_drop(False)
                elif event.type == pygame.QUIT:
                    self.ai_quit()




if __name__ == '__main__':
    weights = [0.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093, -2.9262681134021786, -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861, -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956, -2.684925769670947, -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828, 0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105, -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306, 17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875] #21755 lignes
    AITetris(4).run(weights)

