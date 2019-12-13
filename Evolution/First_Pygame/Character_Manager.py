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
                   aggression_range: Tuple[int, int],
                   stage: Stage):
        self.__stage_limits = stage.get_stage_limits()
        self.__stage_color = stage.get_stage_color()
        self.__walls_color = stage.get_walls_color()
        self.__characters.clear()
        self.__span_random_characters(amount, sensing_range, speed_range,
                                      aggression_range)
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
            data += Constants.AGGRESSION + " " + \
                str(character.get_aggression()) + "\n"
        return data

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
            elif self.__characters[i].no_energy():
                self.__kill(i)
                i -= 1
                characters_left -= 1
            else:
                self.__move_character(i, movement,
                                      self.__get_blockings(i,
                                                           stage.get_walls(),
                                                           only_walls),
                                      food_manager)
            i += 1
        self.__maybe_someone_is_eating_someone()
        for j in range(self.characters_left()):
            food_manager.maybe_is_eating(self.__characters[j])
            self.__characters[j].draw()

    # Resets all the characters to a random position inside the stage.
    def reset_characters(self):
        self.__characters.clear()
        self.__oldest_generation = self.__newest_generation
        while self.__finished_characters:
            if self.__finished_characters[-1].can_live():
                self.__characters.append(self.__finished_characters.pop())
                generation = self.__characters[-1].get_generation()
                if self.__oldest_generation > generation:
                    self.__oldest_generation = generation
                self.__characters[-1].draw_background()
                self.__characters[-1].teleport(Rectangle.free_random_position(
                    self.__stage_limits, self.__character_size,
                    self.__characters,
                    True))
                self.__characters[-1].set_background_color(self.__stage_color)
                self.__characters[-1].set_can_reproduce()
                self.__characters[-1].reset()
            else:
                self.__finished_characters.pop()
        if self.__characters:
            self.__characters[-1].reset_home()
        self.__perished = self.__initial_amount - len(self.__characters)
        self.__initial_amount = len(self.__characters)

    # Reproduces the surviving characters according to the probability given.
    def reproduce_characters(self, probability: int):
        self.__newborn = 0
        for i in range(self.__initial_amount):
            if self.__characters[i].can_reproduce() is False:
                continue
            speed, sensing, aggression = self.__get_mutations(i)
            next_generation = self.__characters[i].get_generation()+1
            if random.randrange(0, 100, 1) < probability:
                self.__span_random_character((sensing, sensing),
                                             (speed, speed),
                                             (aggression, aggression))
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

    # Returns True if any of the characters has eaten.
    def has_someone_eaten(self) -> bool:
        for character in self.__characters:
            if character.has_eaten():
                return True
        return False

    # Sorts the character list by its x coordinate.
    def xsort(self):
        self.__characters.sort(key=lambda x: x._rectangle.left)

    # Moves the character home, and transfers it to the finished list.
    def __move_home(self, index: int):
        self.__finished_characters.append(self.__characters.pop(index))
        self.__finished_characters[-1].move_home()
        self.__finished_characters[-1].set_background_color(self.__walls_color)

    # Kills the character with the selected index.
    def __kill(self, index: int):
        self.__characters.pop(index)

    # Returns the blockings for the current index.
    def __get_blockings(self, current: int, walls: List[Rectangle.Rectangle],
                        only_walls: bool) -> List[Rectangle.Rectangle]:
        if only_walls:
            return walls
        left_hand = characters[:current]
        right_hand = characters[current+1:]
        return left_hand + right_hand + walls

    # Returns True if the aggression of b is superior enough that it's
    # dangerous
    def __is_dangerous(self, a: int, b: int) -> bool:
        return a*a*a*Constants.AGGRESSION_DIFF < b*b*b

    # Returns a list of the directions towards the dangerous characters.
    def __get_dangers(self, index: int) -> List[Direction]:
        directions = []
        s_range = self.__characters[index].get_sensing()
        agg = self.__characters[index].get_aggression()
        closests = Distances.all_within_r_L2(self.__characters[index],
                                             self.__characters,
                                             s_range)
        for closest in closests:
            c_agg = self.__characters[closest].get_aggression()
            if self.__is_dangerous(agg, c_agg):  # Is dangerous.
                direction, within_r = \
                    Distances.sensing_direction(self.__characters[index],
                                                self.__characters[closest],
                                                s_range)
                if within_r:
                    directions.append(direction)
        return directions

    # Returns the best direction by adding and normalizing the list of
    # directions.
    def __get_best_direction(self, directions: List[Direction]) -> Direction:
        t_dx = 0
        t_dy = 0
        dx = 0
        dy = 0
        for direction in directions:
            t_dx += abs(direction.dx)
            t_dy += abs(direction.dy)
            dx -= direction.dx
            dy -= direction.dy
        if t_dx > 0:
            dx /= float(t_dx)
        else:
            dx = 0
        if t_dy > 0:
            dy /= float(t_dy)
        else:
            dy = 0
        return Direction(dx, dy)

    # Returns true if the character is in danger and the direction of its
    # movement to prevent it.
    def __in_danger(self, index: int, stage: Stage) -> Tuple[bool, Direction]:
        dangerous_directions = self.__get_dangers(index)
        if dangerous_directions:
            return True, self.__get_best_direction(dangerous_directions)
        else:
            return False, Direction(0, 0)

    # Goes through all the characters and checks if someone is eating someone.
    def __maybe_someone_is_eating_someone(self):
        characters_left = len(self.__characters)
        previous = 0
        current = 0
        after = 0
        while current < characters_left:
            has_been_eaten = False
            c_lim = self.__characters[current].get_limits()
            c_agg = self.__characters[current].get_aggression()
            previous = current
            while previous > 0:
                p_lim = self.__characters[previous].get_limits()
                p_agg = self.__characters[previous].get_aggression()
                if p_lim.x_max < c_lim.x_min:
                    break
                elif self.__characters[current].collides(
                    self.__characters[previous]) \
                        and self.__is_dangerous(c_agg, p_agg):
                    self.__characters[previous].feed(2)
                    self.__characters.pop(current)
                    has_been_eaten = True
                    characters_left -= 1
                    break
                previous -= 1
            if has_been_eaten:
                continue
            after = current
            while after < characters_left:
                a_lim = self.__characters[after].get_limits()
                a_agg = self.__characters[after].get_aggression()
                if a_lim.x_min > c_lim.x_max:
                    break
                elif self.__characters[current].collides(
                    self.__characters[after]) \
                        and self.__is_dangerous(c_agg, a_agg):
                    self.__characters[after].feed(2)
                    self.__characters.pop(current)
                    has_been_eaten = True
                    characters_left -= 1
                    break
                after += 1
            if has_been_eaten:
                continue
            current += 1

    # Returns the direction to the closest victim and returns True if it has
    # reached it.
    def __goto_closest_victim(self, index: int) -> Tuple[Direction, bool]:
        character = self.__characters[index]
        r = character.get_sensing()
        s = character.get_speed()
        agg = character.get_aggression()
        closests = Distances.all_within_r_L2(character, self.__characters, r)
        for closest in closests:
            c_character = self.__characters[closest]
            c_agg = c_character.get_aggression()
            if self.__is_dangerous(c_agg, agg):
                d, within_r = Distances.sensing_direction(character,
                                                          c_character,
                                                          r)
                if within_r:
                    d2, within_r = Distances.sensing_direction(character,
                                                               c_character,
                                                               s)
                    if within_r:
                        character.draw_background()
                        center = c_character.get_center()
                        character.move(center.x, center.y, [], True)
                        return Direction(0, 0), True
                return d, True
        return Direction(0, 0), False

    # Returns the direction to the closest wall of the indexed character.
    # If it arrives home, it does nothing and sets the variable on the
    # character.
    def __goto_closest_wall(self,
                            index: int, stage: Stage) -> Tuple[Direction, int]:
        wall, movement, distance = \
            stage.closest_wall_to(self.__characters[index])
        if self.__characters[index].would_collide(wall, movement):
            self.__characters[index].arrived_home()
            return (0, 0)
        return movement, distance

    # Returns the direction to the closest food or victim of the
    # indexed character.
    # If there's no food or victim close or left, it returns a random movement.
    def __goto_closest_food(self, i: int,
                            food_manager: FoodManager) -> Direction:
        character = self.__characters[i]
        if food_manager.food_left() > 0:
            d, r = food_manager.direction_to_closest_food(character)
            if r:
                return d
        else:
            d, r = self.__goto_closest_victim(i)
            if r:
                return d
        return Distances.get_weighted_random_move(character.get_center(),
                                                  character.get_direction())

    # Returns the direction that the character shall follow, prioritizing
    # its own safety first.
    def __get_direction(self, index: int, stage: Stage,
                        food_manager: FoodManager) -> Direction:
        in_danger, movement = self.__in_danger(index, stage)
        if in_danger:
            return movement
        elif self.__characters[index].has_eaten() is False:
            return self.__goto_closest_food(index, food_manager)

        movement, distance = self.__goto_closest_wall(index, stage)
        if self.__characters[index].is_hungry() \
                and self.__characters[index].enough_energy(distance):
            return self.__goto_closest_food(index, food_manager)
        return movement

    # Moves the character a certain dx and dy times its own speed, plus
    # checks on the foods and eats if the character is hungry.
    def __move_character(self, index: int, dir: Direction,
                         blockings: List[Rectangle.Rectangle],
                         food_manager: FoodManager):
        self.__characters[index].move(dir[0], dir[1], blockings)

    # Spans randomly throughout the stage the amount of characters
    # selected with random values of sensing and speed, within the range.
    def __span_random_characters(self, amount: int,
                                 sensing_range: Tuple[int, int],
                                 speed_range: Tuple[int, int],
                                 aggression_range: Tuple[int, int]):
        for i in range(amount):
            self.__span_random_character(sensing_range, speed_range,
                                         aggression_range)

    # Spans randomly one character.
    def __span_random_character(self,
                                sensing_range: Tuple[int, int],
                                speed_range: Tuple[int, int],
                                aggression_range: Tuple[int, int]):
        current_speed = random.randint(speed_range[0], speed_range[1])
        current_sensing = random.randint(sensing_range[0],
                                         sensing_range[1])
        current_aggression = random.randint(aggression_range[0],
                                            aggression_range[1])

        x, y = Rectangle.free_random_position(
            self.__stage_limits, self.__character_size, self.__characters,
            self.__in_wall)
        pos_dim = PointSize(x, y, self.__character_size.width,
                            self.__character_size.height)
        self.__characters.append(Character(pos_dim,
                                           self.__stage_color,
                                           current_speed,
                                           current_sensing,
                                           current_aggression))

    def __get_mutations(self, index: int) -> List[int]:
        speed = self.__characters[index].get_speed()
        sensing = self.__characters[index].get_sensing()
        aggression = self.__characters[index].get_aggression()
        index = random.choice(range(3))
        if index == 0:
            speeds = list()
            for i in range(-2, 3, 1):
                speeds.append(speed + (Constants.STEP_SPEED * i))
                speeds[i+2] = max(speeds[i+2], Constants.MIN_SPEED)
                speeds[i+2] = min(speeds[i+2], Constants.MAX_SPEED)
            index = \
                Distances.get_weighted_index(
                    Constants.PROBABILITIES_MUTATIONS,
                    0,
                    Constants.MUTATIONS_INDEXES)
            speed = speeds[index]
        elif index == 1:
            sensings = list()
            for i in range(-2, 3, 1):
                sensings.append(sensing + (Constants.STEP_SENSING * i))
                sensings[i+2] = max(sensings[i+2], Constants.MIN_SENSING)
                sensings[i+2] = min(sensings[i+2], Constants.MAX_SENSING)
            index = \
                Distances.get_weighted_index(
                    Constants.PROBABILITIES_MUTATIONS,
                    0,
                    Constants.MUTATIONS_INDEXES)
            sensing = sensings[index]
        else:
            aggressions = list()
            for i in range(-2, 3, 1):
                aggressions.append(aggression +
                                   (Constants.STEP_AGGRESSION * i))
                aggressions[i+2] = max(aggressions[i+2],
                                       Constants.MIN_AGGRESSION)
                aggressions[i+2] = min(aggressions[i+2],
                                       Constants.MAX_AGGRESSION)
            index = \
                Distances.get_weighted_index(
                    Constants.PROBABILITIES_MUTATIONS,
                    0,
                    Constants.MUTATIONS_INDEXES)
            aggression = aggressions[index]
        return speed, sensing, aggression
