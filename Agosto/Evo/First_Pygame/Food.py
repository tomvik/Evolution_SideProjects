import pygame
from typing import List

from Rectangle import Rectangle


class Food(Rectangle):
    def __init__(self, id: int, left: int, top: int, width: int, height: int,
                 color: List[int], background_color: List[int],
                 win: pygame.Surface, nutritional_value: int):
        super().__init__(pygame.Rect(left, top, width, height),
                         color, background_color, win)
        self._id = id
        self._nutritional_value = nutritional_value

    # Returns the id.
    def get_id(self) -> int:
        return self._id

    # Returns the nutritional value.
    def get_nutritional_value(self) -> int:
        return self._nutritional_value
