from Database import Database
import pygame
import sys
import pygame, sys, time
from pygame.locals import *



database = Database()
print(database.load_data("original"))

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



class Rank():
    def __init__(self):

        self.width = 10  # 맵의 좌에서 우로 사이즈
        self.height = 18  # 맵 위에서 아래로 사이즈
        self.block_size = 25   # 바꾸면 맵 블럭크기 변경

        self.database = Database()

        self.display_width = (self.width + 4) * self.block_size
        self.display_height = self.height * self.block_size
        self.screen = pygame.display.set_mode((self.display_width*2, self.display_height))

        self.font_size_small = 14
        self.font_size_middle = 16
        self.font_size_big = 18


    # 가장 높은 점수 보여주기 배경
    def show_rank(self):
        pygame.init()
        fontObj1 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_big  )
        fontObj2 = pygame.font.Font('assets/Roboto-Bold.ttf', self.font_size_middle)

        Original_bar_text = fontObj1.render('Original Mode', True, GREEN)
        twohands_bar_text = fontObj1.render('TwoHands Mode', True, GREEN)
        mini_bar_text = fontObj1.render('Mini Mode', True, GREEN)

        print("1")
        original_data = self.database.load_data("original")
        print("2")
        twohands_data = self.database.load_data("twohands")
        print("3")
        mini_data = self.database.load_data("mini")
        print("4")
        print(original_data)

        original_1_name = fontObj2.render("#1    "+str(original_data[0]['ID']),True, GREEN)
        original_1_score = fontObj2.render(str(original_data[0]['score']), True, GREEN)
        original_2_name = fontObj2.render("#2    "+str(original_data[1]['ID']), True, GREEN)
        original_2_score = fontObj2.render(str(original_data[1]['score']), True, GREEN)
        original_3_name = fontObj2.render("#3    "+str(original_data[2]['ID']), True, GREEN)
        original_3_score = fontObj2.render(str(original_data[2]['score']), True, GREEN)
        original_4_name = fontObj2.render("#4    "+str(original_data[3]['ID']), True, GREEN)
        original_4_score = fontObj2.render(str(original_data[3]['score']), True, GREEN)
        original_5_name = fontObj2.render("#5    "+str(original_data[4]['ID']), True, GREEN)
        original_5_score = fontObj2.render(str(original_data[4]['score']), True, GREEN)

        twohands_1_name = fontObj2.render("#1    " + str(twohands_data[0]['ID']), True, GREEN)
        twohands_1_score = fontObj2.render(str(twohands_data[0]['score']), True, GREEN)
        twohands_2_name = fontObj2.render("#2    " + str(twohands_data[1]['ID']), True, GREEN)
        twohands_2_score = fontObj2.render(str(twohands_data[1]['score']), True, GREEN)
        twohands_3_name = fontObj2.render("#3    " + str(twohands_data[2]['ID']), True, GREEN)
        twohands_3_score = fontObj2.render(str(twohands_data[2]['score']), True, GREEN)
        twohands_4_name = fontObj2.render("#4    " + str(twohands_data[3]['ID']), True, GREEN)
        twohands_4_score = fontObj2.render(str(twohands_data[3]['score']), True, GREEN)
        twohands_5_name = fontObj2.render("#5    " + str(twohands_data[4]['ID']), True, GREEN)
        twohands_5_score = fontObj2.render(str(twohands_data[4]['score']), True, GREEN)



        mini_1_name = fontObj2.render("#1    " + str(mini_data[0]['ID']), True, GREEN)
        mini_1_score = fontObj2.render(str(mini_data[0]['score']), True, GREEN)
        mini_2_name = fontObj2.render("#2    " + str(mini_data[1]['ID']), True, GREEN)
        mini_2_score = fontObj2.render(str(mini_data[1]['score']), True, GREEN)
        mini_3_name = fontObj2.render("#3    " + str(mini_data[2]['ID']), True, GREEN)
        mini_3_score = fontObj2.render(str(mini_data[2]['score']), True, GREEN)
        mini_4_name = fontObj2.render("#4    " + str(mini_data[3]['ID']), True, GREEN)
        mini_4_score = fontObj2.render(str(mini_data[3]['score']), True, GREEN)
        mini_5_name = fontObj2.render("#5    " + str(mini_data[4]['ID']), True, GREEN)
        mini_5_score = fontObj2.render(str(mini_data[4]['score']), True, GREEN)



        self.screen.fill(BLACK)
        self.screen.blit(Original_bar_text, (self.block_size * 3, self.block_size * 2))

        self.screen.blit(original_1_name, (self.block_size * 3, self.block_size * 4))
        self.screen.blit(original_1_score, (self.block_size * 7, self.block_size * 4))
        self.screen.blit(original_2_name, (self.block_size * 3, self.block_size * 6))
        self.screen.blit(original_2_score, (self.block_size * 7, self.block_size * 6))
        self.screen.blit(original_3_name, (self.block_size * 3, self.block_size * 8))
        self.screen.blit(original_3_score, (self.block_size * 7, self.block_size * 8))
        self.screen.blit(original_4_name, (self.block_size * 3, self.block_size * 10))
        self.screen.blit(original_4_score, (self.block_size * 7, self.block_size * 10))
        self.screen.blit(original_5_name, (self.block_size * 3, self.block_size * 12))
        self.screen.blit(original_5_score, (self.block_size * 7, self.block_size * 12))


        self.screen.blit(twohands_bar_text, (self.block_size * 11.5, self.block_size * 2))
        self.screen.blit(twohands_1_name, (self.block_size * 11.5, self.block_size * 4))
        self.screen.blit(twohands_1_score, (self.block_size * 15.5, self.block_size * 4))
        self.screen.blit(twohands_2_name, (self.block_size * 11.5, self.block_size * 6))
        self.screen.blit(twohands_2_score, (self.block_size * 15.5, self.block_size * 6))
        self.screen.blit(twohands_3_name, (self.block_size * 11.5, self.block_size * 8))
        self.screen.blit(twohands_3_score, (self.block_size * 15.5, self.block_size * 8))
        self.screen.blit(twohands_4_name, (self.block_size * 11.5, self.block_size * 10))
        self.screen.blit(twohands_4_score, (self.block_size * 15.5, self.block_size * 10))
        self.screen.blit(twohands_5_name, (self.block_size * 11.5, self.block_size * 12))
        self.screen.blit(twohands_5_score, (self.block_size * 15.5, self.block_size * 12))


        self.screen.blit(mini_bar_text, (self.block_size * 20.5, self.block_size * 2))
        self.screen.blit(mini_1_name, (self.block_size * 20.5, self.block_size * 4))
        self.screen.blit(mini_1_score, (self.block_size * 24.5, self.block_size * 4))
        self.screen.blit(mini_2_name, (self.block_size * 20.5, self.block_size * 6))
        self.screen.blit(mini_2_score, (self.block_size * 24.5, self.block_size * 6))
        self.screen.blit(mini_3_name, (self.block_size * 20.5, self.block_size * 8))
        self.screen.blit(mini_3_score, (self.block_size * 24.5, self.block_size * 8))
        self.screen.blit(mini_4_name, (self.block_size * 20.5, self.block_size * 10))
        self.screen.blit(mini_4_score, (self.block_size * 24.5, self.block_size * 10))
        self.screen.blit(mini_5_name, (self.block_size * 20.5, self.block_size * 12))
        self.screen.blit(mini_5_score, (self.block_size * 24.5, self.block_size * 12))








        pygame.display.update()

    #실행하기
    def run(self):
        pygame.init()
        icon = pygame.image.load('assets/images/icon.PNG')  # png -> PNG로 수정
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Ranking')
        self.show_rank()
        pygame.display.update()

        #start_sound = pygame.mixer.Sound('assets/sounds/Start.wav')
        #start_sound.play()
        #bgm = pygame.mixer.music.load('assets/sounds/bensound-ukulele.mp3')  # (기존 파일은 소리가 안남) 다른 mp3 파일은 소리 난다. 게임진행 bgm변경

        while True:

            for event in pygame.event.get(): #게임진행중 - event는 키보드 누를떄 특정 동작 수할떄 발생
                if event.type == QUIT: #종류 이벤트가 발생한 경우
                    pygame.quit() #모든 호출 종
                    sys.exit() #게임을 종료한다ㅏ.
                #화면 크기 조절해 보기
                elif event.type == VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE )


            # self.screen.fill(BLACK)

           #이게 나오면 구현 시


if __name__ == "__main__":
    Rank().run()
