import pygame, sys, time
from pygame.locals import *
from Board import *


#            R    G    B
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

class Tetris:

    #생성자
    def __init__(self):
        self.screen = pygame.display.set_mode((350, 450)) # 고정 크기의 창을 만들어준다.
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.music_on_off = True
        self.check_reset = True

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
            f = open('assets/save.txt', 'r')
            l = f.read()
            f.close()
            if int(l) < self.board.score:
                h_s = self.board.score
                f = open('assets/save.txt', 'w')
                f.write(str(self.board.score))
                f.close()
            else:
                h_s = l
            self.board.HS(str(h_s))
        except:
            f = open('assets/save.txt', 'w')
            f.write(str(self.board.score))
            f.close()
            self.board.HS(str(self.board.score))

    #실행하기
    def run(self):
        pygame.init()
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')

        self.board.level_speed() #추가 - level1에서 속도

        start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        start_sound.play()
        #bgm = pygame.mixer.music.load('assets/sounds/bensound-ukulele.mp3')  # (기존 파일은 소리가 안남) 다른 mp3 파일은 소리 난다. 게임진행 bgm변경
        while True:

            if self.check_reset:
                self.board.newGame()
                self.check_reset = False
                #pygame.mixer.music.play(-1, 0.0)  ## 수정 필요 오류 나서 일단 빼둠

            if self.board.game_over():
                self.screen.fill(BLACK) #게임 오버 배경 색
                #pygame.mixer.music.stop() #음악 멈추기     오류나서 일단 뺴
                self.board.GameOver()  #게임 오버 보드 불러오기
                self.HighScore()          #하이스코어 표기
                self.check_reset = True
                self.board.init_board()
            for event in pygame.event.get(): #게임진행중 - event는 키보드 누를떄 특정 동작 수할떄 발생
                if event.type == QUIT: #종류 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종
                    sys.exit() #게임을 종료한다ㅏ.
                elif event.type == KEYUP and event.key == K_p: # 일시 정지 버튼 누르면
                    self.screen.fill(BLACK)         #일시 정지 화면
                    pygame.mixer.music.stop()       #일시 정지 노래 중둠    오류나서 일단 뺴
                    self.board.pause()
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN: #키보드를 누르면
                    self.handle_key(event.key) #handle 메소드 실행
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece()

            # self.screen.fill(BLACK)
            self.board.draw()
            pygame.display.update() #이게 나오면 구현 시
            self.clock.tick(30) # 초당 프레임 관련
