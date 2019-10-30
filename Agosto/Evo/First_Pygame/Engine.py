import pygame
import random
from typing import List, Tuple

import Rectangle
from Character import Character
from Character_Manager import CharacterManager
from Food import Food
from Food_Manager import FoodManager
import Stage
import TextBox


# Moves all the characters on the list and some may eat some food.
def run_game(character_manager: CharacterManager, food_manager: FoodManager,
             stage: Stage.Stage):
    character_manager.move_characters(food_manager, stage)
    food_manager.draw()


# Initializes the stage.
def initialize_stage(stage_size: Tuple[int, int],
                     stage_colors: Tuple[List[int], List[int]],
                     fps: int, clock_position: Tuple[int, int],
                     clock_font: Tuple[str, int], clock_font_color: List[int],
                     ttl: int,
                     text_position: Tuple[int, int],
                     text_font: Tuple[str, int],
                     text_colors: Tuple[List[int], List[int]],
                     win: pygame.Surface) -> Stage.Stage:
    stage = Stage.Stage(stage_size[0], stage_size[1],
                        stage_colors[0], stage_colors[1],
                        win, fps, clock_font,
                        clock_font_color, ttl, text_font)
    pygame.display.update()
    return stage


def initialize_managers(stage: Stage.Stage, character_size: int,
                        character_color: List[int],
                        character_speed: int,
                        character_sensing: int,
                        food_size: int,
                        food_color: List[int],
                        food_value: int) -> Tuple[CharacterManager,
                                                  FoodManager]:
    print("Select amount of characters and foods. Afterwards, press enter")
    wait_for_enter(stage)
    number_of_characters, number_of_foods = load_state(stage)

    character_manager = CharacterManager(character_size, character_color)
    character_manager.initialize_character_list(number_of_characters,
                                                (character_sensing,
                                                 character_sensing),
                                                (character_speed,
                                                 character_speed),
                                                stage)

    food_manager = FoodManager(food_size, food_color)
    food_manager.initialize_food_list(number_of_foods,
                                      (food_value, food_value),
                                      stage, character_manager.get_list())

    return character_manager, food_manager


def wait_for_enter(stage: Stage.Stage):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            stage.check_box(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def load_state(stage: Stage.Stage) -> List[int]:
    return stage.get_text_values()
