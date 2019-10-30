import pygame
from typing import List

from Rectangle import Rectangle
from Food import Food


class Character(Rectangle):
    # Variable to set where the next home would be
    # TODO: reset it when a new round begins.
    next_home = (1, 1)

    def __init__(self, left: int, top: int, width: int, height: int,
                 color: List[int], background_color: List[int],
                 win: pygame.Surface, id: int, speed: int, sensing_range: int):
        super().__init__(pygame.Rect(left, top, width, height),
                         color, background_color, win)
        self._id = id
        self._hunger = 1
        self._speed = speed
        self._sensing_range = sensing_range
        self._is_home = False

    # Returns id of character.
    def get_id(self) -> int:
        return self._id

    # Returns the hunger.
    def get_hunger(self) -> int:
        return self._hunger

    # Returns True if it's hungry.
    def is_hungry(self) -> bool:
        return self._hunger > 0

    # Returns True if it has arrived home.
    def is_home(self) -> bool:
        return self._is_home

    # Tells self that it has arrived home.
    def arrived_home(self):
        self._is_home = True

    # Returns True if self is home and not hungry.
    def finished(self) -> bool:
        return self.is_home() and (self.is_hungry() is False)

    # Returns the sensing value.
    def get_sensing(self) -> int:
        return self._sensing_range

    # Adjusts the hunger according to the nutritional value intake.
    def feed(self, nutritional_value: int):
        if self._hunger - nutritional_value < 0:
            self._hunger = 0
        else:
            self._hunger -= nutritional_value

    # Moves the object by dx and dy times speed.
    # If there's a blocking, it moves as much as possible.
    # It moves each axis separately for collision checking.
    def move(self, dx: int, dy: int, blockings: List[Rectangle]):
        if dx != 0:
            self.__move_single_axis(dx, 0, blockings)
        if dy != 0:
            self.__move_single_axis(0, dy, blockings)

    # Helper function for moving the object on a single axis.
    def __move_single_axis(self, dx: int, dy: int, blockings: List[Rectangle]):
        self.draw_background()

        super().move((dx*self._speed, dy*self._speed))

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
        self.draw()

    # Moves self to home.
    def move_home(self):
        self.draw_background()
        self.teleport(self.__class__.next_home)
        self.draw()
        window_width, window_height = self.get_window().get_size()
        character_width, character_height = self.get_size()
        new_home_x = self.__class__.next_home[0] + character_width + 5
        new_home_y = self.__class__.next_home[1]
        if new_home_x + 50 > window_width:
            new_home_x = 1
            new_home_y += character_height + 5

        self.__class__.next_home = (new_home_x, new_home_y)
