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

stage_width = 800
stage_height = 500

character_size = 15
character_speed = 5
character_sensing = 70
food_size = 5
food_nutritional_value = 1

number_of_characters = 20
number_of_foods = 30

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
                                           stage.get_stage(),
                                           character_size,
                                           character_size,
                                           color_1, stage_color, win,
                                           character_speed,
                                           character_sensing)

foods = Engine.span_random_foods(number_of_foods, stage.get_stage(),
                                 food_size, food_size, food_color,
                                 stage_color, win, characters,
                                 food_nutritional_value)

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
