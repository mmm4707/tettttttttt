import pygame
from variable import Var
import pygame_menu
from Tetris import *
from Database import *
import time
class Menu:

    def __init__(self):
        print('test')
        pygame.init()
        Var.infoObject = pygame.display.Info()
        print(Var.infoObject.current_w, Var.infoObject.current_h)
        self.w=Var.menu_display_w
        self.h=Var.menu_display_h
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.database = Database()
        self.Mode = Var.initial_mode
        self.id=Var.initial_id
        self.score=Var.initial_score
        self.tetris=Tetris()
        self.page='page0'  # 페이지 순서
        self.size=Var.size
        self.size2=Var.size2
        self.margin=Var.margin
        self.margin2=Var.margin2
        self.margin3=Var.margin3
        self.margin4=Var.margin4
        self.margin_help=Var.margin_help
        self.margin_rank=Var.margin_rank
        self.page=Var.initial_page
        self.mytheme=Var.mytheme
        self.mytheme2=Var.mytheme_help
        self.menu = pygame_menu.Menu(self.h,self.w, '', theme=self.mytheme)



    def run(self):
        print('test2')
        self.page=Var.initial_page
        self.menu.clear()
        self.mytheme.widget_margin=self.margin3
        self.menu.add_vertical_margin(self.margin)
        self.menu.add_button('   Select mode   ', self.show_game,font_size=self.size)
        self.menu.add_button('    Show Rank    ', self.show_rank,font_size=self.size)
        self.menu.add_button('  Help  ', self.help,font_size=self.size)
        self.menu.add_button('        Quit         ', pygame_menu.events.EXIT,font_size=self.size)


    def reset(self):  ## 뒤로 갈때 보여줄 목록들
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.menu = pygame_menu.Menu(self.h, self.w, '', theme=self.mytheme)
        self.page='page0'
        self.mytheme.widget_margin=self.margin3
        Var.click.play()
        self.page=Var.initial_page
        self.menu.clear()
        self.menu.add_vertical_margin(self.margin)
        self.menu.add_button('   Select mode   ', self.show_game,font_size=self.size)
        self.menu.add_button('    Show Rank    ', self.show_rank,font_size=self.size)
        self.menu.add_button('  Help  ', self.help,font_size=self.size)
        self.menu.add_button('        Quit         ', pygame_menu.events.EXIT,font_size=self.size)

    def help(self):
        self.page='page7'
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.menu = pygame_menu.Menu(self.h, self.w, '', theme=self.mytheme2)
        self.menu.add_vertical_margin(self.margin_help)
        self.menu.add_button(' back ', self.reset,font_size=self.size2)



    def show_game(self):  ## 게임 목록 들어가면 나오는 목록들
        self.page='page1'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.margin2
        self.menu.add_vertical_margin(self.margin)
        self.menu.add_label("    --Start game--    ",max_char=0,selectable=False,font_size=self.size)
        self.menu.add_vertical_margin(15)
        self.menu.add_button('      Single mode      ', self.start_the_game,font_size=self.size)
        self.menu.add_button('       MiNi mode       ', self.start_the_Mini,font_size=self.size)
        self.menu.add_button('    Twohands mode   ', self.start_the_Twohands,font_size=self.size)
        self.menu.add_button('         Ai mode         ', self.start_the_Ai,font_size=self.size)
        self.menu.add_button('           back            ', self.reset,font_size=self.size)

    def show_rank(self):  ## 랭크 들어가면 나오는 목록들기
        self.page='page2'
        self.mytheme.widget_margin=self.margin2
        Var.click.play()
        self.menu.clear()
        self.menu.add_vertical_margin(self.margin)
        self.menu.add_label("     --Show Rank--     ", max_char=0, selectable=False,font_size=self.size)
        self.menu.add_vertical_margin(15)
        self.menu.add_button('      Single mode      ', self.Single_the_rank,font_size=self.size)
        self.menu.add_button('    Twohands mode   ', self.Twohands_the_rank,font_size=self.size)
        self.menu.add_button('       MiNi mode       ', self.Mini_the_rank,font_size=self.size)
        self.menu.add_button('           back            ', self.reset,font_size=self.size)


    def show_score(self ,game_mode,game_score):
        self.page='page6'
        self.mytheme.widget_margin=self.margin3
        self.menu.add_vertical_margin(self.margin)
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.Mode=game_mode
        self.score=game_score
        self.menu.add_button(self.Mode+' Mode', self.pass_,font_size=self.size)
        self.menu.add_text_input('ID: ', maxchar=3,onreturn=self.save_id,font_size=self.size)
        self.menu.add_button("Exit",pygame_menu.events.EXIT,font_size=self.size)

    def save_id(self ,value):
        self.id=value
        self.database.add_data(self.Mode,self.id ,self.score)
        self.reset()

    def stop(self):
        Var.click.play()
        self.menu.disable()

    def Single_the_rank(self):
        self.page='page3'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.margin4
        self.menu.add_vertical_margin(self.margin)
        self.menu.add_label("--Single Rank--", selectable=False, size=self.size)
        self.menu.add_vertical_margin(self.margin_rank)
        self.menu.add_button("       ID       Score", self.Mini_the_rank,font_size=self.size2)
        original_data = self.database.load_data("basic")
        for i in range(Var.rank_max) :
            original_name=str(original_data[i]['ID'])
            original_score = '{0:>05s}'.format(str(original_data[i]['score']))
            r= "#{} : ".format(i+1) + original_name+"    "+ original_score
            self.menu.add_button(r, self.pass_,font_size=self.size2)
        self.menu.add_button('back', self.reset,font_size=self.size2)


    def Twohands_the_rank(self):
        self.page='page4'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.margin4
        self.menu.add_vertical_margin(self.margin)
        twohadns_data = self.database.load_data("two")
        self.menu.add_label("--Two Rank--",  selectable=False, size=self.size)
        self.menu.add_vertical_margin(self.margin_rank)
        self.menu.add_button("       ID       Score", self.pass_,font_size=self.size2)
        for i in range(Var.rank_max):
            original_name = str(twohadns_data[i]['ID'])
            original_score = '{0:>05s}'.format(str(twohadns_data[i]['score']))
            r = "#{} : ".format(i+1) + original_name + "    " + original_score
            self.menu.add_button(r, self.pass_, font_size=self.size2)
        self.menu.add_button('back', self.reset,font_size=self.size2)

    def Mini_the_rank(self):
        self.page='page5'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.margin4
        mini_data = self.database.load_data("mini")
        self.menu.add_vertical_margin(self.margin)
        self.menu.add_label("--Mini Rank--", selectable=False, size=self.size)
        self.menu.add_vertical_margin(10)
        self.menu.add_button("       ID       Score", self.pass_,font_size=self.size2)
        for i in range(Var.rank_max):
            original_name = str(mini_data[i]['ID'])
            original_score = '{0:>05s}'.format(str(mini_data[i]['score']))
            r = "#{} : ".format(i+1) + original_name + "    " + original_score
            self.menu.add_button(r, self.pass_, font_size=self.size2)
        self.menu.add_button('back', self.reset,font_size=self.size2)

    def start_the_game(self):
        Var.click.play()
        self.Mode = 'basic'
        self.tetris.mode = 'basic'
        if __name__ == "__main__":
            self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)

    def start_the_Mini(self):
        Var.click.play()
        self.Mode = 'mini'
        self.tetris.mode='mini'
        if __name__ == "__main__":
            self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)

    def start_the_Twohands(self):
        Var.click.play()
        self.Mode = 'two'
        self.tetris.mode='two'
        if __name__ == "__main__":
            self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)



    def start_the_Ai(self):
        Var.click.play()
        self.Mode = 'ai'
        self.tetris.mode='ai'
        if __name__ == '__main__':
            self.tetris.run()
        self.reset()

    def pass_(self):
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
            if event.w < Var.min_display_w:
                mymenu.w = Var.min_display_w
            if event.h < Var.min_display_h:
                mymenu.h = Var.min_display_h
            mymenu.surface = pygame.display.set_mode((mymenu.w, mymenu.h), RESIZABLE)
            mymenu.menu = pygame_menu.Menu(mymenu.h, mymenu.w, '', theme=Var.mytheme)
            mymenu.menu.draw(mymenu.surface)
            mymenu.size=int((mymenu.h)/Var.font_rate1)
            mymenu.size2=int((mymenu.h)/Var.font_rate2)
            mymenu.margin=int((mymenu.h)/Var.margin_rate1)
            mymenu.margin2=(0,int((mymenu.h)/Var.margin_rate2))
            mymenu.margin3=(0,int((mymenu.h)/Var.margin_rate3))
            mymenu.margin4=(0,int((mymenu.h)/Var.margin_rate4))
            mymenu.margin_help = int((mymenu.h)/Var.margin_rate6)
            time.sleep(0.3)
            print(mymenu.w)
            print(mymenu.h)
            if mymenu.page=='page0':
                mymenu.run()
            elif mymenu.page=='page1':
                mymenu.show_game()
            elif mymenu.page=='page2':
                mymenu.show_rank()
            elif mymenu.page=='page3':
                mymenu.Single_the_rank()
            elif mymenu.page=='page4':
                mymenu.Twohands_the_rank()
            elif mymenu.page=='page5':
                mymenu.Mini_the_rank()
            elif mymenu.page=='page6':
                mymenu.show_score(mymenu.Mode,mymenu.tetris.Score)
            elif mymenu.page=='page7':
                mymenu.help()
    if mymenu.menu.is_enabled():
        mymenu.menu.update(events)
        mymenu.menu.draw(mymenu.surface)
    pygame.display.update()
