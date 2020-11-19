import time
import pygame, sys
from ai_Board import *



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

base_width = 350
base_height = 450

max_speed = 750
min_speed = 150


time = 300


class Gui(object):
    def __init__(self):
        pygame.init()
        #pygame.key.set_repeat(250,25)
        self.width_size = base_width*2
        self.height_size = base_height
        #self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(cols)] for y in range(rows)]

        #self.default_font =  pygame.font.Font(pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width_size, self.height_size))
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        pygame.time.set_timer(pygame.USEREVENT + 1, time)


    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,colors[val], pygame.Rect((off_x+x) *cell_size,(off_y+y) *cell_size,cell_size,cell_size),0)


