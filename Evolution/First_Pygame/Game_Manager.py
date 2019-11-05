import pygame
from typing import Dict, List, Tuple

from Character_Manager import CharacterManager
from Food_Manager import FoodManager
from Stage import Stage
import Constants
import Rectangle
from Common_Types import *


class GameManager:
    def __init__(self,
                 window_size: Point,
                 window_title: str,
                 stage_size: Point,
                 stage_colors: Tuple[Color, Color],
                 clock_font: Font,
                 clock_font_color: Color,
                 text_font: Font,
                 character_size: Size,
                 character_speed: Tuple[int, int],
                 character_sensing: Tuple[int, int],
                 character_patience: Tuple[int, int],
                 traverse_characters: bool,
                 food_size: Size,
                 food_color: Color,
                 food_value: int,
                 file_name: str,
                 update_display: bool) -> 'GameManager':
        pygame.init()
        self.__days = 0
        self.__traverse = traverse_characters
        self.__update_display = update_display
        self.__stage = self.__initialize_stage(window_size,
                                               window_title,
                                               stage_size,
                                               stage_colors,
                                               clock_font,
                                               clock_font_color,
                                               text_font)
        self.__wait_for_input()
        stage_data = self.__load_stage_state()
        self.__max_generation = stage_data[Constants.MAX_GENERATION]
        self.__update_stage_state(stage_data[Constants.FPS],
                                  stage_data[Constants.TTL])
        self.__character_manager, self.__food_manager = \
            self.__initialize_managers(
                self.__stage,
                stage_data[Constants.INITIAL_CHARACTERS],
                character_size,
                character_speed,
                character_sensing,
                character_patience,
                stage_data[Constants.INITIAL_FOODS],
                food_size,
                food_color,
                food_value
            )
        pygame.display.update()
        self.__wait_for_enter()
        self.__stage.initialize_game()
        self.__file_name = file_name

    def __del__(self):
        pygame.quit()

    # Runs the game in continuous mode.
    def continous_game(self):
        window_life = True
        round_life = True
        while window_life:
            while round_life:
                round_life, window_life = self.__run_game()
            if window_life:
                window_life = self.__new_round()
                round_life = True
            pygame.display.update()
        self.__wait_for_exit()

    # Initializes the stage.
    def __initialize_stage(self,
                           window_size: Size,
                           window_title: str,
                           stage_size: Size,
                           stage_colors: Tuple[Color, Color],
                           clock_font: Font,
                           clock_font_color: Color,
                           text_font: Font) -> Stage:
        stage = Stage(window_size, window_title, stage_size, stage_colors,
                      clock_font, clock_font_color, text_font)
        pygame.display.update()
        return stage

    # Initialize the managers and waits for the input.
    def __initialize_managers(self,
                              stage: Stage,
                              number_of_characters: int,
                              character_size: int,
                              character_speed: Tuple[int, int],
                              character_sensing: Tuple[int, int],
                              character_patience: Tuple[int, int],
                              number_of_foods: int,
                              food_size: int,
                              food_color: Color,
                              food_value: int) -> Tuple[CharacterManager,
                                                        FoodManager]:

        character_manager = CharacterManager(character_size)
        character_manager.initialize(number_of_characters,
                                     character_sensing,
                                     character_speed,
                                     character_patience,
                                     stage)

        food_manager = FoodManager(food_size,
                                   food_color)
        food_manager.initialize(number_of_foods,
                                (food_value, food_value),
                                stage,
                                character_manager.get_list())

        return character_manager, food_manager

    # Waits for the input of textboxes.
    # It finishes once enter has been pressed.
    def __wait_for_input(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                self.__stage.handle_event(event)
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    waiting = False

    # Waits for the key enter and while doing so,
    # the input textboxes can be written on.
    def __wait_for_enter(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    waiting = False

    # Waits for the key enter and while doing so,
    # the input textboxes can be written on.
    def __wait_for_exit(self):
        while True:
            for event in pygame.event.get():
                if self.__maybe_quit(event):
                    return

    # Returns a list of the values of the text_boxes.
    def __load_stage_state(self) -> Dict[str, int]:
        return self.__stage.get_text_values()

    # Updates the stage state by setting the TTL and FPS
    def __update_stage_state(self, fps: int, ttl: int):
        self.__stage.set_fps(fps)
        self.__stage.set_ttl_seconds(ttl)

    # Returns true if quit or escape have been pressed.
    def __maybe_quit(self, event: pygame.event) -> bool:
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return True
        return False

    # Returns True if space has been pressed.
    def __maybe_end_round(self, event: pygame.event) -> int:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False

    # Handles the events during the game.
    def __handle_in_game_events(self) -> int:
        for event in pygame.event.get():
            if self.__maybe_quit(event):
                return 1
            if self.__maybe_end_round(event):
                return 2
        return 0

    # Sorts both character and food lists by its x coordinate.
    def __xsort_lists(self):
        self.__character_manager.xsort()
        self.__food_manager.xsort()

    # Runs the game. Returns false if the round has finished.
    def __run_game(self) -> Tuple[bool, bool]:
        round_life = True
        window_life = True
        self.__xsort_lists()
        self.__character_manager.move_characters(self.__food_manager,
                                                 self.__stage,
                                                 self.__traverse)
        self.__food_manager.draw()
        remaining_characters = self.__character_manager.characters_left()
        remaining_foods = self.__food_manager.food_left()

        round_life = self.__stage.handle_in_game(self.__load_data_dict(0))
        if remaining_characters is 0 \
                or (remaining_foods is 0
                    and self.__character_manager.heading_home() is False):
            round_life = False
        event_case = self.__handle_in_game_events()
        if event_case == 1:
            round_life = window_life = False
        elif event_case == 2:
            round_life = False
        if self.__update_display:
            pygame.display.update()

        if self.__character_manager.get_newest_generation() >= \
                self.__max_generation:
            round_life = window_life = False

        return round_life, window_life

    # Resets the game to run another round.
    def __new_round(self) -> bool:
        self.__character_manager.new_round_characters(Constants.REPRODUCTION)
        self.__food_manager.reset_foods(self.__character_manager.get_list())
        self.__days += 1
        text_boxes_dict = self.__load_data_dict(1)
        self.__stage.new_round_stage(text_boxes_dict)
        self.__update_stats(text_boxes_dict)
        return self.__character_manager.characters_left() > 0

    # Loads the data for the dictionary, depending the case.
    # Case 0: In-game update
    # Case 1: New round update
    def __load_data_dict(self, case: int) -> Dict[str, int]:
        key_value = {Constants.CHARACTERS:
                     self.__character_manager.characters_left(),
                     Constants.FOODS:
                     self.__food_manager.food_left()}
        if case == 1:
            key_value.update({
                Constants.INITIAL_CHARACTERS:
                self.__character_manager.characters_left(),
                Constants.INITIAL_FOODS:
                self.__food_manager.food_left(),
                Constants.NEWEST_GENERATION:
                self.__character_manager.get_newest_generation(),
                Constants.OLDEST_GENERATION:
                self.__character_manager.get_oldest_generation(),
                Constants.PERISHED:
                self.__character_manager.get_perished(),
                Constants.NEWBORN:
                self.__character_manager.get_newborn(),
                Constants.DAYS:
                self.__days
            })
        return key_value

    # Writes down the stats to the stats file.
    def __update_stats(self, key_value: Dict[str, int]):
        data = "\n"
        for x, y in key_value.items():
            data += x + " " + str(y) + "\n"
        data += "\n"
        data += self.__character_manager.get_stats()
        file = open(self.__file_name, "a+")
        file.write(data)
        file.close()
