import pygame

class Sound:
    pygame.mixer.init()

    menu_bgm = pygame.mixer.Sound('assets/sounds/menu_sound.wav')
    menu_bgm.set_volume(0.1)

    ai_bgm = pygame.mixer.Sound('assets/sounds/ai_sound.wav')
    ai_bgm.set_volume(0.1)

    base_bgm = pygame.mixer.Sound('assets/sounds/base_sound.wav')
    base_bgm.set_volume(0.1)



    block_fall = pygame.mixer.Sound('assets/sounds/block_fall.wav')
    block_fall.set_volume(0.1)

    click = pygame.mixer.Sound('assets/sounds/click.wav')
    click.set_volume(1)

    game_over = pygame.mixer.Sound('assets/sounds/game_over.wav')
    game_over.set_volume(0.2)

    line_clear = pygame.mixer.Sound('assets/sounds/Line_Clear.wav')
    line_clear.set_volume(0.2)

    level_up = pygame.mixer.Sound('assets/sounds/level_up.wav')
    level_up.set_volume(0.2)
