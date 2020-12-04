import pygame
from sound import Sound
import pygame_menu
from Tetris import *
from Database import *

class Menu:

    def __init__(self):
        print('test')
        pygame.init()
        self.w=600
        self.h=600
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.menu = pygame_menu.Menu(self.h,self.w, 'Yami Tetris', theme=pygame_menu.themes.THEME_BLUE)
        self.database = Database()
        self.Mode = 0
        self.id=0
        self.mode='origin'
        self.score=0
        self.tetris=Tetris()
        self.page=0
        self.fontsize=int((self.w+self.h)/40)

    def back(self):
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.menu = pygame_menu.Menu(self.h,self.w, 'Yami Tetris', theme=pygame_menu.themes.THEME_BLUE)
        self.menu.draw(self.surface)

    def run(self):
        print('test2')
        self.page=0
        self.menu.clear()
        self.menu.add_button('Select mode', self.show_game,font_size=self.fontsize)
        self.menu.add_button('Show Rank', self.show_rank,font_size=self.fontsize)
        self.menu.add_button('Quit', pygame_menu.events.EXIT,font_size=self.fontsize)

    def reset(self):  ## 뒤로 갈때 보여줄 목록들
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.menu = pygame_menu.Menu(self.h, self.w, 'Yami Tetris', theme=pygame_menu.themes.THEME_BLUE)
        Sound.click.play()
        self.page=0

        self.menu.clear()

        print('tset5')

        self.menu.add_button('Select mode', self.show_game,font_size=self.fontsize)

        self.menu.add_button('Show Rank', self.show_rank,font_size=self.fontsize)

        self.menu.add_button('Quit', pygame_menu.events.EXIT,font_size=self.fontsize)


    def show_game(self):  ## 게임 목록 들어가면 나오는 목록들
        self.page=1
        Sound.click.play()

        self.menu.clear()

        self.menu.add_label("--Show game--",max_char=0,selectable=False,font_size=self.fontsize)

        self.menu.add_vertical_margin(self.fontsize)

        self.menu.add_button('Single mode', self.start_the_game,font_size=self.fontsize)

        self.menu.add_button('MiNi mode', self.start_the_Mini,font_size=self.fontsize)

        self.menu.add_button('Twohands mode', self.start_the_Twohands,font_size=self.fontsize)

        self.menu.add_button('Ai mode', self.start_the_Ai,font_size=self.fontsize)

        self.menu.add_button('back', self.reset,font_size=self.fontsize)

    def show_rank(self):  ## 랭크 들어가면 나오는 목록들기
        self.page=2
        Sound.click.play()

        self.menu.clear()

        self.menu.add_label("--Show Rank--", max_char=0, selectable=False,font_size=self.fontsize)

        self.menu.add_vertical_margin(30)

        self.menu.add_button('Single mode', self.Single_the_rank,font_size=self.fontsize)

        self.menu.add_button('Twohands mode', self.Twohands_the_rank,font_size=self.fontsize)

        self.menu.add_button('MiNi mode', self.Mini_the_rank,font_size=self.fontsize)

        self.menu.add_button('back', self.reset,font_size=self.fontsize)


    def show_score(self ,game_mode,game_score):
        self.page=6
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.mode=game_mode
        self.score=game_score
        self.menu.add_button(self.mode+' Mode', self.show_the_rank,font_size=self.fontsize)
        self.menu.add_text_input('ID: ', maxchar=3,onreturn=self.save_id,font_size=self.fontsize)
        self.menu.add_button("Exit",pygame_menu.events.EXIT,align=pygame_menu.locals.ALIGN_RIGHT,font_size=self.fontsize)

    def save_id(self ,value):
        self.id=value
        self.database.add_data(self.mode,self.id ,self.score)
        self.reset()

    def stop(self):
        Sound.click.play()
        self.menu.disable()


    def Single_the_rank(self):
        self.page=3
        Sound.click.play()
        self.menu.clear()
        self.menu.add_label("--Single Rank--", max_char=0, selectable=False, fontsize=20)

        self.menu.add_vertical_margin(30)
        original_data = self.database.load_data("basic")
        original_1_name = str(original_data[0]['ID'])
        original_1_score ='{0:>05s}'.format(str(original_data[0]['score']))
        original_2_name = str(original_data[1]['ID'])
        original_2_score = '{0:>05s}'.format(str(original_data[1]['score']))
        original_3_name = str(original_data[2]['ID'])
        original_3_score ='{0:>05s}'.format(str(original_data[2]['score']))
        original_4_name = str(original_data[3]['ID'])
        original_4_score = '{0:>05s}'.format(str(original_data[3]['score']))
        original_5_name = str(original_data[4]['ID'])
        original_5_score = '{0:>05s}'.format(str(original_data[4]['score']))
        r1="#1 : "+original_1_name+"    "+ original_1_score
        r2="#2 : "+original_2_name+"    "+ original_2_score
        r3="#3 : "+original_3_name+"    "+ original_3_score
        r4="#4 : "+original_4_name+"    "+ original_4_score
        r5="#5 : "+original_5_name+"    "+ original_5_score
        self.menu.add_button("       ID       Score", self.Mini_the_rank)
        self.menu.add_button(r1, self.Mini_the_rank,font_size=self.fontsize)
        self.menu.add_button(r2, self.Mini_the_rank,font_size=self.fontsize)
        self.menu.add_button(r3, self.Mini_the_rank,font_size=self.fontsize)
        self.menu.add_button(r4, self.Mini_the_rank,font_size=self.fontsize)
        self.menu.add_button(r5, self.Mini_the_rank,font_size=self.fontsize)
        self.menu.add_button('back', self.reset,font_size=self.fontsize)


    def Twohands_the_rank(self):
        self.page=4
        Sound.click.play()
        self.menu.clear()
        self.menu.add_label("--Two Rank--", max_char=0, selectable=False, fontsize=20)

        self.menu.add_vertical_margin(30)
        twohands_data = self.database.load_data("two")
        original_1_name = str(twohands_data[0]['ID'])
        original_1_score ='{0:>05s}'.format(str(twohands_data[0]['score']))
        original_2_name = str(twohands_data[1]['ID'])
        original_2_score = '{0:>05s}'.format(str(twohands_data[1]['score']))
        original_3_name = str(twohands_data[2]['ID'])
        original_3_score ='{0:>05s}'.format(str(twohands_data[2]['score']))
        original_4_name = str(twohands_data[3]['ID'])
        original_4_score = '{0:>05s}'.format(str(twohands_data[3]['score']))
        original_5_name = str(twohands_data[4]['ID'])
        original_5_score = '{0:>05s}'.format(str(twohands_data[4]['score']))
        r1="#1 : "+original_1_name+"    "+ original_1_score
        r2="#2 : "+original_2_name+"    "+ original_2_score
        r3="#3 : "+original_3_name+"    "+ original_3_score
        r4="#4 : "+original_4_name+"    "+ original_4_score
        r5="#5 : "+original_5_name+"    "+ original_5_score
        self.menu.add_button("       ID       Score", self.show_the_Twohands)
        self.menu.add_button(r1, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r2, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r3, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r4, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r5, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button('back', self.reset,font_size=self.fontsize)

    def Mini_the_rank(self):
        self.page=5
        Sound.click.play()
        self.menu.clear()
        self.menu.add_label("--Mini Rank--", max_char=0, selectable=False, fontsize=20)

        self.menu.add_vertical_margin(30)
        mini_data = self.database.load_data("mini")
        original_1_name = str(mini_data[0]['ID'])
        original_1_score ='{0:>05s}'.format(str(mini_data[0]['score']))
        original_2_name = str(mini_data[1]['ID'])
        original_2_score = '{0:>05s}'.format(str(mini_data[1]['score']))
        original_3_name = str(mini_data[2]['ID'])
        original_3_score ='{0:>05s}'.format(str(mini_data[2]['score']))
        original_4_name = str(mini_data[3]['ID'])
        original_4_score = '{0:>05s}'.format(str(mini_data[3]['score']))
        original_5_name = str(mini_data[4]['ID'])
        original_5_score = '{0:>05s}'.format(str(mini_data[4]['score']))
        r1="#1 : "+original_1_name+"    "+ original_1_score
        r2="#2 : "+original_2_name+"    "+ original_2_score
        r3="#3 : "+original_3_name+"    "+ original_3_score
        r4="#4 : "+original_4_name+"    "+ original_4_score
        r5="#5 : "+original_5_name+"    "+ original_5_score
        self.menu.add_button("       ID       Score", self.show_the_Twohands)
        self.menu.add_button(r1, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r2, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r3, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r4, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button(r5, self.show_the_Twohands,font_size=self.fontsize)
        self.menu.add_button('back', self.reset)


    def start_the_game(self):
        Sound.click.play()

        self.Mode = 'basic'
        self.tetris.mode = 'basic'
        if __name__ == "__main__":
            self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)

    def start_the_Mini(self):
        Sound.click.play()

        self.Mode = 'mini'
        self.tetris.mode='mini'
        if __name__ == "__main__":
            self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)


    def start_the_Twohands(self):
        Sound.click.play()

        self.Mode = 'two'
        self.tetris.mode='two'
        if __name__ == "__main__":
            self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)



    def start_the_Ai(self):
        Sound.click.play()

        self.Mode = 'ai'
        self.tetris.mode='ai'
        if __name__ == '__main__':
            self.tetris.run()
        self.reset()


    def show_the_rank(self):
        ## 일반게임 랭크 보여주기

        pass

    def show_the_Mini(self):
        ## 미니 게임 랭크 보여주기

        pass

    def show_the_Twohands(self):
        ## 투핸드 모드 랭크 보여주기

        pass


mymenu=Menu()
mymenu.run()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        elif event.type == VIDEORESIZE:
            mymenu.w=event.w
            mymenu.h=event.h
            mymenu.fontsize=int((mymenu.w+mymenu.h)/40)
            print(mymenu.w)
            print(mymenu.h)
            mymenu.back()
            if mymenu.page==0:
                mymenu.run()
            elif mymenu.page==1:
                mymenu.show_game()
            elif mymenu.page==2:
                mymenu.show_rank()
            elif mymenu.page==3:
                mymenu.Single_the_rank()
            elif mymenu.page==4:
                mymenu.Twohands_the_rank()
            elif mymenu.page==5:
                mymenu.Mini_the_rank()
            elif mymenu.page==6:
                mymenu.show_score(mymenu.mode,mymenu.score)

    if mymenu.menu.is_enabled():
        mymenu.menu.update(events)
        mymenu.menu.draw(mymenu.surface)
    pygame.display.update()