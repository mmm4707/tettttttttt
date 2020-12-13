import pygame
from variable import Var
import pygame_menu
from Tetris import *
from Database import *
import time
class Menu:

    def __init__(self):
        pygame.init()
        Var.infoObject = pygame.display.Info()
        self.tetris=Tetris()
        self.database = Database()
        self.w=Var.menu_display_w
        self.h=Var.menu_display_h
        self.Mode = Var.initial_mode
        self.id=Var.initial_id
        self.score=Var.initial_score
        self.page=Var.initial_page
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.mytheme=Var.mytheme
        self.mytheme2=Var.mytheme_help
        self.menu = pygame_menu.Menu(self.h,self.w, '', theme=self.mytheme)
        self.font_main=Var.font_main   # 메인 폰트 사이즈
        self.font_sub=Var.font_sub     # 서브 폰트 사이즈
        self.widget_margin_main=Var.widget_margin_main         #메인 위젯 사이 간격
        self.widget_margin_showpage=Var.widget_margin_showpage #show 페이지 위젯 사이 간격
        self.widget_margin_rank=Var.widget_margin_rank         #rank 페이지 위젯 사이 간격
        self.margin_main=Var.margin_main                       #메인 페이지 x,y 위젯 시작 위치
        self.margin_show=Var.margin_show                       #show 페이지 x,y 위젯 시작 위치
        self.margin_help=Var.margin_help                       #help 페이지 back 위치
        self.margin_rank=Var.margin_rank                       #rank 페이지 x,y 위젯 시작 위치


