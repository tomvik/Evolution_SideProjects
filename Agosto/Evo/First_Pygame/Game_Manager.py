import pygame
from typing import Dict, List, Tuple

from Character_Manager import CharacterManager
from Food_Manager import FoodManager
from Stage import Stage
import Constants


class GameManager:
    def __init__(self,
                 window_size: Tuple[int, int],
                 window_title: str,
                 stage_size: Tuple[int, int],
                 stage_colors: Tuple[List[int], List[int]],
                 clock_font: Tuple[str, int],
                 clock_font_color: List[int],
                 text_font: Tuple[str, int],
                 character_size: int,
                 character_color: List[int],
                 character_speed: int,
                 character_sensing: int,
                 traverse_characters: bool,
                 food_size: int,
                 food_color: List[int],
                 food_value: int) -> 'GameManager':
        self.__days = 0
        self.__traverse = traverse_characters
        self.__window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(window_title)
        self.__stage = self.__initialize_stage(self.__window,
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
            self.__initialize_managers(self.__stage,
                                       stage_data[Constants.CHARACTERS],
                                       character_size,
                                       character_color,
                                       character_speed,
                                       character_sensing,
                                       stage_data[Constants.FOODS],
                                       food_size,
                                       food_color,
                                       food_value)
        pygame.display.update()
        self.__wait_for_enter()
        self.__stage.initialize_game()

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
        self.__wait_for_enter()

    # Initializes the stage.
    def __initialize_stage(self,
                           win: pygame.Surface,
                           stage_size: Tuple[int, int],
                           stage_colors: Tuple[List[int], List[int]],
                           clock_font: Tuple[str, int],
                           clock_font_color: List[int],
                           text_font: Tuple[str, int]) -> Stage:
        stage = Stage(win, stage_size, stage_colors,
                      clock_font, clock_font_color, text_font)
        pygame.display.update()
        return stage

    # Initialize the managers and waits for the input.
    def __initialize_managers(self,
                              stage: Stage,
                              number_of_characters: int,
                              character_size: int,
                              character_color: List[int],
                              character_speed: int,
                              character_sensing: int,
                              number_of_foods: int,
                              food_size: int,
                              food_color: List[int],
                              food_value: int) -> Tuple[CharacterManager,
                                                        FoodManager]:

        character_manager = CharacterManager(character_size,
                                             character_color)
        character_manager.initialize(number_of_characters,
                                     (character_sensing,
                                      character_sensing),
                                     (character_speed,
                                      character_speed),
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
        waiting: bool = True
        while waiting:
            for event in pygame.event.get():
                self.__stage.handle_event(event)
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    waiting = False

    # Waits for the key enter and while doing so,
    # the input textboxes can be written on.
    def __wait_for_enter(self):
        waiting: bool = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    waiting = False

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

    # Runs the game. Returns false if the round has finished.
    def __run_game(self) -> Tuple[bool, bool]:
        round_life = True
        window_life = True
        self.__character_manager.move_characters(self.__food_manager,
                                                 self.__stage,
                                                 self.__traverse)
        remaining_characters = self.__character_manager.characters_left()
        remaining_foods = self.__food_manager.food_left()

        key_value = {Constants.CHARACTERS:
                     remaining_characters,
                     Constants.FOODS:
                     remaining_foods}
        round_life = self.__stage.handle_in_game(key_value)
        if remaining_characters is 0 \
                or (remaining_foods is 0
                    and self.__character_manager.heading_home() is False):
            round_life = False
        event_case = self.__handle_in_game_events()
        if event_case == 1:
            round_life = window_life = False
        elif event_case == 2:
            round_life = False
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
        key_value = {Constants.CHARACTERS:
                     self.__character_manager.characters_left(),
                     Constants.FOODS:
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
                     self.__days}
        self.__stage.new_round_stage(key_value)
        return self.__character_manager.characters_left() > 0
