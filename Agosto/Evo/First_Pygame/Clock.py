import pygame
from typing import Tuple, List

import TextBox


class Clock:
    def __init__(self, fps: int, pos: Tuple[int, int], box_color: List[int],
                 background_color: List[int], font_letter: str, font_size: int,
                 font_color: List[int], ttl: int, win: pygame.Surface):
        self.__fps = fps
        self.__clock = pygame.time.Clock()
        self.__ttl = ttl
        self.__total_ms = 0
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
        self.__first = True
        self.__hour_box = TextBox.TextBox(pos, font_color, box_color,
                                          True, background_color,
                                          font_letter, font_size, False, win,
                                          "{0:02}:".format(self.__hour))
        x, y = pos
        pos = (x+((self.__hour_box.get_size())[0]), y)
        self.__minute_box = TextBox.TextBox(pos, font_color, box_color,
                                            True, background_color,
                                            font_letter, font_size, False, win,
                                            "{0:02}:".format(self.__minute))
        x, y = pos
        pos = (x+((self.__minute_box.get_size())[0]), y)
        self.__second_box = TextBox.TextBox(pos, font_color, box_color,
                                            True, background_color,
                                            font_letter, font_size, False, win,
                                            "{0:02}".format(self.__second))

    # Returns true if the time is still under the TTL.
    def still_valid(self) -> bool:
        return self.__total_ms < self.__ttl

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

    # Writes and draws the new values of time.
    def draw(self):
        self.__hour_box.write("{0:02}:".format(self.__hour))
        self.__hour_box.draw()
        self.__minute_box.write("{0:02}:".format(self.__minute))
        self.__minute_box.draw()
        self.__second_box.write("{0:02}".format(self.__second))
        self.__second_box.draw()

    # Resets the clock to 0 and draws it.
    def reset(self):
        self.__first = True
        self.update_clock()
        self.__first = True
        self.draw()
