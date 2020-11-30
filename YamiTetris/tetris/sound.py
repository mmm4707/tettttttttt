import pygame

class Sound:
    pygame.mixer.init()
    #pygame.mixer.music.load('assets/sounds/menu_sound.wav')

    #pygame.mixer.music.load('assets/sounds/ai_sound.wav')


    menu_bgm = pygame.mixer.Sound('assets/sounds/menu_sound.wav')
    ai_bgm = pygame.mixer.Sound('assets/sounds/ai_sound.wav')
    base_bgm = pygame.mixer.Sound('assets/sounds/base_sound.wav')



    block_fall = pygame.mixer.Sound('assets/sounds/block_fall.wav')
    click = pygame.mixer.Sound('assets/sounds/click.wav')
    game_over = pygame.mixer.Sound('assets/sounds/game_over.wav')
    line_clear = pygame.mixer.Sound('assets/sounds/Line_Clear.wav')
    level_up = pygame.mixer.Sound('assets/sounds/level_up.wav')
