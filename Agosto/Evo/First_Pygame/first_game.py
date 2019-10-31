import pygame
import random
from typing import List

import Rectangle
import Character
import Stage
import Engine
from Food_Manager import FoodManager
from Character_Manager import CharacterManager

pygame.init()

win_size = (1200, 700)
win_title = "First game"
clear_grey = (211, 211, 211)
dark_grey = (140, 140, 140)

fps = 20
clock_font = ("Trebuchet MS", 25)
clock_font_color = (0, 0, 0)
clock_ttl = 5*1000

text_font = ("Trebuchet MS", 15)

stage_size = (800, 500)
stage_colors = (clear_grey, dark_grey)

character_size = 20
character_speed = 5
character_sensing = 70
character_color = (255, 0, 0)
traverse_character = True

food_size = 5
food_value = 1
food_color = (255, 255, 255)

win = pygame.display.set_mode(win_size)
pygame.display.set_caption(win_title)

stage = Engine.initialize_stage(stage_size, stage_colors, fps,
                                clock_font, clock_font_color, clock_ttl,
                                text_font, win)

character_manager, food_manager = Engine.initialize_managers(stage,
                                                             character_size,
                                                             character_color,
                                                             character_speed,
                                                             character_sensing,
                                                             food_size,
                                                             food_color,
                                                             food_value)


pygame.display.update()

Engine.wait_for_enter(stage)

win_life = True
round_life = True
continuous_mode = True

if continuous_mode:
    while win_life:
        while round_life:
            round_life = Engine.run_game(character_manager, food_manager,
                                         stage, traverse_character)
        event_case = Engine.handle_events(False, stage)
        if event_case == 0:
            pass
        elif event_case == 1:
            win_life = False
        elif event_case == 2:
            win_life = Engine.new_round_game(character_manager,
                                             food_manager, stage)
            round_life = True


while win_life:
    while round_life:
        round_life = Engine.run_game(character_manager, food_manager,
                                     stage, traverse_character)
    event_case = Engine.handle_events(False, stage)
    if event_case == 0:
        pass
    elif event_case == 1:
        win_life = False
    elif event_case == 2:
        round_life = True
        stage.reset_clock()
        character_manager, food_manager = \
            Engine.initialize_managers(stage,
                                       character_size,
                                       character_color,
                                       character_speed,
                                       character_sensing,
                                       food_size,
                                       food_color,
                                       food_value)
pygame.display.update()

pygame.quit()
