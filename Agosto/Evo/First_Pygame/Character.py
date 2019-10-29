import pygame
from typing import List

import Color
from Rectangle import Rectangle
from Food import Food


class Character(Rectangle):

    def __init__(self, left: int, top: int, width: int, height: int,
                 color: Color.RBGColor, background_color: Color.RBGColor,
                 win: pygame.Surface, id: int, speed: int, sensing_range: int):
        super().__init__(pygame.Rect(left, top, width, height),
                         color, background_color, win)
        self._id = id
        self._hunger = 1
        self._speed = speed
        self._sensing_range = sensing_range

    def get_id(self) -> int:
        return self._id

    def get_hunger(self) -> int:
        return self._hunger

    def is_hungry(self) -> bool:
        return self._hunger > 0

    def get_sensing(self) -> int:
        return self._sensing_range

    # Adjusts the hunger according to the nutritional value intake.
    def feed(self, nutritional_value: int):
        if self._hunger - nutritional_value < 0:
            self._hunger = 0
        else:
            self._hunger -= nutritional_value

    # Moves the object by dx and dy times speed.
    # If there's a blocking, it moves at much as possible.
    # Also checks if there's food and eats it if there is.
    def move(self, dx: int, dy: int, blockings: List[Rectangle]):
        # Move each axis separately.
        # Note that this checks for collisions both times.
        if dx != 0:
            self.__move_single_axis(dx, 0, blockings)
        if dy != 0:
            self.__move_single_axis(0, dy, blockings)

    # Helper function for moving the object on a single axis.
    def __move_single_axis(self, dx: int, dy: int,
                           blockings: List[Rectangle]):
        self.draw_background()

        self.rectangle.x += dx*self._speed
        self.rectangle.y += dy*self._speed

        for block in blockings:
            if self.rectangle.colliderect(block.rectangle):
                if dx > 0:  # Moving right; Hit the left side of the block
                    self.rectangle.right = block.rectangle.left
                if dx < 0:  # Moving left; Hit the right side of the block
                    self.rectangle.left = block.rectangle.right
                if dy > 0:  # Moving down; Hit the top side of the block
                    self.rectangle.bottom = block.rectangle.top
                if dy < 0:  # Moving up; Hit the bottom side of the block
                    self.rectangle.top = block.rectangle.bottom
        self.draw()
