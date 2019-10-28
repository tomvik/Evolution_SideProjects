import pygame
import random
from typing import List

import Color
import Rectangle
import Character
import Food
import Engine

pygame.init()

delay_ms = 100
win_heigth = 700
win_width = 1200
win_title = "First game"
win_life = True

number_of_characters = 20
number_of_foods = 20

characters = list()
stage = list()
foods = list()
walls = list()

window_rect = pygame.Rect(0, 0, win_width, win_heigth)
stage_rects = (pygame.Rect(0, 0, 100, win_heigth),
               pygame.Rect(0, 0, win_width, 100),
               pygame.Rect(1100, 0, 100, win_heigth),
               pygame.Rect(0, 600, win_width, 100))
actual_stage_rect = (pygame.Rect(100, 100, 1000, 500))

color_1 = Color.RBGColor(255, 0, 0)
color_2 = Color.RBGColor(0, 0, 255)
food_color = Color.RBGColor(255, 255, 255)
stage_color = Color.RBGColor(211, 211, 211)
stage_walls_color = Color.RBGColor(0, 0, 0)

win = pygame.display.set_mode((win_width, win_heigth))
pygame.display.set_caption(win_title)

stage.append(Rectangle.Rectangle(actual_stage_rect,
                                 stage_color, stage_walls_color, win))
for stage_rect in stage_rects:
    stage.append(Rectangle.Rectangle(
        stage_rect, stage_walls_color, stage_walls_color, win))
    walls.append(stage[-1])

characters = Engine.span_random_characters(20, actual_stage_rect, 10, 15,
                                           color_1, stage_color, win)

foods = Engine.span_random_foods(20, actual_stage_rect, 5, 5, food_color,
                                 stage_color, win, 1, characters)

while win_life:
    # Use actual timer later on
    pygame.time.delay(delay_ms)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False

    Engine.move_characters(number_of_characters, characters, foods, walls)

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
