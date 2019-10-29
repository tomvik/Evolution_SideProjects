import pygame
from typing import Tuple, List

import Rectangle


class Clock:
    def __init__(self, fps: int, pos: Tuple[int, int],
                 font_letter: str, font_size: int, font_color: List[int],
                 ttl: int):
        self.__fps = fps
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.SysFont(font_letter, font_size)
        self.__font_color = font_color
        self.__separation = 33
        self.__total_ms = 0
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
        self.__first = True
        self.__ttl = ttl

        self.__hour_font, self.__hour_fontR = self.initialize_font(
            self.__hour, pos, False)
        self.__minute_font, self.__minute_fontR = self.initialize_font(
            self.__minute, (pos[0]+self.__separation, pos[1]), False)
        self.__second_font, self.__second_fontR = self.initialize_font(
            self.__second, (pos[0]+(self.__separation*2), pos[1]), True)

    def initialize_font(self, time: int, pos: Tuple[int, int],
                        is_second: bool):
        if is_second:
            font = self.__font.render("{0:02}".format(
                time), 1, self.__font_color)
        else:
            font = self.__font.render("{0:02}:".format(
                time), 1, self.__font_color)
        fontR = font.get_rect()
        fontR.center = pos
        return font, fontR

    # This function should be called each frame.
    def update_clock(self):
        self.__clock.tick_busy_loop(self.__fps)
        self.__total_ms += self.__clock.get_time()
        if self.__first:
            self.__total_ms = 0
            self.__first = False

        self.__second = int(self.__total_ms/1000)
        self.__minute = int(self.__second/60)
        self.__hour = int(self.__minute/60)

        self.__second = self.__second % 60
        self.__minute = self.__minute % 60

    # Draws background first and renders the new time.
    def render_clock(self, background: Rectangle, win: pygame.Surface):
        background.draw()
        self.render_individual(self.__second, self.__second_font,
                               self.__second_fontR, True, win)
        self.render_individual(self.__minute, self.__minute_font,
                               self.__minute_fontR, False, win)
        self.render_individual(self.__hour, self.__hour_font,
                               self.__hour_fontR, False, win)

    # Renders individual part of clock
    def render_individual(self, time: int, font, fontR: pygame.Rect,
                          is_second: bool, win: pygame.Surface):
        if is_second:
            font = self.__font.render(
                "{0:02}".format(time), 1, self.__font_color)
        else:
            font = self.__font.render(
                "{0:02}:".format(time), 1, self.__font_color)
        win.blit(font, fontR)

    def still_valid(self) -> bool:
        return self.__ttl > self.__total_ms
