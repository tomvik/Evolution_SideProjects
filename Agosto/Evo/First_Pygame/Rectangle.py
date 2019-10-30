import pygame
import random
import math
from typing import List, Tuple


class Rectangle:

    def __init__(self, rectangle: pygame.Rect, color: List[int],
                 background_color: List[int], win: pygame.Surface):
        self._rectangle = rectangle
        self._color = color
        self._background_color = background_color
        self._win = win
        self.draw()
        self._previous_movement = (0, 0)

    def __del__(self):
        self.draw_background()

    # Returns the Rectangle and Color as a Tuple.
    def get_rectangle(self) -> pygame.Rect:
        return (self._rectangle)

    # Returns the window.
    def get_window(self) -> pygame.Surface:
        return (self._win)

    # Returns the color.
    def get_color(self) -> List[int]:
        return self._color

    # Returns the size as in width, height
    def get_size(self) -> Tuple[int, int]:
        return (self._rectangle.width, self._rectangle.height)

    # Returns the background color.
    def get_background_color(self) -> List[int]:
        return self._background_color

    # Returns the Rectangle corners.
    # a b
    # c d
    def get_corners(self) -> List[Tuple[int, int]]:
        return (self._rectangle.topleft, self._rectangle.topright,
                self._rectangle.bottomleft, self._rectangle.bottomright)

    # Returns the Rectangle limits as in: x_min, y_min, x_max, y_max
    def get_limits(self) -> List[int]:
        return (self._rectangle.left, self._rectangle.top,
                self._rectangle.right, self._rectangle.bottom,)

    # Returns the position of the left top corner as x,y
    def get_position(self) -> Tuple[int, int]:
        return self._rectangle.topleft

    # Returns a random movement that does not contradict the anterior one.
    def get_random_move(self) -> Tuple[int, int]:
        possible = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        movement = random.choice(possible)
        while movement == -1*self._previous_movement:
            movement = random.choice(possible)
        return movement

    # Sets the color.
    def set_color(self, color: List[int]):
        self._color = color

    # Sets the background color
    def set_background_color(self, background_color: List[int]):
        self._background_color = background_color

    # Sets the left side to the x input
    def set_left(self, left: int):
        self._rectangle.left = left

    # Sets the top side to the y input
    def set_top(self, top: int):
        self._rectangle.top = top

    # Sets the right side to the x input
    def set_right(self, right: int):
        self._rectangle.right = right

    # Sets the bottom side to the y input
    def set_bottom(self, bottom: int):
        self._rectangle.bottom = bottom

    # Move the rectangle dx and dy from its current position.
    def move(self, movement: Tuple[float, float]):
        self._previous_movement = movement
        self._rectangle.left += movement[0]
        self._rectangle.top += movement[1]

    # Teleports the rectangle to x and y
    def teleport(self, position: Tuple[int, int]):
        self._rectangle.left = position[0]
        self._rectangle.top = position[1]

    # Draws itself.
    def draw(self):
        pygame.draw.rect(self._win, self._color, self._rectangle)

    # Draws the background.
    # Note: Must be used before moving the object.
    def draw_background(self):
        pygame.draw.rect(self._win, self._background_color, self._rectangle)

    # Blits in the window a certain Rectangle or Surface received on itself.
    def blit(self, thing):
        self._win.blit(thing, self._rectangle)

    # Returns true if there would be a collision between self and b.
    def would_collide(self, b: 'Rectangle',
                      mov: Tuple[int, int]) -> bool:
        self._rectangle.left += mov[0]
        self._rectangle.top += mov[1]
        would_collide = self._rectangle.colliderect(b.get_rectangle())
        self._rectangle.left -= mov[0]
        self._rectangle.top -= mov[1]
        return would_collide

    # Returns True if self collides with the area given.
    def area_collide(self, area: List[int]) -> bool:
        collides = False
        left, top, right, bottom = self.get_limits()
        left_, top_, right_, bottom_ = area
        if (left <= left_ <= right or left <= right_ <= right) and \
                (top <= top_ <= bottom or top <= bottom_ <= bottom):
            collides = True
        elif (left_ <= left <= right_ or left_ <= right <= right_) and \
                (top_ <= top <= bottom_ or top_ <= bottom <= bottom_):
            collides = True
        return collides

    # Returns true if self collides with the given point.
    def collide_point(self, b: Tuple[int, int]) -> bool:
        return self._rectangle.collidepoint(b)

    # Returns true if self collides with another Rectangle.
    def collides(self, b: 'Rectangle') -> bool:
        return self._rectangle.colliderect(b.get_rectangle())
