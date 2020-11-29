import pygame
import pygame_menu
from Menu import *
from Tetris import *

import sys

running=True
while running:
    menu = Menu()
    menu.run()
    tetris=Tetris()
    print('ok? ')
    if menu.Mode == 'basic':
        tetris.mode='basic'
        if __name__ == "__main__":
            tetris.run()

    if menu.Mode == 'mini':
        tetris.mode='mini'
        if __name__ == "__main__":
            tetris.run()
    if menu.Mode == 'two':
        tetris.mode='two'
        if __name__ == "__main__":
            tetris.run()

    if menu.Mode == 'ai':
        tetris.mode='ai'
        if __name__ == '__main__':
            tetris.run()
