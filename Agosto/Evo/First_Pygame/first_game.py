import pygame
import random
from typing import List

import Rectangle
import Character
import Stage
import Food
import Engine

pygame.init()

win_heigth = 700
win_width = 1200
win_title = "First game"
win_life = True

clock_position = (500, 650)
fps = 20
clock_font_type = "Trebuchet MS"
clock_font_size = 25
clock_font = (clock_font_type, clock_font_size)
clock_font_color = (0, 0, 0)
clock_ttl = 5*1000

stage_size = (800, 500)
stage_color = (211, 211, 211)
walls_color = (0, 255, 0)
stage_colors = (stage_color, walls_color)

character_size = 20
character_speed = 5
character_sensing = 70
food_size = 5
food_nutritional_value = 1

number_of_characters = 70
number_of_foods = 80

characters = list()
foods = list()

color_1 = (255, 0, 0)
color_2 = (0, 0, 255)
food_color = (255, 255, 255)
stage_color = (211, 211, 211)
walls_color = (0, 255, 0)

win = pygame.display.set_mode((win_width, win_heigth))
pygame.display.set_caption(win_title)

start_game = False

stage = Engine.initialize_stage(stage_size, stage_colors, fps, clock_position,
                                clock_font, clock_font_color, clock_ttl, win)

while start_game is False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            start_game = True

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


pygame.display.update()

start_game = False

while start_game is False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            start_game = True


while win_life:

    if stage.update_clock() is False:
        win_life = False

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                win_life = False

    Engine.move_characters(number_of_characters, characters, foods,
                           stage.get_walls())


pygame.display.update()

start_game = False

while start_game is False:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            start_game = True

pygame.quit()
