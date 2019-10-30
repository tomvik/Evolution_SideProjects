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
round_life = True
clear_grey = (211, 211, 211)
dark_grey = (140, 140, 140)

clock_position = (500, 650)
fps = 20
clock_font = ("Trebuchet MS", 25)
clock_font_color = (0, 0, 0)
clock_ttl = 5*1000

text_position = (1125, 300)
text_colors = (dark_grey, clear_grey)
text_font = ("Trebuchet MS", 15)

stage_size = (800, 500)
stage_colors = (clear_grey, dark_grey)

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

stage = Engine.initialize_stage(stage_size, stage_colors, fps, clock_position,
                                clock_font, clock_font_color, clock_ttl,
                                text_position, text_font, text_colors, win)

number_of_characters, number_of_foods = Engine.load_state(stage)

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

Engine.wait_for_enter(stage)

while win_life:
    while round_life:

        if stage.update_clock() is False:
            round_life = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                round_life = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    round_life = False
        Engine.move_characters(number_of_characters, characters, foods,
                               stage.get_walls())
    for event in pygame.event.get():
        stage.check_box(event)
        if event.type == pygame.QUIT:
            win_life = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                win_life = False
            if event.key == pygame.K_SPACE:
                round_life = True
                stage.reset_clock()
                number_of_characters, number_of_foods = Engine.load_state(
                    stage)

                characters = Engine.span_random_characters(
                    number_of_characters,
                    stage.get_stage(),
                    character_size,
                    character_size,
                    color_1, stage_color, win,
                    character_speed,
                    character_sensing)

                foods = Engine.span_random_foods(
                    number_of_foods, stage.get_stage(),
                    food_size, food_size, food_color,
                    stage_color, win, characters,
                    food_nutritional_value)


pygame.display.update()
Engine.wait_for_enter(stage)

pygame.quit()
