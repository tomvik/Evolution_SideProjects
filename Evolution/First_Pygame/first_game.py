import pygame

import Constants
from Game_Manager import GameManager
from Plotter import Plotter

pygame.init()


character_speed = (Constants.MIN_SPEED, Constants.MIN_SPEED + 5)
character_sensing = (Constants.MIN_SENSING, Constants.MIN_SENSING + 5)
character_patience = (Constants.MIN_MOVEMENTS, Constants.MAX_MOVEMENTS)

food_value = 1

game_manager = GameManager(Constants.WINDOW_SIZE,
                           Constants.WINDOW_TITLE,
                           Constants.STAGE_SIZE,
                           Constants.STAGE_COLORS,
                           Constants.CLOCK_FONT,
                           Constants.CLOCK_COLOR,
                           Constants.TEXT_FONT,
                           Constants.CHARACTER_SIZE,
                           character_speed,
                           character_sensing,
                           character_patience,
                           Constants.TRAVERSE_CHARACTERS,
                           Constants.FOOD_SIZE,
                           Constants.FOOD_COLOR,
                           food_value)

game_manager.continous_game()


plotter = Plotter(Constants.FILE_NAME+'0'+'.txt', '')
plotter.plot_3d()
pygame.quit()
