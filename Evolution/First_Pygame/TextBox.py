import pygame
from typing import List, Tuple

import Rectangle
from Common_Types import *


class TextBox:

    def __init__(self, position: Point, text_color: Color,
                 box_color: Color, box_transparent: bool,
                 background_color: Color, font: Font,
                 is_input: bool, name: str = '', text: str = ''):
        self.__color = text_color
        self.__is_transparent = box_transparent
        self.__text = text
        self.__name = name
        self.__is_input = is_input
        self.__active = False
        self.__font = pygame.font.SysFont(font.letter, font.size)
        self.__text_surface = self.__font.render(self.__text, 1, self.__color)
        rect = self.__text_surface.get_rect()
        rect.topleft = position
        self.__rect = Rectangle.Rectangle(rect, box_color, background_color)
        self.__text = self.__text.strip()
        self.draw(True)

    # Returns the text value in int.
    def get_value(self) -> int:
        return int(self.__text)

    # Returns the text value as string.
    def get_text(self) -> str:
        return self.__text

    # Returns the size as [width, height].
    def get_size(self) -> Size:
        return self.__rect.get_size()

    # Returns the name of the box.
    def get_name(self) -> str:
        return self.__name

    # Returns true if it has name.
    def has_name(self) -> bool:
        return self.__name != ''

    # Returns the Tuple [name, value]
    def get_name_value(self) -> KeyValue:
        return KeyValue(self.get_name(), self.get_value())

    # Returns True if the textbox is an input box.
    def is_input(self) -> bool:
        return self.__is_input

    # Sets if the box is transparent or not.
    def set_transparent(self, transparent: bool):
        self.__is_transparent = transparent

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
                self.draw(True)

    # Updates the value of the textbox and it draws it.
    def draw(self, update_display: bool = False):
        self.__text_surface = self.__font.render(self.__text, 1, self.__color)
        if self.__is_transparent is False:
            self.__rect.draw()
        self.__rect.blit(self.__text_surface)
        if update_display:
            pygame.display.update()

    # Changes the type of the box to the opposite one, changing its colors too.
    def change_type(self):
        self.__is_input = not self.__is_input
        self.__is_transparent = not self.__is_transparent
        new_text_color = self.__rect.get_color()
        self.__rect.set_color(self.__color)
        self.__color = new_text_color
        self.__rect.draw_background()
        self.draw(True)


# Returns an array of TextBoxes. It does not verify if it fits on the same row.
def create_array(position: Point, colors: Tuple[Color, Color],
                 separation: int,
                 is_input: List[bool],
                 data: List[KeyValue],
                 font: Font) -> List[TextBox]:
    text_boxes = list()
    current_x, current_y = position
    for i in range(len(is_input)):
        current_x, current_y = position
        color_1 = colors[0] if is_input[i] else colors[1]
        color_2 = colors[0] if not is_input[i] else colors[1]
        text_boxes.append(TextBox(position, color_2,
                                  color_1, not is_input[i],
                                  colors[1], font,
                                  is_input[i], data[i][0],
                                  data[i][1]))
        current_x = current_x + (text_boxes[-1].get_size())[0] + separation
        position = Point(current_x, current_y)
    return text_boxes


# Returns a List of Textboxes arranged in a matrix style.
def create_matrix(position: Point, colors: Tuple[Color, Color],
                  separations: Tuple[int, int], per_row: int,
                  is_input: List[bool],
                  data: List[KeyValue],
                  font: Font) -> List[TextBox]:
    text_boxes = list()
    current_x, current_y = position
    for i in range(0, len(is_input), per_row):
        text_boxes += create_array(position,
                                   colors,
                                   separations[0],
                                   is_input[i:i+per_row],
                                   data[i:i+per_row],
                                   font)
        current_y += (text_boxes[-1].get_size())[1] + separations[1]
        position = Point(current_x, current_y)
    return text_boxes
