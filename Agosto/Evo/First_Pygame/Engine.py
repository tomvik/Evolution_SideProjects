import pygame
import random
from typing import List, Tuple

import Rectangle
from Character import Character
from Character_Manager import CharacterManager
from Food import Food
from Food_Manager import FoodManager
import Stage
import Constants
import TextBox


# Initializes the stage.
def initialize_stage(stage_size: Tuple[int, int],
                     stage_colors: Tuple[List[int], List[int]],
                     fps: int, clock_font: Tuple[str, int],
                     clock_font_color: List[int], ttl: int,
                     text_font: Tuple[str, int],
                     win: pygame.Surface) -> Stage.Stage:
    stage = Stage.Stage(stage_size, stage_colors,
                        win, fps, clock_font,
                        clock_font_color, ttl, text_font)
    pygame.display.update()
    return stage


# Initialize the managers and waits for the input.
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
    number_of_characters, number_of_foods, ttl, fps = load_state(stage)
    stage.set_ttl_seconds(ttl)
    stage.set_fps(fps)

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


# Waits for the key enter and while doing so,
# the input textboxes can be written on.
def wait_for_enter(stage: Stage.Stage):
    waiting: bool = True
    while waiting:
        for event in pygame.event.get():
            stage.handle_event(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


# Returns a list of the values of the text_boxes.
def load_state(stage: Stage.Stage) -> List[int]:
    return stage.get_text_values()


# Returns true if quit or escape have been pressed.
def maybe_quit(event: pygame.event) -> bool:
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True
    return False


def maybe_restart(event: pygame.event, stage: Stage.Stage) -> int:
    stage.handle_event(event)
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            return True
    return False


def handle_events(in_game: bool, stage: Stage.Stage) -> int:
    for event in pygame.event.get():
        if maybe_quit(event):
            return 1
        if not in_game:
            if maybe_restart(event, stage):
                return 2
    return 0


# Resets the game to run another round.
def new_round_game(character_manager: CharacterManager,
                   food_manager: FoodManager,
                   stage: Stage.Stage) -> bool:
    character_manager.new_round_characters(Constants.REPRODUCTION)
    food_manager.reset_foods(character_manager.get_list())
    stage.new_round_stage(character_manager.characters_left(),
                          food_manager.food_left())
    return character_manager.characters_left() > 0


# Runs the game. Returns false if the round has finished.
def run_game(character_manager: CharacterManager, food_manager: FoodManager,
             stage: Stage.Stage, traverse_character: bool) -> bool:
    round_life: bool = True
    character_manager.move_characters(food_manager, stage,
                                      traverse_character)
    round_life = stage.handle_in_game(character_manager.characters_left(),
                                      food_manager.food_left())
    if character_manager.characters_left() is 0 \
            or (food_manager.food_left() is 0
                and character_manager.heading_home() is False):
        round_life = False
    if handle_events(True, stage) == 1:
        round_life = False
    pygame.display.update()

    return round_life
