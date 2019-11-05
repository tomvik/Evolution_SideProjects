import pygame
import random
import math
from typing import List, Tuple
from Common_Types import *


class Rectangle:
    __window = None

    def __init__(self,
                 rectangle: PointSize,
                 color: Color,
                 background_color: Color,
                 max_movement: int = 80):
        self._rectangle = pygame.Rect(rectangle)
        self._color = color
        self._background_color = background_color
        self.draw()
        self._movements = 0
        self._direction = 0
        self._max_movements = max_movement

    def __del__(self):
        self.draw_background()

    # Returns the Rectangle and Color as a Tuple.
    def get_rectangle(self) -> pygame.Rect:
        return self._rectangle

    # Returns the color.
    def get_color(self) -> Color:
        return self._color

    # Returns the size as in width, height
    def get_size(self) -> Size:
        return Size(self._rectangle.width, self._rectangle.height)

    # Returns the background color.
    def get_background_color(self) -> Color:
        return self._background_color

    # Returns the Rectangle corners.
    # a b
    # c d
    def get_corners(self) -> Corners:
        left, top = self._rectangle.topleft
        right, bottom = self._rectangle.bottomright
        return Corners(Point(left, top),
                       Point(right, top),
                       Point(left, bottom),
                       Point(right, bottom))

    # Returns the Rectangle limits as in: x_min, y_min, x_max, y_max
    def get_limits(self) -> Limits:
        return Limits(self._rectangle.left, self._rectangle.top,
                      self._rectangle.right, self._rectangle.bottom)

    # Returns the position of the left top corner as x,y
    def get_position(self) -> Point:
        return Point(self._rectangle.top, self._rectangle.left)

    # Returns the center position.
    def get_center(self) -> Point:
        return Point(self._rectangle.centerx, self._rectangle.centery)

    # Returns the direction to where it's headed.
    def get_direction(self) -> int:
        return self._direction

    # Returns the max movement limit.
    def get_movement_limit(self) -> int:
        return self._max_movements

    # Sets and creates the window. Should be called at the initialization
    # of the game once.
    def set_window(window_size: Size, window_title: str):
        __class__.__window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(window_title)

    # Sets the color.
    def set_color(self, color: Color):
        self._color = color

    # Sets the background color
    def set_background_color(self, background_color: Color):
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
    def move(self, movement: Direction):
        self._rectangle.left += movement.dx
        self._rectangle.top += movement.dy

    # Teleports the rectangle to x and y
    def teleport(self, position: Point):
        self._rectangle.left = position.x
        self._rectangle.top = position.y

    # Teleports the rectangle to the center x and y
    def teleport_center(self, position: Point):
        self._rectangle.center = (position.x, position.y)

    # Draws itself.
    def draw(self):
        pygame.draw.rect(self.__class__.__window, self._color, self._rectangle)

    # Draws the background.
    # Note: Must be used before moving the object.
    def draw_background(self):
        pygame.draw.rect(self.__class__.__window, self._background_color,
                         self._rectangle)

    # Blits in the window a certain Rectangle or Surface received on itself.
    def blit(self, thing):
        self.__class__.__window.blit(thing, self._rectangle)

    # Returns true if there would be a collision between self and b.
    def would_collide(self, b: 'Rectangle', mov: Direction) -> bool:
        self._rectangle.left += mov.dx
        self._rectangle.top += mov.dy
        would_collide = self._rectangle.colliderect(b.get_rectangle())
        self._rectangle.left -= mov.dx
        self._rectangle.top -= mov.dy
        return would_collide

    # Returns True if self collides with the area given.
    def area_collide(self, area: Limits) -> bool:
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
    def collide_point(self, b: Point) -> bool:
        return self._rectangle.collidepoint(b)

    # Returns true if self collides with another Rectangle.
    def collides(self, b: 'Rectangle') -> bool:
        return self._rectangle.colliderect(b.get_rectangle())


# Returns a random position that does not collide with any other blocking.
# And may be next to the walls.
def free_random_position(limits: Limits, size: Size,
                         blockings: List[Rectangle],
                         in_wall: bool = False) -> Point:
    x_min, y_min, x_max, y_max = limits
    x_max -= size.width
    y_max -= size.height
    position = Point(0, 0)
    blocks = True
    loop = 0
    while blocks:
        loop += 1
        selected = random.randint(0, 3) if in_wall else 4
        if selected == 0:  # Left wall.
            position = Point(x_min + 1,
                             random.randint(y_min, y_max))
            blocks = check_if_blocked(position, size, blockings)
        elif selected == 1:  # Top wall.
            position = Point(random.randint(x_min, x_max),
                             y_min + 1)
            blocks = check_if_blocked(position, size, blockings)
        elif selected == 2:  # Right wall.
            position = Point(x_max - 1,
                             random.randint(y_min, y_max))
            blocks = check_if_blocked(position, size, blockings)
        elif selected == 3:  # Bottom wall.
            position = Point(random.randint(x_min, x_max),
                             y_max - 1)
            blocks = check_if_blocked(position, size, blockings)
        elif selected == 4:  # Around all the stage.
            position = Point(random.randint(x_min, x_max),
                             random.randint(y_min, y_max))
            blocks = check_if_blocked(position, size, blockings)
        if loop > 500:
            return position
    return position


# Returns True if it's blocked.
def check_if_blocked(position: Point, size: Size,
                     blockings: List[Rectangle]) -> bool:
    current_limits = Limits(position.x, position.y,
                            position.x + size.width, position.y + size.height)
    for blocking in blockings:
        if blocking.area_collide(current_limits):
            return True
    return False
