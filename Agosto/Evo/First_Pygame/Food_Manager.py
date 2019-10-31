import pygame
import random
from typing import List, Tuple

import Rectangle
from Food import Food
import Stage
import Distances
from Character import Character


class FoodManager:
    def __init__(self, food_size: int, food_color: List[int]):
        self.__foods = list()
        self.__food_size = food_size
        self.__food_color = food_color
        self.__initial_amount = 0
        self.__range_of_values = (0, 0)
        self.__stage_limits = (0, 0, 0, 0)
        self.__stage_color = (0, 0, 0)
        self.__win = 0

    # Spans a random amount of food throughout the specified stage.
    def __span_random_food(self, amount: int,
                           blockings: List[Rectangle.Rectangle]) -> List[Food]:
        foods = list()
        while len(foods) < amount:
            current_value = random.randint(self.__range_of_values[0],
                                           self.__range_of_values[1])

            current_x, current_y = Rectangle.free_random_position(
                self.__stage_limits, self.__food_size, blockings + foods)

            foods.append(Food(len(foods)+1,
                              current_x, current_y,
                              self.__food_size, self.__food_size,
                              self.__food_color, self.__stage_color,
                              self.__win, current_value))
        return foods

    # Spans randomly throughout the stage the amount of food selected with
    # random values of nutrition within the range.
    # Replaces the list of foods.
    def initialize_food_list(self, amount: int,
                             range_of_values: Tuple[int, int],
                             stage: Stage.Stage,
                             blockings: List[Rectangle.Rectangle]):
        foods = list()
        self.__stage_limits = stage.get_stage_limits()
        self.__stage_color = stage.get_stage_color()
        self.__win = stage.get_win()
        self.__range_of_values = range_of_values

        self.__foods = self.__span_random_food(amount, blockings)
        self.__initial_amount = amount

    # Returns the list of food.
    def get_list(self) -> List[Food]:
        return self.__foods

    # Returns how much food is left.
    def food_left(self) -> int:
        return len(self.__foods)

    # Returns the direction to the closes food from the character received.
    def direction_to_closest_food(self,
                                  character: Character) -> Tuple[int, int]:
        food = Distances.closest_of_all_L2(character, self.__foods)
        return Distances.sensing_direction(character, food,
                                           character.get_sensing())

    # Delete the specific food.
    def delete_index(self, index: int):
        del self.__foods[index]

    # Draws all the foods.
    def draw(self):
        for food in self.__foods:
            food.draw()

    # Feeds the character that it receives.
    def maybe_is_eating(self, character: Character):
        counter = 0
        foods_to_eat = list()
        amount_of_food = self.food_left()

        while counter < amount_of_food and character.is_hungry():
            if character.collides(self.__foods[counter]):
                character.feed(self.__foods[counter].get_nutritional_value())
                del self.__foods[counter]
                counter -= 1
                amount_of_food -= 1
                character.draw()
            counter += 1

    # Spans the initial amount of food throughout the already defined stage.
    def reset_foods(self,
                    blockings: List[Rectangle.Rectangle]):
        self.__foods = self.__span_random_food(self.__initial_amount,
                                               blockings)
