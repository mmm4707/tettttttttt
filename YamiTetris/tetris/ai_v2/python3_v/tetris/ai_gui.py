import pygame

# The configuration


ai_cell_size =    25     #게임의 셀 크기 조정
ai_cols =        10      #게임 보드의 열 개수 지정
ai_rows =        18      #게임 보드의 행 개수 조절
#maxfps =     30
ai_time =     50         # ai속도 조절  (ai_time ms에 몇번의 이벤트가 실행 될지를 결정 해준다.)
spare_space = 6



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

        #pygame 초기화
        pygame.init()

        #pygame.key.set_repeat(250,25) 키보드 누를때 지연 시간 설정

        # 게임 전체 화면 크기 지정에 사용 예정
        self.ai_width = ai_cell_size*(ai_cols+6)  # ai_width = 셀의크기(25) *(열개수 +6) - 옆에 예비 공간 만들어 줄려고
        self.ai_height = ai_cell_size*ai_rows        #ai_height = 셀의 크기 * 행의 개수

        # 행(18)과 열(10) 을 2로 나눈 너머지가 같을때는 8을 반화, 아니면 0을 반환   [[8,0,8,0,8,0 ... ], [0,8,0,8..]..]
        #self.ai_bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(ai_cols)] for y in range(ai_rows)]

        #게임 스크린 사이즈
        self.ai_screen = pygame.display.set_mode((700, 450))

        #게임 속도 조절
        #주어진 시간 (밀리 초)마다 이벤트 큐에 표시 할 이벤트 유형을 설정합니다.
        #USEREVENT = 사용자가 임의로 설정하는 이벤트   옆에 +1 은 뭐지..
        pygame.time.set_timer(pygame.USEREVENT+1, ai_time)

    #매트릭스 모양 그려주기   offset = 내가 그릴 매트릭스 시작 지점 좌표
    def ai_draw_matrix(self, matrix, ai_offset):
        off_x, off_y  = ai_offset   #시작점 x, y 좌표 받아 오기
        for y, row in enumerate(matrix):  # 행렬의 행과 행의 번호 받아오기
            for x, val in enumerate(row):  # 각 열에 대한 값을 받아오기  x는 열의 번호, val에는 구분 값(색 지정에 사용)
                if val: # 0이 아닌경우에는
                    #지정한 screen에, color 리스트에서 해당하는 색으로 만들어 주기 ###############
                    pygame.draw.rect(self.ai_screen,colors[val]
                                     , pygame.Rect(
                                     (off_x+x*ai_cell_size , (off_y+y) *ai_cell_size,  ai_cell_size,  ai_cell_size)
                                      ) ,0)

    #테트리스 화면 업데이트
    def update(self, tetris): #테트리스 생성한 객체 맞아오기
        self.ai_screen.fill(GRAY) #내가 지정한 화면을 GRAY로 채우기(그냥 배경 화면)

        if tetris.gameover:# or self.nbPiece >= maxPiece:   게임이 종료가 된 상태라면 pass하기
            pass
           # self.center_msg("""Game Over!\nYour score: %dPress space to continue""" % tetris.score)
        else: #게임이 진행중 이라면
             pygame.draw.rect(self.ai_screen, WHITE, pygame.Rect(600, 0, 450, 450))  #게임 화면에 하얀색으로 네모 그려주기
             ai_score_text = pygame.font.Font('../../../assets/Roboto-Bold.ttf', 18).render('SCORE', True, BLACK)  #점수 글씨
             ai_score_value = pygame.font.Font('../../../assets/Roboto-Bold.ttf', 16).render(str(tetris.ai_score), True, BLACK) # ai의 점수 표시해주기
             self.ai_screen.blit(ai_score_text, (605, 180))   # 정해둔 값을 화면에 올리기
             self.ai_screen.blit(ai_score_value, (605, 200))

          #   self.ai_draw_matrix(self.ai_bground_grid, (0,0))   #(0,0) 부터 내가 설정한 격자 그려주기
             self.ai_draw_matrix(tetris.ai_board, (0,0)) # (0.0) 부터  보드 업데이트 해주기 ####################################### 블럭이 쌓이는 위치 알려줌
             self.ai_draw_matrix(tetris.stone, (tetris.stone_x, tetris.stone_y)) #테트리스 블럭을 그려준다. 블럭의 왼쪽 끝 좌표부터 - 시작 블럭

             computer_said1 = pygame.font.Font('../../../assets/Roboto-Bold.ttf', 16).render("YOU CAN'T", True, BLACK)
             computer_said2 = pygame.font.Font('../../../assets/Roboto-Bold.ttf', 16).render("DEFEAT ME", True, BLACK)

             self.ai_screen.blit(computer_said1, (605, 20))
             self.ai_screen.blit(computer_said2, (605, 40))

             # 배경에 라인 추가 하기 -> 테트리스 보드 칸을 나눠주는 선 만들기
             for i in range(ai_cols + 1):
                 pygame.draw.line(self.ai_screen, (0, 0, 0), ((ai_cell_size) * i, 0), ((ai_cell_size) * i, self.ai_height - 1),2)

             for j in range(ai_rows + 1):
                 pygame.draw.line(self.ai_screen, (0, 0, 0), (0, (ai_cell_size) * j),
                                     (ai_cell_size * ai_cols - 1, (ai_cell_size) * j), 2)
        #내가 위에서 설정해 준 것들 업데이트 해주기
        pygame.display.update()

