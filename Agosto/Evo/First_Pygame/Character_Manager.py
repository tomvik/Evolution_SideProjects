import pygame
import random
from typing import List, Tuple

import Rectangle
from Character import Character
from Stage import Stage
from Food_Manager import FoodManager


class CharacterManager:
    def __init__(self, character_size: int, character_color: List[int]):
        self.__characters = list()
        self.__finished_characters = list()
        self.__character_size = character_size
        self.__character_color = character_color
        self.__initial_amount = 0

    # Spans randomly throughout the stage the amount of characters
    # selected with random values of sensing and speed, within the range.
    # Replaces the list of characters.
    def initialize_character_list(self, amount: int,
                                  sensing_range: Tuple[int, int],
                                  speed_range: Tuple[int, int],
                                  stage: Stage):
        characters = list()
        x_min, y_min, x_max, y_max = stage.get_stage_limits()
        x_max -= self.__character_size
        y_max -= self.__character_size

        while len(characters) < amount:
            current_x = random.randint(x_min, x_max)
            current_y = random.randint(y_min, y_max)
            current_limits = (current_x, current_y,
                              current_x + self.__character_size,
                              current_y + self.__character_size)
            current_speed = random.randint(speed_range[0], speed_range[1])
            current_sensing = random.randint(sensing_range[0],
                                             sensing_range[1])

            blocks = False
            for character in characters:
                if character.area_collide(current_limits):
                    blocks = True
                    break

            if blocks is False:
                characters.append(Character(current_x,
                                            current_y,
                                            self.__character_size,
                                            self.__character_size,
                                            self.__character_color,
                                            stage.get_stage_color(),
                                            stage.get_win(),
                                            len(characters) + 1,
                                            current_speed,
                                            current_sensing))

        self.__characters = characters
        self.__initial_amount = amount

    def get_list(self) -> List[Character]:
        return self.__characters

    def draw(self):
        for character in self.__characters:
            character.draw()

    def delete_index(self, index: int):
        del self.__characters[index]

    def character_left(self) -> int:
        return len(self.__characters)

    # Returns the blockings for the current index.
    def get_blockings(self, characters: List[Character],
                      walls: List[Rectangle.Rectangle],
                      current: int) -> List[Rectangle.Rectangle]:
        left_hand = characters[:current]
        right_hand = characters[current+1:]
        return left_hand + right_hand + walls

    def goto_closer_wall(self, character: Character,
                         walls: List[Rectangle.Rectangle]) -> Tuple[int, int]:
        wall = Rectangle.closest_of_all_Linf(character, walls)
        movement = Rectangle.cardinal_system_direction(character, wall)
        if character.would_collide(wall, movement):
            character.arrived_home()
            character.move_home()
            return (0, 0)
        return movement

    def goto_closer_food(self, character: Character,
                         food_manager: FoodManager) -> Tuple[int, int]:
        foods = food_manager.get_list()
        if len(foods) is 0:
            return character.get_random_move()
        food = Rectangle.closest_of_all_L2(character, foods)
        return Rectangle.sensing_direction(character, food,
                                           character.get_sensing())

    def get_direction(self, character: Character, walls: List[Rectangle.Rectangle],
                      food_manager: FoodManager) -> Tuple[int, int]:
        if (character.is_hungry() is False):
            return self.goto_closer_wall(character, walls)
        return self.goto_closer_food(character, food_manager)
        return character.get_random_move()

    # Moves the character a certain dx and dy times its own speed, plus
    # checks on the foods and eats if the character is hungry.

    def move_character(self, character: Character, dx: int, dy: int,
                       blockings: List[Rectangle.Rectangle],
                       food_manager: FoodManager):
        character.move(dx, dy, blockings)
        counter = 0
        fed = False
        foods = food_manager.get_list()
        if character.is_hungry():
            for food in foods:
                if character.rectangle.colliderect(food.rectangle):
                    character.feed(food.get_nutritional_value())
                    fed = True
                    break
                counter += 1
            if fed:
                del foods[counter]
                character.draw()

    def move_characters(self, food_manager: FoodManager, stage: Stage):
        for i in range(len(self.__characters)):
            if self.__characters[i].finished() is False:
                movement = self.get_direction(self.__characters[i], stage.get_walls(),
                                              food_manager)
                self.move_character(self.__characters[i], movement[0], movement[1],
                                    self.get_blockings(
                                        self.get_list(), stage.get_walls(), i),
                                    food_manager)
