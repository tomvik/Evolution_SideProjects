import pygame
import random
from typing import List, Tuple

import Rectangle
from Character import Character
from Stage import Stage
from Food_Manager import FoodManager
import Distances
import Constants
from Common_Types import *


class CharacterManager:
    def __init__(self, character_size: Size):
        self.__characters = list()
        self.__finished_characters = list()
        self.__character_size = character_size
        self.__initial_amount = 0
        self.__stage_limits = Limits(0, 0, 0, 0)
        self.__stage_color = Color(0, 0, 0)
        self.__walls_color = Color(0, 0, 0)
        self.__in_wall = True
        self.__newest_generation = 0
        self.__oldest_generation = 0
        self.__perished = 0
        self.__newborn = 0

    # Spans randomly throughout the stage the amount of characters
    # selected with random values of sensing and speed, within the range.
    # Replaces the list of characters.
    # Initializes stage values too.
    def initialize(self, amount: int,
                   sensing_range: Tuple[int, int],
                   speed_range: Tuple[int, int],
                   movements_range: Tuple[int, int],
                   stage: Stage):
        self.__stage_limits = stage.get_stage_limits()
        self.__stage_color = stage.get_stage_color()
        self.__walls_color = stage.get_walls_color()
        self.__characters.clear()
        self.__heading_home = 0
        self.__span_random_characters(amount, sensing_range, speed_range,
                                      movements_range)
        self.__initial_amount = amount

    # Returns the list of characters.
    def get_list(self) -> List[Character]:
        return self.__characters

    # Returns how many perished the previous day.
    def get_perished(self) -> int:
        return self.__perished

    # Returns how many were born today.
    def get_newborn(self) -> int:
        return self.__newborn

    # Returns the number of the newest generation.
    def get_newest_generation(self) -> int:
        return self.__newest_generation

    # Returns the number of the oldest generation.
    def get_oldest_generation(self) -> int:
        return self.__oldest_generation

    # Returns the stats of the current set of characters.
    def get_stats(self) -> str:
        self.__characters.sort(key=lambda x: x.get_generation())
        data = ""
        for character in self.__characters:
            data += Constants.GENERATION + " " + \
                str(character.get_generation()) + " "
            data += Constants.HUNGER + " " + \
                str(character.get_hunger()) + " "
            data += Constants.SENSING + " " + \
                str(character.get_sensing()) + " "
            data += Constants.SPEED + " " + \
                str(character.get_speed()) + " "
            data += Constants.MOVEMENT + " " + \
                str(character.get_movement_limit()) + "\n"
        return data

    # Returns if someone is heading home
    def heading_home(self) -> bool:
        return self.__heading_home > 0

    # Draws all the characters.
    def draw(self):
        for character in self.__characters:
            character.draw()

    # Deletes the indexed character.
    def delete_index(self, index: int):
        del self.__characters[index]

    # Returns the number of characters that haven't finished.
    def characters_left(self) -> int:
        return len(self.__characters)

    # Moves all the characters.
    # They may also eat some food.
    def move_characters(self, food_manager: FoodManager, stage: Stage,
                        only_walls: bool):
        characters_left = self.characters_left()
        i = 0
        while i < characters_left:
            movement = self.__get_direction(i, stage, food_manager)
            if self.__characters[i].finished():
                self.__move_home(i)
                i -= 1
                characters_left -= 1
            else:
                self.__move_character(i, movement,
                                      self.__get_blockings(i,
                                                           stage.get_walls(),
                                                           only_walls),
                                      food_manager)
            i += 1
        food_manager.draw()

    # Resets all the characters to a random position inside the stage.
    def reset_characters(self):
        self.__characters.clear()
        self.__oldest_generation = self.__newest_generation
        while self.__finished_characters:
            self.__characters.append(self.__finished_characters.pop())
            generation = self.__characters[-1].get_generation()
            if self.__oldest_generation > generation:
                self.__oldest_generation = generation
            self.__characters[-1].draw_background()
            self.__characters[-1].teleport(Rectangle.free_random_position(
                self.__stage_limits, self.__character_size, self.__characters,
                True))
            self.__characters[-1].set_background_color(self.__stage_color)
            self.__characters[-1].reset()
        self.__characters[-1].reset_home()
        self.__perished = self.__initial_amount - len(self.__characters)
        self.__initial_amount = len(self.__characters)
        self.__heading_home = 0

    # Reproduces the surviving characters according to the probability given.
    def reproduce_characters(self, probability: int):
        self.__newborn = 0
        for i in range(self.__initial_amount):
            speed, sensing, movements = self.__get_mutations(i)
            next_generation = self.__characters[i].get_generation()+1
            if random.randrange(0, 100, 1) < probability:
                self.__span_random_character((sensing, sensing),
                                             (speed, speed),
                                             (movements, movements))
                self.__characters[-1].set_generation(next_generation)
                if next_generation > self.__newest_generation:
                    self.__newest_generation = next_generation
                self.__newborn += 1
        self.__initial_amount = len(self.__characters)

    # Sets the characters ready for the new round.
    def new_round_characters(self, reproduction_probability: int):
        self.reset_characters()
        self.reproduce_characters(reproduction_probability)
        self.draw()

    # Moves the character home, and transfers it to the finished list.
    def __move_home(self, index: int):
        self.__heading_home -= 1
        self.__finished_characters.append(self.__characters.pop(index))
        self.__finished_characters[-1].move_home()
        self.__finished_characters[-1].set_background_color(self.__walls_color)

    # Returns the blockings for the current index.
    def __get_blockings(self, current: int, walls: List[Rectangle.Rectangle],
                        only_walls: bool) -> List[Rectangle.Rectangle]:
        if only_walls:
            return walls
        left_hand = characters[:current]
        right_hand = characters[current+1:]
        return left_hand + right_hand + walls

    # Returns the direction to the closest wall of the indexed character.
    # If it arrives home, it does nothing and sets the variable on the
    # character.
    def __goto_closest_wall(self, index: int, stage: Stage) -> Tuple[int, int]:
        wall, movement = stage.closest_wall_to(self.__characters[index])
        if self.__characters[index].would_collide(wall, movement):
            self.__characters[index].arrived_home()
            return (0, 0)
        return movement

    # Returns the direction to the closest food of the indexed character.
    # If there's no food left, it returns a random movement.
    # TODO: Make this more pretty.
    def __goto_closest_food(self, index: int,
                            food_manager: FoodManager) -> Direction:
        if food_manager.food_left() is 0:
            return Distances.get_weighted_random_move(self.__characters[index].get_center(), self.__characters[index].get_direction())  # noqa: E501
        return food_manager.direction_to_closest_food(self.__characters[index])

    # Returns the direction that the character shall follow.
    def __get_direction(self, index: int, stage: Stage,
                        food_manager: FoodManager) -> Direction:
        if (self.__characters[index].is_hungry() is False):
            return self.__goto_closest_wall(index, stage)
        return self.__goto_closest_food(index, food_manager)

    # Moves the character a certain dx and dy times its own speed, plus
    # checks on the foods and eats if the character is hungry.
    def __move_character(self, index: int, dir: Direction,
                         blockings: List[Rectangle.Rectangle],
                         food_manager: FoodManager):
        self.__characters[index].move(dir[0], dir[1], blockings)
        if food_manager.maybe_is_eating(self.__characters[index]):
            self.__heading_home += 1

    # Spans randomly throughout the stage the amount of characters
    # selected with random values of sensing and speed, within the range.
    def __span_random_characters(self, amount: int,
                                 sensing_range: Tuple[int, int],
                                 speed_range: Tuple[int, int],
                                 movements_range: Tuple[int, int]):
        for i in range(amount):
            self.__span_random_character(sensing_range, speed_range,
                                         movements_range)

    # Spans randomly one character.
    def __span_random_character(self,
                                sensing_range: Tuple[int, int],
                                speed_range: Tuple[int, int],
                                movements_range: Tuple[int, int]):
        current_speed = random.randint(speed_range[0], speed_range[1])
        current_sensing = random.randint(sensing_range[0],
                                         sensing_range[1])
        current_movement = random.randint(movements_range[0],
                                          movements_range[1])

        x, y = Rectangle.free_random_position(
            self.__stage_limits, self.__character_size, self.__characters,
            self.__in_wall)
        pos_dim = PointSize(x, y, self.__character_size.width,
                            self.__character_size.height)
        self.__characters.append(Character(pos_dim,
                                           self.__stage_color,
                                           current_speed,
                                           current_sensing,
                                           current_movement))

    def __get_mutations(self, index: int) -> List[int]:
        speed = self.__characters[index].get_speed()
        sensing = self.__characters[index].get_sensing()
        movements = self.__characters[index].get_movement_limit()
        index = Distances.get_weighted_index(Constants.PROBABILITIES_STEP,
                                             0,
                                             Constants.STEP_INDEXES)
        if index == 0:
            speeds = list()
            for i in range(-2, 3, 1):
                # print(i)
                speeds.append(speed + (Constants.STEP_SPEED * i))
                speeds[i+2] = max(speeds[i+2], Constants.MIN_SPEED)
                speeds[i+2] = min(speeds[i+2], Constants.MAX_SPEED)
            # print(len(speeds))
            index = \
                Distances.get_weighted_index(
                    Constants.PROBABILITIES_MUTATIONS,
                    0,
                    Constants.MUTATIONS_INDEXES)
            # print(index)
            speed = speeds[index]
        elif index == 1:
            sensings = list()
            for i in range(-2, 3, 1):
                # print(i)
                sensings.append(sensing + (Constants.STEP_SENSING * i))
                sensings[i+2] = max(sensings[i+2], Constants.MIN_SENSING)
                sensings[i+2] = min(sensings[i+2], Constants.MAX_SENSING)
            # print(len(sensings))
            index = \
                Distances.get_weighted_index(
                    Constants.PROBABILITIES_MUTATIONS,
                    0,
                    Constants.MUTATIONS_INDEXES)
            # print(index)
            sensing = sensings[index]
        else:
            movementss = list()
            for i in range(-2, 3, 1):
                # print(i)
                movementss.append(movements + (Constants.STEP_MOVEMENTS * i))
                movementss[i+2] = max(movementss[i+2], Constants.MIN_MOVEMENTS)
                movementss[i+2] = min(movementss[i+2], Constants.MAX_MOVEMENTS)
            # print(len(movementss))
            index = \
                Distances.get_weighted_index(
                    Constants.PROBABILITIES_MUTATIONS,
                    0,
                    Constants.MUTATIONS_INDEXES)
            # print(index)
            movements = movementss[index]
        return speed, sensing, movements
