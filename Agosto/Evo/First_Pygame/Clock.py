import pygame
from typing import Tuple, List

import Rectangle


class Clock:
    def __init__(self, fps: int, pos: Tuple[int, int],
                 font_letter: str, font_size: int, font_color: List[int]):
        self.__fps = fps
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.SysFont(font_letter, font_size)
        self.__font_color = font_color
        self.__total_ms = 0
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
        self.__hour_font, self.__hour_fontR = self.initialize_font(
            self.__hour, pos)
        self.__minute_font, self.__minute_fontR = self.initialize_font(
            self.__minute, (pos[0]+150, pos[1]))
        self.__second_font, self.__second_fontR = self.initialize_font(
            self.__second, (pos[0]+300, pos[1]))

    def initialize_font(self, time: int, pos: Tuple[int, int]):
        font = self.__font.render("Hour:{0:02}".format(
            time), 1, self.__font_color)  # zero-pad hours to 2 digits
        fontR = font.get_rect()
        fontR.center = pos
        return font, fontR

    # This function should be called each frame.
    def update_clock(self):
        self.__clock.tick_busy_loop(self.__fps)
        self.__total_ms += self.__clock.get_time()

        self.__second = int(self.__total_ms/1000)
        self.__minute = int(self.__second/60)
        self.__hour = int(self.__minute/60)

        self.__second = self.__second % 60
        self.__minute = self.__minute % 60

    # Draws background first and renders the new time.
    def render_clock(self, background: Rectangle, win: pygame.Surface):
        background.draw()
        self.__second_font = self.__font.render(
            "Second:{0:02}".format(self.__second), 1, self.__font_color)
        win.blit(self.__second_font, self.__second_fontR)
        self.__minute_font = self.__font.render(
            "Minute:{0:02}".format(self.__minute), 1, self.__font_color)
        win.blit(self.__minute_font, self.__minute_fontR)
        self.__hour_font = self.__font.render(
            "Hour:{0:02}".format(self.__hour), 1, self.__font_color)
        win.blit(self.__hour_font, self.__hour_fontR)
