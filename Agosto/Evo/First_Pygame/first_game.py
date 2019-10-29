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
number_of_foods = 30
sensing_range = 70

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

characters = Engine.span_random_characters(number_of_characters,
                                           stage.get_stage(), 10, 15,
                                           color_1, stage_color, win, 5,
                                           sensing_range)

foods = Engine.span_random_foods(number_of_foods, stage.get_stage(),
                                 5, 5, food_color,
                                 stage_color, win, characters, 1)

while win_life:
    # Use actual timer later on
    pygame.time.delay(delay_ms)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False

    Engine.move_characters(number_of_characters, characters, foods,
                           stage.get_walls())


pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
