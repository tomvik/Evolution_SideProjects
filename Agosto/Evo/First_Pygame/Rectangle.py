import pygame
import random
from typing import List

import Color


class Rectangle:
    window_width = 500
    window_heigth = 500

    def __init__(self, rectangle: pygame.Rect, color: Color.RBGColor,
                 background_color: Color.RBGColor, win: pygame.Surface):
        self.rectangle = rectangle
        self.initial_pos = (rectangle.x, rectangle.y)
        self.color = color
        # TODO: Can be upgraded to multiple backgrounds
        self.background_color = background_color
        self.win = win
        self.draw()

    def __del__(self):
        self.draw_background()

    # Returns the Rectangle and Color as a Tuple.
    def get_rectangle(self):
        return (self.rectangle)

    # Draws itself.
    def draw(self):
        pygame.draw.rect(self.win, self.color.get_color(), self.rectangle)

    # Draws the background.
    # Note: Must be used before moving the object.
    def draw_background(self):
        pygame.draw.rect(
            self.win, self.background_color.get_color(), self.rectangle)

    # Returns true if there's a collision between self and character_b.
    def is_collision(self, character_b: 'Rectangle'):
        return self.rectangle.colliderect(character_b.rectangle)


# Spans the amount of rectangles on the delimited area without collision
# and adds them to the blocking list if is_blocking is set to True.
def random_spanner(amount: int, delimiter_rect: pygame.Rect,
                   span_rect: pygame.Rect, color: Color.RBGColor,
                   background_color: Color.RBGColor,
                   win: pygame.Surface, is_blocking: bool,
                   blockings: List[Rectangle]) -> List[Rectangle]:
    final_list = list()
    min_x = delimiter_rect.x
    min_y = delimiter_rect.y
    max_x = delimiter_rect.x + delimiter_rect.width - span_rect.width
    max_y = delimiter_rect.y + delimiter_rect.height - span_rect.height

    while len(final_list) < amount:
        current_x = random.randint(min_x, max_x)
        current_y = random.randint(min_y, max_y)

        current_rectangle = pygame.Rect(current_x, current_y,
                                        span_rect.width, span_rect.height)
        blocks = False
        for blocking in blockings:
            if current_rectangle.colliderect(blocking.rectangle) is True:
                blocks = True
                break

        if blocks is False:
            final_list.append(Rectangle(current_rectangle,
                                        color,
                                        background_color,
                                        win))
            if is_blocking:
                blockings.append(final_list[-1])

    return final_list
