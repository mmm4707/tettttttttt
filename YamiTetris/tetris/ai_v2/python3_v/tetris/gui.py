import time
import pygame, sys

# The configuration
cell_size =    25
cols =        10
rows =        18
maxfps =     30
time =     50 # ai속도 조절
maxPiece = 500

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

class Gui(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = base_width*2
        self.height = base_height
        self.rlim = cell_size*cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(cols)] for y in range(rows)]

        self.default_font =  pygame.font.Font(
            pygame.font.get_default_font(), 12)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.time.set_timer(pygame.USEREVENT+1, time)

    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14



    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,colors[val], pygame.Rect((off_x+x) *cell_size,(off_y+y) *cell_size,cell_size,cell_size),0)

    def update(self, tetris):
        self.screen.fill((23,23,23))
        if tetris.gameover:# or self.nbPiece >= maxPiece:
            pass
           # self.center_msg("""Game Over!\nYour score: %dPress space to continue""" % tetris.score)
        else:
            if tetris.paused:
                self.center_msg("Paused")
            else:
                menu_size = 100
                pygame.draw.rect(self.screen, WHITE, pygame.Rect(self.width-menu_size, 0, base_height, base_height))  # 게임 화면에 하얀색으로 네모 그려주기
                ai_score_text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render('SCORE', True, BLACK)  # 점수 글씨
                ai_score_value = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(str(tetris.score), True,BLACK)  # 점수 표시해주기


                self.screen.blit(ai_score_text, (605, 180))  # 정해둔 값을 화면에 올리기
                self.screen.blit(ai_score_value, (605, 200))

                #   self.ai_draw_matrix(self.bground_grid, (0,0))   #(0,0) 부터 내가 설정한 격자 그려주기
                self.draw_matrix(tetris.board, (cols+(menu_size/cell_size), 0))  # (0.0) 부터  보드 업데이트 해주기 ####################################### 블럭이 쌓이는 위치 알려줌
                self.draw_matrix(tetris.stone, (tetris.stone_x+cols+(menu_size/cell_size), tetris.stone_y))  # 테트리스 블럭을 그려준다. 블럭의 왼쪽 끝 좌표부터 - 시작 블럭

                computer_said1 = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render("YOU CAN'T", True, BLACK)
                computer_said2 = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render("DEFEAT ME", True, BLACK)

                self.screen.blit(computer_said1, (605, 20))
                self.screen.blit(computer_said2, (605, 40))

                # 배경에 라인 추가 하기 -> 테트리스 보드 칸을 나눠주는 선 만들기
                for i in range(cols + 1):
                    pygame.draw.line(self.screen, BLACK, ((cell_size) * i+base_width, 0),
                                     ((cell_size) * i+base_width, self.height - 1), 2)

                for j in range(rows + 1):
                    pygame.draw.line(self.screen, BLACK, (base_width, (cell_size) * j),
                                     (cell_size * cols - 1+base_width, (cell_size) * j), 2)

            pygame.display.update()
