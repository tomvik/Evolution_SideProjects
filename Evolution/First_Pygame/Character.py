import pygame
import random
from typing import List

from Rectangle import Rectangle
from Food import Food
import Distances
import Constants
from Common_Types import *


class Character(Rectangle):
    # Class variable to set where the next home would be
    next_home = Point(1, 1)

    def __init__(self, rectangle: PointSize,
                 background_color: Color,
                 speed: int, sensing_range: int,
                 movement_limit: int):
        self._speed = speed
        self._sensing_range = sensing_range
        self._max_movements = movement_limit

        super().__init__(rectangle,
                         (0, 0, 0), background_color, movement_limit)
        self.__set_color_attributes()
        self.draw()
        self._energy = Constants.ENERGY
        self._generation = 0
        self._is_home = False
        self._can_reproduce = False
        self.__set_hunger()

    # Returns the generation of the character.
    def get_generation(self) -> int:
        return self._generation

    # Returns the energy of the character.
    def get_energy(self) -> int:
        return self._energy

    # Returns the hunger.
    def get_hunger(self) -> int:
        return self._hunger

    # Returns True if it's hungry.
    def is_hungry(self) -> bool:
        return self._hunger > 0

    # Returns True if it has eaten at least once.
    def has_eaten(self) -> bool:
        return self._hunger < self._original_hunger

    # Returns True if it has arrived home.
    def is_home(self) -> bool:
        return self._is_home

    # If it ate all it needed to eat, it can reproduce.
    def set_can_reproduce(self):
        self._can_reproduce = not self.is_hungry()

    # Returns True if it can reproduce
    def can_reproduce(self) -> bool:
        return self._can_reproduce

    # Tells self that it has arrived home.
    def arrived_home(self):
        self._is_home = True

    # Returns True if self is home and not hungry.
    def finished(self) -> bool:
        return self.is_home()

    # Returns the sensing value.
    def get_sensing(self) -> int:
        return self._sensing_range

    # Returns the speed value.
    def get_speed(self) -> int:
        return self._speed

    # Sets the generation of the character.
    def set_generation(self, generation: int):
        self._generation = generation

    # Sets the hunger of the character depending on its stats.
    # hunger = int(speed/10)
    def __set_hunger(self):
        self._original_hunger = int(self._speed/10) + 1
        self._hunger = self._original_hunger

    # Resets the values to indicate that is hungry and is not home.
    def reset(self):
        self._is_home = False
        self._hunger = self._original_hunger
        self._movements = 0
        self._energy = Constants.ENERGY

    # Resets the coordinate of home.
    def reset_home(self):
        self.__class__.next_home = Point(1, 1)

    # Adjusts the hunger according to the nutritional value intake.
    def feed(self, nutritional_value: int):
        if self._hunger - nutritional_value < 0:
            self._hunger = 0
        else:
            self._hunger -= nutritional_value

    # Moves the object by dx and dy times speed.
    # If there's a blocking, it moves as much as possible.
    # It moves each axis separately for collision checking.
    def move(self, dx: int, dy: int,
             blockings: List[Rectangle],
             teleport: bool = False):
        if teleport:
            x, y = self.get_center()
            self.teleport_center(Point(dx, dy))
            dx -= x
            dy -= y
        else:
            dx *= self._speed
            dy *= self._speed
            if dx != 0:
                self.__move_single_axis(dx, 0, blockings)
            if dy != 0:
                self.__move_single_axis(0, dy, blockings)
            self._movements += 1
            if self._movements >= self._max_movements:
                self._direction = random.randint(0, 4)
                self._movements = 0
            while Distances.L2(self.get_center(),
                               Constants.INTEREST_POINTS[self._direction]) \
                    < self._sensing_range:
                self._direction = random.randint(0, 4)
        self.__modify_energy(Point(dx, dy))

    # Helper function for moving the object on a single axis.
    def __move_single_axis(self, dx: int, dy: int, blockings: List[Rectangle]):
        self.draw_background()

        super().move(Direction(dx, dy))

        for block in blockings:
            if self.collides(block):
                left, top, right, bottom = block.get_limits()
                if dx > 0:  # Moving right; Hit the left side.
                    self.set_right(left)
                elif dx < 0:  # Moving left; Hit the right side.
                    self.set_left(right)
                elif dy > 0:  # Moving down; Hit the top side.
                    self.set_bottom(top)
                elif dy < 0:  # Moving up; Hit the bottom side.
                    self.set_top(bottom)

    # Moves self to home.
    def move_home(self):
        self.draw_background()
        self.teleport(self.__class__.next_home)
        self.draw()
        window_width, window_height = Constants.WINDOW_SIZE
        character_width, character_height = self.get_size()
        new_home_x = self.__class__.next_home.x + character_width + 5
        new_home_y = self.__class__.next_home.y
        if new_home_x + 50 > window_width:
            new_home_x = 1
            new_home_y += character_height + 5

        self.__class__.next_home = Point(new_home_x, new_home_y)

    def __set_color_attributes(self):
        r = Constants.SLOPE_SPEED * self._speed + Constants.B_SPEED
        r = int(r)
        r = min(r, 255)
        r = max(r, 0)
        g = Constants.SLOPE_SENSING * self._sensing_range + Constants.B_SENSING
        g = int(g)
        g = min(g, 255)
        g = max(g, 0)
        b = Constants.SLOPE_MOVEMENTS * self._max_movements \
            + Constants.B_MOVEMENTS
        b = int(b)
        b = min(b, 255)
        b = max(b, 0)
        self.set_color((r, g, b))

    # The energy consumed per movement is:
    # sqrt(dx^2 + dy^2) * speed^2
    def __modify_energy(self, d: Point):
        self._energy -= Distances.L2(d, Point(0, 0)) \
            * self._speed * self._speed
        self._energy = max(0, self._energy)

    # Returns True if there's enough energy to go back.
    # Enough energy is considered:
    # current energy > energy_to_nearest_wall + 3 movements
    def enough_energy(self, distance: int) -> bool:
        return self._energy >= (distance * self._speed * self._speed) \
            + (self._speed * self._speed * self._speed * 3)

    # Returns True if the character has no more energy.
    def no_energy(self) -> bool:
        return self._energy == 0
