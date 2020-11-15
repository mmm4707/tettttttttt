#!/usr/bin/env python2
import copy
import time
import threading
import random
from ai_field import ai_Field
from ai import Ai
import pygame, sys
from ai_gui import ai_Gui

# The configuration
ai_cell_size =    25
ai_cols =        10
ai_rows =        18

#colors = [
 #   (0, 0, 0),
  #  (225, 13, 27), #레드
   # (98, 190, 68), #그린
    #(64, 111, 249), #블루
   # (253, 189, 53), # 오렌지
   # (246, 227, 90), #엘로우
   # (242, 64, 235), #핑크
    #(70, 230, 210), #사이온
   # (23,23,23 )  # Helper color for background grid
#]

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

def ai_rotate_clockwise(ai_shape):
    return [ [ ai_shape[y][x] for y in range(len(ai_shape)) ] for x in range(len(ai_shape[0]) - 1, -1, -1) ]

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

def ai_remove_row(ai_board, row):
    del ai_board[row]
    return [[0 for i in range(ai_cols)]] + ai_board

def ai_join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1][cx+off_x] += val
    return mat1

def ai_new_board():
    ai_board = [ [ 0 for x in range(ai_cols) ]
            for y in range(ai_rows) ]
    #board += [[ 1 for x in range(cols)]]
    return ai_board


class AITetris(object):
    def __init__(self, seed):
        random.seed(seed)
        self.ai_next_stone = ai_tetris_shapes[random.randint(0, len(ai_tetris_shapes)-1)] #다음 블럭 랜덤으로 고르기
        self.gui = ai_Gui()
        self.init_game()

    def ai_new_stone(self):
        self.stone = self.ai_next_stone[:]
        self.ai_next_stone = ai_tetris_shapes[random.randint(0, len(ai_tetris_shapes)-1)]
        self.stone_x = int((ai_cols / 2 - len(self.stone[0])/2))
        self.stone_y = 0
        if ai_check_collision(self.ai_board,self.stone,(self.stone_x, self.stone_y)):
            self.gameover = True

     #게임 실행시 초기화 시켜주기!
    def init_game(self):
        self.ai_board = ai_new_board()
        self.ai_new_stone()
        self.ai_level = 1
        self.ai_score = 0
        self.ai_lines = 0

    def add_cl_lines(self, n):
        ai_linescores = [0, 40, 100, 300, 1200]
        self.ai_lines += n
        self.ai_score += ai_linescores[n] * self.ai_level
        if self.ai_lines >= self.ai_level*6:
            self.ai_level += 1

    def ai_move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > ai_cols - len(self.stone[0]):
                new_x = ai_cols - len(self.stone[0])
            if not ai_check_collision(self.ai_board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def ai_drop(self, manual):
        if not self.gameover and not self.paused:
            self.ai_score += 1 if manual else 0
            self.stone_y += 1
            if ai_check_collision(self.ai_board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.ai_board = ai_join_matrixes(self.ai_board,self.stone,(self.stone_x, self.stone_y))
                self.ai_new_stone()
                cleared_rows = 0

                for i, row in enumerate(self.ai_board):
                    if 0 not in row:
                        self.ai_board = ai_remove_row(self.ai_board, i)
                        cleared_rows += 1
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def ai_rotate_stone(self):
        if not self.gameover and not self.paused:
            ai_new_stone = ai_rotate_clockwise(self.stone)
            if not ai_check_collision(self.ai_board,
                                   ai_new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = ai_new_stone



    def ai_start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def ai_quit(self):
        pygame.display.update()
        sys.exit()

    def ai_executes_moves(self, moves):
        key_actions = {
            'LEFT':        lambda:self.ai_move(-1),
            'RIGHT':    lambda:self.ai_move(+1),
            'DOWN':        lambda:self.ai_drop(True),
            'UP':        self.ai_rotate_stone,
            'SPACE':    self.ai_start_game,
        }
        for action in moves:
            key_actions[action]()

    def run(self, weights):
        self.gameover = False
        self.paused = False

        #dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.gui.update(self)
            Ai.choose(self.ai_board, self.stone, self.ai_next_stone, self.stone_x, weights, self)

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.ai_drop(False)
                elif event.type == pygame.QUIT:
                    self.ai_quit()




if __name__ == '__main__':
    weights = [0.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093, -2.9262681134021786, -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861, -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956, -2.684925769670947, -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828, 0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105, -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306, 17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875] #21755 lignes
    AITetris(4).run(weights)

