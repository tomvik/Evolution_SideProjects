import pygame
import random
from typing import List

import Rectangle
import Character
import Constants
from Game_Manager import GameManager

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

game_manager = GameManager(Constants.WINDOW_SIZE,
                           Constants.WINDOW_TITLE,
                           Constants.STAGE_SIZE,
                           Constants.STAGE_COLORS,
                           Constants.CLOCK_FONT,
                           Constants.CLOCK_COLOR,
                           Constants.TEXT_FONT,
                           character_size,
                           character_color,
                           character_speed,
                           character_sensing,
                           Constants.TRAVERSE_CHARACTERS,
                           food_size,
                           Constants.FOOD_COLOR,
                           food_value)

game_manager.continous_game()

pygame.quit()
