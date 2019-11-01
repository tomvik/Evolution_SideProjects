import pygame
import random
from typing import List

import Rectangle
import Character
import Stage
import Engine
import Constants
from Food_Manager import FoodManager
from Character_Manager import CharacterManager

pygame.init()

fps = 20
clock_ttl = 5*1000

character_size = 20
character_speed = 5
character_sensing = 70
character_color = (255, 0, 0)
traverse_character = True

food_size = 5
food_value = 1

win = pygame.display.set_mode(Constants.WINDOW_SIZE)
pygame.display.set_caption(Constants.WINDOW_TITLE)

stage = Engine.initialize_stage(Constants.STAGE_SIZE,
                                Constants.STAGE_COLORS,
                                fps,
                                Constants.CLOCK_FONT,
                                Constants.CLOCK_COLOR,
                                clock_ttl,
                                Constants.TEXT_FONT,
                                win)

character_manager, food_manager = \
    Engine.initialize_managers(stage,
                               character_size,
                               character_color,
                               character_speed,
                               character_sensing,
                               food_size,
                               Constants.FOOD_COLOR,
                               food_value)


pygame.display.update()

Engine.wait_for_enter(stage)

win_life = True
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
