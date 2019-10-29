import pygame
from typing import List, Tuple

import Rectangle


class TextBox:

    def __init__(self, position: Tuple[int, int], size: Tuple[int, int],
                 colors: Tuple[List[int], List[int]],
                 background_color: List[int],
                 font_letter: str, font_size: int, win: pygame.Surface,
                 text: str = ''):
        rect = pygame.Rect(position, size)
        self.__rect = Rectangle.Rectangle(rect, colors[0],
                                          background_color, win)
        self.__win = win
        self.__color = colors[1]
        self.__text = text
        self.__font = pygame.font.SysFont(font_letter, font_size)
        self.__text_surface = self.__font.render(
            self.__text, 1, self.__color)
        self.__active = False

    def handle_event(self, event: pygame.event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__rect.collide_point(event.pos):
                self.__active = not self.__active
            else:
                self.__active = False
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_RETURN:
                    print(self.__text)
                elif event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1]
                else:
                    self.__text += event.unicode
                self.__text_surface = self.__font.render(
                    self.__text, 1, self.__color)
                self.draw()

    def draw(self):
        self.__rect.draw_background()
        self.__rect.draw()
        self.__win.blit(self.__text_surface, self.__rect.get_rectangle())
        pygame.display.update()

    def write_text(self, text: str):
        self.__text = text

    def get_text(self) -> str:
        return self.__text
