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

    # Spans randomly throughout the stage the amount of food selected with
    # random values of nutrition within the range.
    # Replaces the list of foods.
    def initialize_food_list(self, amount: int,
                             range_of_values: Tuple[int, int],
                             stage: Stage.Stage,
                             blockings: List[Rectangle.Rectangle]):
        foods = list()
        x_min, y_min, x_max, y_max = stage.get_stage_limits()
        x_max -= self.__food_size
        y_max -= self.__food_size

        while len(foods) < amount:
            current_x = random.randint(x_min, x_max)
            current_y = random.randint(y_min, y_max)
            current_limits = (current_x, current_y,
                              current_x + self.__food_size,
                              current_y + self.__food_size)
            current_value = random.randint(range_of_values[0],
                                           range_of_values[1])

            blocks = False
            for blocking in blockings:
                if blocking.area_collide(current_limits):
                    blocks = True
                    break

            for food in foods:
                if food.area_collide(current_limits):
                    blocks = True
                    break

            if blocks is False:
                foods.append(Food(len(foods)+1,
                                  current_x, current_y,
                                  self.__food_size, self.__food_size,
                                  self.__food_color, stage.get_stage_color(),
                                  stage.get_win(), current_value))

        self.__foods = foods
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
