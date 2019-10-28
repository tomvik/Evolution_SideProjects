import pygame

import Color
from Rectangle import Rectangle


class Food(Rectangle):
    def __init__(self, id: int, left: int, top: int, width: int, height: int,
                 color: Color.RBGColor, background_color: Color.RBGColor,
                 win: pygame.Surface, nutritional_value: int):
        super().__init__(pygame.Rect(left, top, width, height),
                         color, background_color, win)
        self._id = id
        self._nutritional_value = nutritional_value

    def get_id(self) -> int:
        return self._id

    def get_nutritional_value(self) -> int:
        return self._nutritional_value
