import pygame
import pygame_menu
from Board import *
from Tetris import *
from Twohands import *
from AITetris import AITetris


resize = 2

width = 10
height = 18
block_size = 25 * resize

display_width = (width + 4) * block_size * 2
display_height = height * block_size


pygame.init()
surface=pygame.display.set_mode((display_width,display_height))

def reset(): ## 뒤로 갈때 보여줄 목록들
    menu.clear()
    menu.add_button('Select mode',show_game)
    menu.add_button('Show Rank',show_rank)
    menu.add_button('Quit',pygame_menu.events.EXIT)

def show_game(): ## 게임 목록 들어가면 나오는 목록들
    menu.clear()
    menu.add_button('Single mode', start_the_game)
    menu.add_button('MiNi mode',start_the_Mini)
    menu.add_button('Twohands mode',start_the_Twohands)
    menu.add_button('Ai mode',start_the_Ai)
    menu.add_button('back',reset)

def show_rank():  ## 랭크 들어가면 나오는 목록들기
    menu.clear()
    menu.add_button('Single mode', show_the_rank)
    menu.add_button('MiNi mode',show_the_rank)
    menu.add_button('Twohands mode',show_the_rank)
    menu.add_button('Ai mode',show_the_rank)
    menu.add_button('back',reset)

def show_the_rank():
    #랭크 제도 만들면 여기다 넣으면 됩니다.
    pass


def start_the_game():
    if __name__ == "__main__":
        Tetris().run()


def start_the_Mini():
    ## 미니 게임 모드 만들면 여기다 실행 코드만 넣으세요
    if __name__ == "__main__":
        Mini().run()


def start_the_Twohands():
    ## 투핸드 모드 만들면 여기다 실행 코드만 넣으세요
    if __name__ == "__main__":
        Twohands().run()

def start_the_Ai():
    ## ai 모드 만들면 여기다 실행 코드 넣으세요
    weights = [3.39357083734159515, -1.8961941343266449, -5.107694873375318, -3.6314963941589093,
               -2.9262681134021786,
               -2.146136640641482, -7.204192964669836, -3.476853402227247, -6.813002842291903, 4.152001386170861,
               -21.131715861293525, -10.181622180279133, -5.351108175564556, -2.6888972099986956,
               -2.684925769670947,
               -4.504495386829769, -7.4527302422826, -6.3489634714511505, -4.701455626343827, -10.502314845278828,
               0.6969259450910086, -4.483319180395864, -2.471375907554622, -6.245643268054767, -1.899364785170105,
               -5.3416512085013395, -4.072687054171711, -5.936652569831475, -2.3140398163110643, -4.842883337741306,
               17.677262456993276, -4.42668539845469, -6.8954976464473585, 4.481308299774875]  # 21755 lignes
    if __name__ == '__main__':
         AITetris(4).run(weights)


def show_the_rank():
    ## 일반게임 랭크 보여주기
    pass

def show_the_Mini():
    ## 미니 게임 랭크 보여주기
    pass


def show_the_Twohands():
    ## 투핸드 모드 랭크 보여주기
    pass


def show_the_Ai():
    ## ai 모드 랭크 보여주
    pass


"""
## 나중에 이미지 바꿀떄
## 여기부터는 배경 이미지 및 꾸미기 등


## 바꿀 이미지 파일 관리

menu_image = pygame_menu.baseimage.BaseImage(

    image_path='images/고양이.png',

    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL

)

## 새로운 태마 만들기

mytheme = pygame_menu.themes.THEME_ORANGE.copy()

## 배경 이미지 교체

mytheme.background_color = menu_image

## 위젯 이미지 교체 .

mytheme.widget_background_color = menu_image

## 상단 바 바꾸기

mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE

## 글꼴 바꾸기

mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD

mytheme.font = pygame_menu.font.FONT_OPEN_SANS_BOLD

##  상단 바 글꼴 크기

mytheme.title_font_size = 30

# 위젯 글골 크기

mytheme.widget_font_size = 30

# 위젯 끼리 떨어져 있는 길이

mytheme.widget_margin = (0, 20)

menu = pygame_menu.Menu(600, 400, 'Yami Tetris',

                        theme=mytheme)

# 상단 메뉴바 모양 바꾸기


title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE

"""

# 이미지 삽입할떄는 이거 삭제하고 위에꺼 쓰면 됩니다. !
menu = pygame_menu.Menu(display_height,display_width,'Yami Tetris',theme=pygame_menu.themes.THEME_BLUE)

#폰트 사이즈 조정 변수 넣어주세욤

menu.add_button('Select mode' , show_game)
menu.add_button('Show Rank', show_rank)
menu.add_button('Quit',pygame_menu.events.EXIT)
menu.mainloop(surface)
