import pygame
from typing import List, Tuple

from Rectangle import Rectangle
from Clock import Clock


class Stage:
    def __init__(self, width: int, height: int, stage_color: List[int],
                 walls_color: List[int], win: pygame.Surface, clock: Clock):
        self.__width = width
        self.__height = height
        self.__stage_color = stage_color
        self.__walls_color = walls_color
        self.__win = win
        self.__walls, self.__stage = self.__initialize_stage()
        self.__clock = clock

    def get_walls(self) -> List[Rectangle]:
        return self.__walls

    def get_stage(self) -> Rectangle:
        return self.__stage

    def __initialize_stage(self) -> Tuple[List[Rectangle], Rectangle]:
        window_width, window_height = self.__win.get_size()
        wall_width = (window_width - self.__width) / 2
        wall_height = (window_height - self.__height) / 2

        wall_rects = (pygame.Rect(0, 0, wall_width, window_height),
                      pygame.Rect(0, 0, window_width, wall_height),
                      pygame.Rect(wall_width+self.__width, 0,
                                  wall_width, window_height),
                      pygame.Rect(0, wall_height+self.__height,
                                  window_width, wall_height))
        stage_rect = pygame.Rect(wall_width, wall_height, self.__width,
                                 self.__height)

        walls = list()
        for wall in wall_rects:
            walls.append(Rectangle(wall, self.__walls_color,
                                   self.__stage_color, self.__win))
        stage = Rectangle(stage_rect, self.__stage_color,
                          self.__walls_color, self.__win)
        return walls, stage

    # Returns True if it's under its Time To Live, otherwise False.
    def update_clock(self):
        self.__clock.update_clock()
        self.__clock.render_clock(self.__walls[-1], self.__win)
        return self.__clock.still_valid()
