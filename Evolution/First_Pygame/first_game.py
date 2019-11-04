import time
import os.path


import Constants
from Game_Manager import GameManager
from Plotter import Plotter


def get_new_file_name() -> str:
    i = 0
    while os.path.isfile(Constants.FILE_NAME + str(i) + ".txt"):
        i += 1
    return Constants.FILE_NAME + str(i) + ".txt"


character_speed = (Constants.MIN_SPEED, Constants.MIN_SPEED + 5)
character_sensing = (Constants.MIN_SENSING, Constants.MIN_SENSING + 5)
character_patience = (Constants.MIN_MOVEMENTS, Constants.MAX_MOVEMENTS)
file_name = get_new_file_name()

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
                           Constants.FOOD_VALUE,
                           file_name)
game_manager.continous_game()


plotter = Plotter(file_name, '')
plotter.plot_3d()
plotter.plot()
