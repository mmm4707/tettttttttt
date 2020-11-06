import pygame, sys, time
from pygame.locals import *
from AIBoard import *

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

import pygame
import random
import tetris_ai


colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 350  #화면에서 시작부분
    y = 0
    zoom = 25
    figure = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

        self.screen = pygame.display.set_mode((700, 450))  # 고정 크기의 창을 만들어준다.  350 450
        self.clock = pygame.time.Clock()
        self.aiboard = AIBoard(self.screen)
        self.music_on_off = True
        self.check_reset = True



    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


    #각 키를 누를떄 실행되는 method
    def handle_key(self, event_key):
        if event_key == K_DOWN or event_key == K_s:
            self.aiboard.drop_piece()
        elif event_key == K_LEFT or event_key == K_a:
            self.aiboard.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT or event_key == K_d:
            self.aiboard.move_piece(dx=1, dy=0)
        elif event_key == K_UP or event_key == K_w:
            self.aiboard.rotate_piece()
        elif event_key == K_SPACE:
            self.aiboard.full_drop_piece()
        elif event_key == K_q: #스킬 부분
            self.aiboard.ultimate()
        elif event_key == K_m: # 소리 설정
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()

    #가장 높은 점수 불러 오는 부분
    def HighScore(self):
        try:
            f = open('assets/save.txt', 'r')
            l = f.read()
            f.close()
            if int(l) < self.aiboard.score:
                h_s = self.aiboard.score
                f = open('assets/save.txt', 'w')
                f.write(str(self.aiboard.score))
                f.close()
            else:
                h_s = l
            self.aiboard.HS(str(h_s))
        except:
            f = open('assets/save.txt', 'w')
            f.write(str(self.aiboard.score))
            f.close()
            self.aiboard.HS(str(self.aiboard.score))

    #실행하기
    def run(self):
        pygame.init()
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')

        self.aiboard.level_speed() #추가 - level1에서 속도

        start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        start_sound.play()
        bgm = pygame.mixer.music.load('assets/sounds/bensound-ukulele.mp3')  # (기존 파일은 소리가 안남) 다른 mp3 파일은 소리 난다. 게임진행 bgm변경

        done = False
        clock = pygame.time.Clock()
        fps = 25
        game = Tetris(18, 10)
        counter = 0
        pressing_down = False

        while not done:
            if game.figure is None:
                game.new_figure()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (fps // game.level // 2) == 0 or pressing_down:
                if game.state == "start":
                    game.go_down()

            if self.check_reset:
                self.aiboard.newGame()
                self.check_reset = False
                pygame.mixer.music.play(-1, 0.0)

            if self.aiboard.game_over() or game.score > (self.score + 10): #ai와 점수차이이 종
                self.screen.fill(BLACK) #게임 오버 배경 색
                pygame.mixer.music.stop() #음악 멈추기
                self.aiboard.GameOver()  #게임 오버 보드 불러오기
                self.HighScore()          #하이스코어 표기
                self.check_reset = True
                self.aiboard.init_aiboard()
                game.score =0

            for event in pygame.event.get(): #게임진행중 - event는 키보드 누를떄 특정 동작 수할떄 발생
                if event.type == QUIT: #종류 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종
                    sys.exit() #게임을 종료한다ㅏ.
                elif event.type == KEYUP and event.key == K_p: # 일시 정지 버튼 누르면
                    self.screen.fill(BLACK)         #일시 정지 화면
                    pygame.mixer.music.stop()       #일시 정지 노래 중지
                    self.aiboard.pause()
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN: #키보드를 누르면
                    self.handle_key(event.key) #handle 메소드 실행
                elif event.type == pygame.USEREVENT:
                    self.aiboard.drop_piece()

            for event in list(pygame.event.get()) + tetris_ai.run_ai(game.field, game.figure, game.width, game.height):
                if event.type == pygame.QUIT:
                   done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                    if event.key == pygame.K_ESCAPE:
                        game.__init__(20, 10)





            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(self.screen, BLACK,
                                     [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(self.screen, colors[game.field[i][j]],
                                         [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                          game.zoom - 1])

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(self.screen, colors[game.figure.color],
                                             [game.x + game.zoom * (j + game.figure.x) + 1,
                                              game.y + game.zoom * (i + game.figure.y) + 1,
                                              game.zoom - 2, game.zoom - 2])



            text = pygame.font.Font('assets/Roboto-Bold.ttf', 18).render("SCORE",True, BLACK)
            scoretext = pygame.font.Font('assets/Roboto-Bold.ttf', 16).render(""+ str(game.score), True, BLACK)

            self.screen.blit(text, [605, 200])
            self.screen.blit(scoretext, [605, 225])


            pygame.display.flip()

            # self.screen.fill(BLACK)
            self.aiboard.draw()

            self.clock.tick(fps) # 초당 프레임 관련

if __name__ == "__main__":
    Tetris(18,20).run()

