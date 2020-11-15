#!/usr/bin/env python2
import copy
import time
from random import randrange as rand
from ai_field import ai_Field
from ai import Ai
import pygame, sys

# The configuration
ai_cell_size =    25
ai_cols =        10
ai_rows =        18
#maxfps =     30
ai_time =     50 # ai속도 조절



colors = [
    (0, 0, 0),     # 블랙
    (225, 13, 27), #레드
    (98, 190, 68), #그린
    (64, 111, 249), #블루
    (253, 189, 53), # 오렌지
    (246, 227, 90), #엘로우
    (242, 64, 235), #핑크
    (70, 230, 210), #사이온
    (23,23,23 )  # 회색
]

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

class ai_Gui(object):
    def __init__(self):
        pygame.init()
        #pygame.key.set_repeat(250,25)
        self.ai_width = ai_cell_size*(ai_cols+6)
        self.ai_height = ai_cell_size*ai_rows

        self.ai_bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(ai_cols)] for y in range(ai_rows)]

        #게임 스크린 사이즈
        self.ai_screen = pygame.display.set_mode((700, 450))

        #게임 속도 조절
        #주어진 시간 (밀리 초)마다 이벤트 큐에 표시 할 이벤트 유형을 설정합니다.
        pygame.time.set_timer(pygame.USEREVENT+1, ai_time)


    def ai_draw_matrix(self, matrix, ai_offset):
        off_x, off_y  = ai_offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.ai_screen,colors[val], pygame.Rect((off_x+x*ai_cell_size +350 , (off_y+y) *ai_cell_size,ai_cell_size,ai_cell_size)) ,0)

    def update(self, tetris):
        self.ai_screen.fill((23,23,23))
        if tetris.gameover:# or self.nbPiece >= maxPiece:
            pass
           # self.center_msg("""Game Over!\nYour score: %dPress space to continue""" % tetris.score)
        else:
             pygame.draw.rect(self.ai_screen, (255,255,255), pygame.Rect(600, 0, 450, 450))
             ai_score_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SCORE', True, (0,0,0))
             ai_score_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(tetris.ai_score), True, (0,0,0))
             self.ai_screen.blit(ai_score_text, (605, 180))
             self.ai_screen.blit(ai_score_value, (605, 200))

             self.ai_draw_matrix(self.ai_bground_grid, (0,0))
             self.ai_draw_matrix(tetris.ai_board, (0,0))
             self.ai_draw_matrix(tetris.stone, (tetris.stone_x+100, tetris.stone_y)) #생성 위치 바뀜

             computer_said1 = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render("YOU CAN'T", True, (0, 0, 0))
             computer_said2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render("DEFEAT ME", True, (0, 0, 0))

             self.ai_screen.blit(computer_said1, (605, 20))
             self.ai_screen.blit(computer_said2, (605, 40))

             # 배경에 라인 추가 하기
             for i in range(ai_cols + 1):
                 pygame.draw.line(self.ai_screen, (0, 0, 0), ((ai_cell_size) * i+350, 0), ((ai_cell_size) * i+350, self.ai_height - 1),2)

             for j in range(ai_rows + 1):
                 pygame.draw.line(self.ai_screen, (0, 0, 0), (0+350, (ai_cell_size) * j),
                                     (ai_cell_size * ai_cols - 1+350, (ai_cell_size) * j), 2)

        pygame.display.update()

