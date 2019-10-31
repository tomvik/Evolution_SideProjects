import pygame
from typing import List, Tuple

import Rectangle


class TextBox:

    # TODO: add ID
    def __init__(self, position: Tuple[int, int], text_color: List[int],
                 box_color: List[int], box_transparent: bool,
                 background_color: List[int], font_letter: str, font_size: int,
                 is_input: bool,  win: pygame.Surface, name: str = '',
                 text: str = ''):
        self.__color = text_color
        self.__is_transparent = box_transparent
        self.__text = text
        self.__name = name
        self.__is_input = is_input
        self.__active = False
        self.__font = pygame.font.SysFont(font_letter, font_size)
        self.__text_surface = self.__font.render(self.__text, 1, self.__color)
        rect = self.__text_surface.get_rect()
        rect.topleft = position
        self.__rect = Rectangle.Rectangle(rect, box_color, background_color,
                                          win)
        self.__text = self.__text.strip()
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

    # Returns the name of the box.
    def get_name(self) -> str:
        return self.__name

    # Returns the Tuple [name, value]
    def get_name_value(self) -> Tuple[str, int]:
        return self.get_name(), self.get_value()

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
                self.__text = self.__text.strip()
                self.draw()

    # Updates the value of the textbox and it draws it.
    def draw(self):
        self.__rect.draw_background()
        self.__text_surface = self.__font.render(self.__text, 1, self.__color)
        if self.__is_transparent is False:
            self.__rect.draw()
        self.__rect.blit(self.__text_surface)
        pygame.display.update()


# Returns an array of TextBoxes. It does not verify if it fits on the same row.
def create_array(position: Tuple[int, int], colors: Tuple[int, int],
                 separation: int, win: pygame.Surface,
                 is_input: List[bool],
                 data: List[Tuple[str, str]],
                 font: Tuple[str, int]) -> List[TextBox]:
    text_boxes = list()
    current_x, current_y = position
    for i in range(len(is_input)):
        current_x, current_y = position
        color_1 = colors[0] if is_input[i] else colors[1]
        color_2 = colors[0] if not is_input[i] else colors[1]
        text_boxes.append(TextBox(position, color_2,
                                  color_1, not is_input[i],
                                  colors[1], font[0], font[1],
                                  is_input[i], win, data[i][0],
                                  data[i][1]))
        current_x = current_x + (text_boxes[-1].get_size())[0] + separation
        position = (current_x, current_y)
    return text_boxes


# Returns a List of Textboxes arranged in a matrix style.
def create_matrix(position: Tuple[int, int], colors: Tuple[int, int],
                  separations: Tuple[int, int], per_row: int,
                  win: pygame.Surface, is_input: List[bool],
                  data: List[Tuple[str, str]],
                  font: Tuple[str, int]) -> List[TextBox]:
    text_boxes = list()
    current_x, current_y = position
    for i in range(0, len(is_input), per_row):
        text_boxes += create_array(position,
                                   colors,
                                   separations[0],
                                   win,
                                   is_input[i:i+per_row],
                                   data[i:i+per_row],
                                   font)
        current_y += (text_boxes[-1].get_size())[1] + separations[1]
        position = (current_x, current_y)
    return text_boxes
