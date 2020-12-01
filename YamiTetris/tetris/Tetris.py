import pygame, sys, time
from pygame.locals import *
from Board import *
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
# 나중에 사용할 사이즈 조절용 변수임
resize = 1


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

weights = [3.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093,

           -2.9262681134021786,

           -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861,

           -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956,

           -2.684925769670947,

           -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828,

           0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105,

           -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306,

           17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875]  # 21755 lignes


class Tetris:

    #생성자
    def __init__(self):
        self.mode = 'basic'
        #self.width = 10  # 가로 칸수
        #self.height = 18  # 세로 칸 수
        #self.block_size = 25*resize  # 블럭 하나당 크기
        #self.display_width = (self.board.width + 4) * self.block_size
        #self.display_height = self.height * self.block_size
        self.clock = pygame.time.Clock()
        self.music_on_off = True
        self.check_reset = True
        self.Id=0
        self.Score=0
        random.seed(4)

        self.ai_speed = 180

    #각 키를 누를떄 실행되는 method
    def handle_key(self, event_key, mode):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece(mode)
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece(mode)
        elif event_key == K_q: #스킬 부분
            self.board.ultimate()
        elif event_key == K_m: # 소리 설정
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()


    def ai_new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = ai_tetris_shapes[
            random.randint(0, len(ai_tetris_shapes) - 1)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
        self.stone_x = int(self.board.width / 2 - len(self.stone[0]) / 2)  # self.width 기준 스톤의 위치 x
        self.stone_y = 0
        if self.board.ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True  # 블럭이 부딪히는 판단, 새로 생성한 블럭이 벽에 부딪히면은 게임 종료


    def ai_init_game(self):
        self.ai_board = [[0 for x in range(self.board.width)] for y in range(self.board.height)] # 새로운 게임 보드 생성
        self.ai_new_stone()  # 새로운 블럭 생성
        self.ai_score = 0  # 시작 스코어
        self.ai_lines = 0  # 지운 라인의 개수


    def ai_add_cl_lines(self, n):
        linescores = [0, 50, 100, 150, 200]
        self.ai_lines += n  # 지운 개수 추가하기
        self.ai_score += linescores[n] * self.board.level * 2  # 점수  = 원래 점수 + 한번에지운 라인개수에 해당하는 점수 * 레벨

        # 블럭을 delta_x 만큼 움직이기

    def ai_move(self, delta_x):
        if not self.gameover and not self.paused:  # 게임 종료, 정지 상태가 아니라면
            new_x = self.stone_x + delta_x  # 새로운 x 좌표는   기존의 stone의 x좌표 + 이동좌표수
            if new_x < 0:  # 새로운 좌표가 0보다 작다면
                new_x = 0  # 새로운 좌표는 0 ( 변경 없음 )
            if new_x > self.board.width - len(self.stone[0]):  # 새로운 좌표 > 열의개수(10) - 블럭의 x축 길이
                new_x = self.board.width - len(self.stone[0])  # 이동 불가 (변경 없음)
            if not self.board.ai_check_collision(self.ai_board, self.stone, (new_x, self.stone_y)):  # 벽과 부딪히지 않는 다면
                self.stone_x = new_x  # 새로운 좌표로 이동

    def ai_drop(self, manual):
        if not self.gameover and not self.paused:  # 게임 종료, 정지 상태가 아니라면
            self.ai_score += 1 if manual else 0  # 내릴 수 있다면  스코어+1, 내릴수 없다면 +0
            self.stone_y += 1  # y축 좌표 +1
            if self.board.ai_check_collision(self.ai_board, self.stone, (self.stone_x, self.stone_y)):  # 벽에 부딪히지 않는 경우에는
                self.ai_board = self.board.join_matrixes(self.ai_board, self.stone,
                                           (self.stone_x, self.stone_y))  # 새로운 보드는   블럭의 새로운 좌표를 포합한 보드로 갱신
                self.ai_score += 1 # 블럭이 밑에 내려가면 점수 추가
                self.ai_new_stone()  # 새로운 블럭 생성하기
                cleared_rows = 0  # 지운 행의 개수 초기화

                for i, row in enumerate(self.ai_board):  # 모든 행마다 검사    i는 행의 번호
                    if 0 not in row:  # 행에 빈공간이 없다면 (0은 빈공간의 의미한다.)
                        self.ai_board = self.board.ai_remove_row(self.ai_board, i)  # ai보드를 i행을 지운 보드로 업데이트
                        cleared_rows += 1  # 지운개수 +1  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                self.ai_add_cl_lines(cleared_rows)  # 한번에 지운 개수에 해당하는 만큼    지운라인개수, 점수, 레벨 변경
                return True  # 게임 종료 상태가 아니 었다면,  true 반환
        return False  # 게임이 정지, 종료 상태 였다면 false 반환

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            ai_new_stone = self.board.ai_rotate_clockwise(self.stone)
            if not self.board.ai_check_collision(self.ai_board,
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



    def handle_key2(self, event_key, mode):
        if event_key == K_s:
            self.board.drop_piece(mode)
        elif event_key == K_a:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_d:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_e:
            self.board.full_drop_piece(mode)
        if event_key == K_DOWN:
            self.board.drop_piece2()
        elif event_key == K_LEFT:
            self.board.move_piece2(dx=-1, dy=0)
        elif event_key == K_RIGHT:
            self.board.move_piece2(dx=1, dy=0)
        elif event_key == K_UP:
            self.board.rotate_piece2()
        elif event_key == K_SPACE:
            self.board.full_drop_piece2()
        elif event_key == K_m:  # 소리 설정
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()
    #실행하기
    def run(self):
        pygame.init()
        self.board = Board(self.mode)
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')
        self.board.level_speed() #추가 - level1에서 속도
        self.gameover =False # ai 관련
        self.paused= False # ai 관련
        #start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        #start_sound.play()
        #bgm = pygame.mixer.music.load('assets/sounds/bensound-ukulele.mp3')  # (기존 파일은 소리가 안남) 다른 mp3 파일은 소리 난다. 게임진행 bgm변경
        if self.mode == 'ai':
            self.next_stone = ai_tetris_shapes[
                random.randint(0, len(ai_tetris_shapes) - 1)]  # 다음 블럭 랜덤으로 고르기 0~6 사이의 랜덤 숫자를 통해 고르기
            self.ai_init_game()

        delay = 150
        interval = 100
        pygame.key.set_repeat(delay, interval)


        while True:
            if self.mode =='ai':
                Ai.choose(self.ai_board, self.stone, self.next_stone, self.stone_x, weights, self)

            if self.check_reset:

                self.check_reset = False
                #pygame.mixer.music.play(-1, 0.0)  ## 수정 필요 오류 나서 일단 빼둠

            if self.mode =='ai':
                if self.board.game_over() or self.board.score < self.ai_score:
                    pygame.quit()
                    break


            if self.board.game_over():
                self.Score=self.board.score
                self.board.show_my_score()
                Menu().show_score(self.mode,self.Score)
                print('test')
                pygame.quit()
                break



            for event in pygame.event.get():
                '''pygame.display.set_mode((wid,hei), pygame.RESIZABLE).blit(image, (wid,hei))
                pygame.display.update()
                #self.screen.blit(image, (wid, hei))
                 #게임진행중 - event는 키보드 누를떄 특정 동작 수할떄 발생
                image = pygame.Surface((wid, hei))'''

                if event.type == QUIT: #종류 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종
                    sys.exit() #게임을 종료한다ㅏ.
                elif event.type == KEYUP and event.key == K_p: # 일시 정지 버튼 누르면
                    self.screen.fill(BLACK)         #일시 정지 화면
                    #pygame.mixer.music.stop()       #일시 정지 노래 중둠    오류나서  일단 뺴
                    self.board.pause()
                    #pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN: #키보드를 누르면
                    if self.mode=='two':
                        self.handle_key2(event.key, self.mode)  # handle 메소드 실행
                    else:
                        self.handle_key(event.key, self.mode) #handle 메소드 실행
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece(self.mode)
                    if self.mode=='two':
                        self.board.drop_piece2()

                elif event.type == pygame.USEREVENT + 1:
                    if self.mode == 'ai' :
                        self.ai_drop(False)


                #화면 크기 조절해 보기
                elif event.type == VIDEORESIZE:
                    if event.h != self.board.display_height:
                        pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE)
                    resize = event.w/self.board.display_width
                    '''#self.board.display_width = int(self.board.display_width*resize)
                    wid = int(event.w)
                    hei = int(hei*resize)
                    image = pygame.transform.scale(image, (wid,hei))
                    #self.board.screen.blit(image, (int(event.w), int(event.h)))
                    pygame.display.set_mode((wid,hei), pygame.RESIZABLE)
                    pygame.display.update()'''
                    if resize> 1.001 or resize<1.0:
                        if self.mode=='mini':
                            self.board.block_size = int(self.board.block_size*resize)
                            self.board.display_width = (self.board.width + 4) * self.board.block_size
                        else:
                            self.board.block_size = int(self.board.block_size*resize)
                            self.board.display_width = (self.board.width + 4) * self.board.block_size
                        self.board.display_height = self.board.height * self.board.block_size
                        if self.mode=='two':
                            self.board.status_width = self.board.block_size * self.board.two_status_size
                        else:
                            self.board.status_width = self.board.block_size * self.board.status_size
                        pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE )
                    '''block_size = int(25*resize)
                        self.board.display_width = (self.board.width + 4) * block_size
                        print(block_size, self.board.display_width)
                    self.board.display_height = self.board.height *block_size
                    print(block_size, self.board.display_width, self.board.display_height)
                    pygame.display.set_mode((self.board.display_width, self.board.display_height), RESIZABLE )
                    print(block_size, self.board.display_width, self.board.display_height)'''
                    #pygame.display.set_mode((300, 500),pygame.RESIZABLE)
            # self.screen.fill(BLACK)
            self.board.draw(self, self.mode)
            pygame.display.update() #이게 나오면 구현 시
            self.clock.tick(30) # 초당 프레임 관련
