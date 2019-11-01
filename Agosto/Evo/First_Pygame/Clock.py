import pygame
from typing import Tuple, List

import TextBox


class Clock:
    def __init__(self, pos: Tuple[int, int], box_color: List[int],
                 background_color: List[int], font: Tuple[str, int],
                 font_color: List[int], win: pygame.Surface,
                 fps: int = 40, ttl: int = 5000):
        self.__fps = fps
        self.__ttl = ttl
        self.__total_ms = 0
        self.__hour = 0
        self.__minute = 0
        self.__second = 0
        self.__first = True
        self.__clock = pygame.time.Clock()
        is_input = [False, False, False]
        data = [("Hour", "{0:02}:".format(self.__hour)),
                ("Minute", "{0:02}:".format(self.__minute)),
                ("Second", "{0:02}".format(self.__second))]
        self.__hour_box, self.__minute_box, self.__second_box = \
            TextBox.create_array(
                pos, (font_color, background_color), 0, win,
                is_input, data, font)
        self.__hour_box.set_transparent(False)
        self.__minute_box.set_transparent(False)
        self.__second_box.set_transparent(False)

    # Returns true if the time is still under the TTL.
    def still_valid(self) -> bool:
        return self.__total_ms < self.__ttl

    # Get TTL.
    def get_ttl(self) -> int:
        return self.__ttl

    # Get FPS.
    def get_fps(self) -> int:
        return self.__fps

    # Sets the new TTL.
    def set_ttl(self, ttl: int):
        self.__ttl = ttl

    # Sets the new FPS.
    def set_fps(self, fps: int):
        self.__fps = fps

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