#add_button 이거는 선택하는 버튼 만들기
#clear()는 초기화하기
#add_vertical_margin 위에서 부터 간격 설정하기
#add_label 은 텍스트만 있는 것 만들기
#add_text_input 은 텍스트 입력 받아 함수 실행 가능한 것
#자세한 것은 깃허브 pygame_menu에 자세하게 나와있습니다. 참고하세요

    def run(self):   # 실행하는 함
        print('test2')
        self.page=Var.initial_page   #시작하면 기본 모드로 모드가 설정
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_main
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button('   Select mode   ', self.show_game,font_size=self.font_main)
        self.menu.add_button('    Show Rank    ', self.show_rank,font_size=self.font_main)
        self.menu.add_button('  Help  ', self.help,font_size=self.font_main)
        self.menu.add_button('        Quit         ', pygame_menu.events.EXIT,font_size=self.font_main)


    def reset(self):  ## 뒤로 갈때 보여줄 목록들
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.menu = pygame_menu.Menu(self.h, self.w, '', theme=self.mytheme)
        self.page='page0'
        self.mytheme.widget_margin=self.widget_margin_main
        Var.click.play()
        self.page=Var.initial_page
        self.menu.clear()
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button('   Select mode   ', self.show_game,font_size=self.font_main)
        self.menu.add_button('    Show Rank    ', self.show_rank,font_size=self.font_main)
        self.menu.add_button('  Help  ', self.help, font_size=self.font_main)
        self.menu.add_button('        Quit         ', pygame_menu.events.EXIT,font_size=self.font_main)

    def help(self): # help 페이
        self.page='page7'
        self.surface = pygame.display.set_mode(Var.help_screen)
        self.menu = pygame_menu.Menu(Var.help_h, Var.help_w, '', theme=self.mytheme2)
        self.menu.add_vertical_margin(self.margin_help)
        self.menu.add_button(' back ', self.reset,font_size=self.font_sub)



    def show_game(self):  ## 게임 목록 들어가면 나오는 목록들
        self.page='page1'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_showpage
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("    --Start game--    ",selectable=False,font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_show)
        self.menu.add_button('      Single mode      ', self.start_the_game,font_size=self.font_main)
        self.menu.add_button('       MiNi mode       ', self.start_the_Mini,font_size=self.font_main)
        self.menu.add_button('    Twohands mode   ', self.start_the_Twohands,font_size=self.font_main)
        self.menu.add_button('         Ai mode         ', self.start_the_Ai,font_size=self.font_main)
        self.menu.add_button('           back            ', self.reset,font_size=self.font_main)

    def show_rank(self):  ## 랭크 들어가면 나오는 목록들기
        self.page='page2'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_showpage
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("     --Show Rank--     ", max_char=0, selectable=False,font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_show)
        self.menu.add_button('      Single mode      ', self.Single_the_rank,font_size=self.font_main)
        self.menu.add_button('    Twohands mode   ', self.Twohands_the_rank,font_size=self.font_main)
        self.menu.add_button('       MiNi mode       ', self.Mini_the_rank,font_size=self.font_main)
        self.menu.add_button('           back            ', self.reset,font_size=self.font_main)


    def show_score(self ,game_mode,game_score):  # Rank 기록 하는 페이지
        self.page='page6'
        self.Mode=game_mode # 게임 모드 받아오기
        self.score=game_score  # 점수 받아오기
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.mytheme.widget_margin=self.widget_margin_main
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button(self.Mode+' Mode', self.pass_,font_size=self.font_main)
        self.menu.add_text_input('ID: ', maxchar=Var.rank_id_max,onreturn=self.save_id,font_size=self.font_main) # 아이디 적는 칸
        self.menu.add_button("Exit",pygame_menu.events.EXIT,font_size=self.font_main)

    def save_id(self ,value): #아이디 저장해서 데이터 베이스로 넘기기
        self.id=value
        self.database.add_data(self.Mode,self.id ,self.score)
        self.reset()

    def stop(self):
        Var.click.play()
        self.menu.disable()

    def Single_the_rank(self): #기본 모드 랭크 보는 화면
        self.page='page3'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_rank
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("--Single Rank--", selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_rank)
        self.menu.add_button("       ID       Score", self.Mini_the_rank,font_size=self.font_sub)
        original_data = self.database.load_data("basic") # 오리지날 모드 데이터 받아오기
        for i in range(Var.rank_max) : #최대 몇명까지 보여줄건지 설정
            original_name=str(original_data[i]['ID'])
            original_score = '{0:>05s}'.format(str(original_data[i]['score']))
            r= "#{} : ".format(i+1) + original_name+"    "+ original_score
            self.menu.add_button(r, self.pass_,font_size=self.font_sub)
        self.menu.add_button('back', self.reset,font_size=self.font_sub)


    def Twohands_the_rank(self):
        self.page='page4'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_rank
        self.menu.add_vertical_margin(self.margin_main)
        twohadns_data = self.database.load_data("two")
        self.menu.add_label("--Two Rank--",  selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_rank)
        self.menu.add_button("       ID       Score", self.pass_,font_size=self.font_sub)
        for i in range(Var.rank_max):
            original_name = str(twohadns_data[i]['ID'])
            original_score = '{0:>05s}'.format(str(twohadns_data[i]['score']))
            r = "#{} : ".format(i+1) + original_name + "    " + original_score
            self.menu.add_button(r, self.pass_, font_size=self.font_sub)
        self.menu.add_button('back', self.reset,font_size=self.font_sub)

    def Mini_the_rank(self):
        self.page='page5'
        Var.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_rank
        mini_data = self.database.load_data("mini")
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("--Mini Rank--", selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_rank)
        self.menu.add_button("       ID       Score", self.pass_,font_size=self.font_sub)
        for i in range(Var.rank_max):
            original_name = str(mini_data[i]['ID'])
            original_score = '{0:>05s}'.format(str(mini_data[i]['score']))
            r = "#{} : ".format(i+1) + original_name + "    " + original_score
            self.menu.add_button(r, self.pass_, font_size=self.font_sub)
        self.menu.add_button('back', self.reset,font_size=self.font_sub)

    def start_the_game(self): # 클릭시 게임 실행 끝나면 기록 화면 보여주기
        Var.click.play()
        self.Mode = 'basic'
        self.tetris.mode = 'basic'
        self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)

    def start_the_Mini(self):
        Var.click.play()
        self.Mode = 'mini'
        self.tetris.mode='mini'
        self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)

    def start_the_Twohands(self):
        Var.click.play()
        self.Mode = 'two'
        self.tetris.mode='two'
        self.tetris.run()
        self.menu.clear()
        self.show_score(self.Mode,self.tetris.Score)



    def start_the_Ai(self):
        Var.click.play()
        self.Mode = 'ai'
        self.tetris.mode='ai'
        self.tetris.run()
        self.reset()

    def pass_(self):
        pass
