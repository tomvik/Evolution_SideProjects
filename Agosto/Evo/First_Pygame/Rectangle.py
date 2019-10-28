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
