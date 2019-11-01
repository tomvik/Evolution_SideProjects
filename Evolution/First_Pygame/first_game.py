import pygame
import random
from typing import List

import Rectangle
import Character
import Constants
from Game_Manager import GameManager

pygame.init()


character_speed = (Constants.MIN_SPEED, Constants.MIN_SPEED)
character_sensing = (Constants.MIN_SENSING, Constants.MIN_SENSING)
character_patience = (Constants.MIN_MOVEMENTS, Constants.MIN_MOVEMENTS)
character_color = (255, 0, 0)

food_value = 1

game_manager = GameManager(Constants.WINDOW_SIZE,
                           Constants.WINDOW_TITLE,
                           Constants.STAGE_SIZE,
                           Constants.STAGE_COLORS,
                           Constants.CLOCK_FONT,
                           Constants.CLOCK_COLOR,
                           Constants.TEXT_FONT,
                           Constants.CHARACTER_SIZE,
                           character_color,
                           character_speed,
                           character_sensing,
                           character_patience,
                           Constants.TRAVERSE_CHARACTERS,
                           Constants.FOOD_SIZE,
                           Constants.FOOD_COLOR,
                           food_value)

game_manager.continous_game()

pygame.quit()
