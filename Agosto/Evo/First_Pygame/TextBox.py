import pygame
from typing import List, Tuple

import Rectangle


class TextBox:

    # TODO: add ID
    def __init__(self, position: Tuple[int, int], text_color: List[int],
                 box_color: List[int], box_transparent: bool,
                 background_color: List[int], font_letter: str, font_size: int,
                 is_input: bool,  win: pygame.Surface, text: str = ''):
        self.__color = text_color
        self.__is_transparent = box_transparent
        self.__text = text
        self.__is_input = is_input
        self.__active = False
        self.__font = pygame.font.SysFont(font_letter, font_size)
        self.__text_surface = self.__font.render(self.__text, 1, self.__color)
        rect = self.__text_surface.get_rect()
        rect.topleft = position
        self.__rect = Rectangle.Rectangle(rect, box_color, background_color,
                                          win)
        if self.__is_transparent:
            self.__rect.draw_background()

    # Returns the text value in int.
    def get_value(self) -> int:
        return int(self.__text)

    # Returns the text value as string.
    def get_text(self) -> str:
        return self.__text

    # Returns the size as [width, height].
    def get_size(self) -> Tuple[int, int]:
        return self.__rect.get_size()

    # Returns True if the textbox is an input box.
    def is_input(self) -> bool:
        return self.__is_input

    # Write the input value into the textbox.
    # Note: It doesn't update the display, for that call draw().
    def write(self, text: str):
        self.__text = text

    # Handles the event of pygame.
    # It only updates those that are input boxes.
    def handle_event(self, event: pygame.event):
        if self.__is_input is False:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__rect.collide_point(event.pos):
                self.__active = not self.__active
            else:
                self.__active = False
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                else:
                    self.__text += event.unicode
                self.draw()

    # Updates the value of the textbox and it draws it.
    def draw(self):
        self.__rect.draw_background()
        self.__text_surface = self.__font.render(self.__text, 1, self.__color)
        if self.__is_transparent is False:
            self.__rect.draw()
        self.__rect.blit(self.__text_surface)
        pygame.display.update()
