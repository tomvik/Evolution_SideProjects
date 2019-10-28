import pygame
import random
from typing import List

import Color
import Rectangle
import Character
import Stage
import Food
import Engine

pygame.init()

delay_ms = 100
win_heigth = 700
win_width = 1200
win_title = "First game"
win_life = True

stage_width = 1000
stage_height = 500

number_of_characters = 20
number_of_foods = 20

characters = list()
foods = list()

color_1 = Color.RBGColor(255, 0, 0)
color_2 = Color.RBGColor(0, 0, 255)
food_color = Color.RBGColor(255, 255, 255)
stage_color = Color.RBGColor(211, 211, 211)
walls_color = Color.RBGColor(0, 255, 0)

win = pygame.display.set_mode((win_width, win_heigth))
pygame.display.set_caption(win_title)

stage = Stage.Stage(stage_width, stage_height, stage_color, walls_color, win)

characters = Engine.span_random_characters(20, stage.get_stage(), 10, 15,
                                           color_1, stage_color, win)

foods = Engine.span_random_foods(20, stage.get_stage(), 5, 5, food_color,
                                 stage_color, win, 1, characters)

while win_life:
    # Use actual timer later on
    pygame.time.delay(delay_ms)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False

    Engine.move_characters(number_of_characters, characters, foods,
                           stage.get_walls())

'''
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        characters[0].move(0, -vel, blocking_rects[1:])
    elif keys[pygame.K_RIGHT]:
        characters[0].move(vel, 0, blocking_rects[1:])
    elif keys[pygame.K_DOWN]:
        characters[0].move(0, vel, blocking_rects[1:])
    elif keys[pygame.K_LEFT]:
        characters[0].move(-vel, 0, blocking_rects[1:])
'''


pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
