import pygame

import pygame_menu

import sys


class Menu:

    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((800, 600))

        self.menu = pygame_menu.Menu(600, 400, 'Yami Tetris', theme=pygame_menu.themes.THEME_BLUE)

        self.Mode = 0

    def run(self):
        self.menu.add_button('Select mode', self.show_game)

        self.menu.add_button('Show Rank', self.show_game)

        self.menu.add_button('Quit', pygame_menu.events.EXIT)

        self.menu.mainloop(self.surface)

    def reset(self):  ## 뒤로 갈때 보여줄 목록들

        self.menu.clear()

        self.menu.add_button('Select mode', self.show_game)

        self.menu.add_button('Show Rank', self.show_rank)

        self.menu.add_button('Quit', pygame_menu.events.EXIT)

    def show_game(self):  ## 게임 목록 들어가면 나오는 목록들

        self.menu.clear()

        self.menu.add_button('Single mode', self.start_the_game)

        self.menu.add_button('MiNi mode', self.start_the_Mini)

        self.menu.add_button('Twohands mode', self.start_the_Twohands)

        self.menu.add_button('Ai mode', self.start_the_Ai)

        self.menu.add_button('back', self.reset)

    def show_rank(self):  ## 랭크 들어가면 나오는 목록들기

        self.menu.clear()

        self.menu.add_button('Single mode', self.show_the_rank)

        self.menu.add_button('MiNi mode', self.show_the_rank)

        self.menu.add_button('Twohands mode', self.show_the_rank)

        self.menu.add_button('Ai mode', self.show_the_rank)

        self.menu.add_button('back', self.reset)

    def show_the_rank(self):
        # 랭크 제도 만들면 여기다 넣으면 됩니다.

        pass

    def start_the_game(self):
        self.Mode = 1

        self.menu.disable()

    def start_the_Mini(self):
        self.Mode = 2

        self.menu.disable()

    def start_the_Twohands(self):
        self.Mode = 3

        self.menu.disable()

    def start_the_Ai(self):
        self.Mode = 4

        self.menu.disable()

    def show_the_rank(self):
        ## 일반게임 랭크 보여주기

        pass

    def show_the_Mini(self):
        ## 미니 게임 랭크 보여주기

        pass

    def show_the_Twohands(self):
        ## 투핸드 모드 랭크 보여주기

        pass

    def show_the_Ai(self):
        ## ai 모드 랭크 보여주

        pass