import pygame
from typing import Dict, List, Tuple

from Rectangle import Rectangle
from Clock import Clock
import TextBox
import Distances
import Constants


class Stage:
    def __init__(self,
                 win: pygame.Surface,
                 size: Tuple[int, int],
                 stage_colors: Tuple[List[int], List[int]],
                 clock_font: Tuple[str, int],
                 clock_font_color: List[int],
                 text_box_font: Tuple[str, int]):
        self.__width = size[0]
        self.__height = size[1]
        self.__stage_color = stage_colors[0]
        self.__walls_color = stage_colors[1]
        self.__win = win

        self.__window_width, self.__window_height = self.__win.get_size()
        self.__wall_width = (self.__window_width - self.__width) / 2
        self.__wall_height = (self.__window_height - self.__height) / 2

        self.__walls, self.__stage = self.__initialize_stage()
        self.__text_boxes = self.__initialize_text_boxes(text_box_font)

        clock_pos = (self.__width + self.__wall_width + 1,
                     self.__height + self.__wall_height)
        self.__clock = Clock(clock_pos, self.__stage_color, self.__walls_color,
                             clock_font, clock_font_color, self.__win)

    # Initializes the stage and returns its walls and stage.
    def __initialize_stage(self) -> Tuple[List[Rectangle], Rectangle]:
        wall_rects = [pygame.Rect(0, 0,
                                  self.__wall_width, self.__window_height),
                      pygame.Rect(0, 0,
                                  self.__window_width, self.__wall_height),
                      pygame.Rect(self.__wall_width+self.__width, 0,
                                  self.__wall_width, self.__window_height),
                      pygame.Rect(0, self.__wall_height+self.__height,
                                  self.__window_width, self.__wall_height)]
        stage_rect = pygame.Rect(self.__wall_width, self.__wall_height,
                                 self.__width, self.__height)

        walls = list()
        for wall in wall_rects:
            walls.append(Rectangle(wall, self.__walls_color,
                                   self.__stage_color, self.__win))
        stage = Rectangle(stage_rect, self.__stage_color,
                          self.__walls_color, self.__win)
        return walls, stage

    # Initializes the text boxes. This part is partly hard_coded.
    def __initialize_text_boxes(self, font: Tuple[str, int]) -> \
            List[TextBox.TextBox]:
        text_boxes = list()

        colors = (self.__stage_color, self.__walls_color)
        position = (self.__width+(self.__wall_width)+10, self.__wall_height)
        separations = (5, 10)
        per_row = 2
        is_input = Constants.TEXTBOX_MATRIX_IS_INPUT
        data = Constants.TEXTBOX_MATRIX
        text_boxes = TextBox.create_matrix(position, colors, separations,
                                           per_row,
                                           self.__win, is_input, data, font)
        position = (5, self.__wall_height)
        is_input = Constants.INSTRUCTIONS_INPUT
        data = Constants.INSTRUCTIONS_TEXTBOXES
        text_boxes += TextBox.create_matrix(position, colors, separations,
                                            per_row,
                                            self.__win, is_input, data, font)
        return text_boxes

    # Returns the index of the box with the desired name.
    def __box_index(self, name: str) -> int:
        for i in range(len(self.__text_boxes)):
            if self.__text_boxes[i].get_name() == name:
                return i
        return -1

    # Returns the walls.
    def get_walls(self) -> List[Rectangle]:
        return self.__walls

    # Returns the stage.
    def get_stage(self) -> Rectangle:
        return self.__stage

    # Returns the stage color.
    def get_stage_color(self) -> List[int]:
        return self.__stage_color

    # Returns the wall color.
    def get_walls_color(self) -> List[int]:
        return self.__walls_color

    # Returns the window.
    def get_win(self) -> pygame.Surface:
        return self.__win

    # Returns the Stage limits as in: x_min, y_min, x_max, y_max
    def get_stage_limits(self) -> List[int]:
        return (self.__stage.get_limits())

    # Gets the TTL in seconds.
    def get_ttl_seconds(self) -> int:
        return self.__clock.get_ttl()/1000

    def get_fps(self) -> int:
        return self.__clock.get_fps()

    # Draws all the text boxes.
    def draw_input_boxes(self):
        for box in self.__text_boxes:
            if box.is_input():
                box.draw()

    # Returns True if it's under its Time To Live, otherwise False.
    def update_clock(self):
        self.__clock.update_clock()
        self.__clock.draw()
        return self.__clock.still_valid()

    # Return the value of each text_box on a list.
    def get_text_values(self) -> Dict[str, int]:
        return_values = dict()
        for text_box in self.__text_boxes:
            if text_box.is_input():
                key_value = text_box.get_name_value()
                return_values[key_value[0]] = key_value[1]
        return return_values

    # Returns the closest wall to the object and its direction towards it.
    def closest_wall_to(self,
                        a: Rectangle) -> Tuple[Rectangle, Tuple[int, int]]:
        selected_wall = Distances.closest_of_all_Linf(a, self.__walls)
        direction = Distances.cardinal_system_direction(a, selected_wall)
        return selected_wall, direction

    # Resets the clock back to 0.
    def reset_clock(self):
        self.__clock.reset()

    # Sets the new TTL.
    def set_ttl_seconds(self, ttl: int):
        self.__clock.set_ttl(ttl*1000)

    # Sets the new FPS.
    def set_fps(self, fps: int):
        self.__clock.set_fps(fps)

    # Handle the events for each text box.
    def handle_event(self, event: pygame.event):
        for text_box in self.__text_boxes:
            text_box.handle_event(event)
            text_box.draw()

    # Handles the in-game updates.
    def handle_in_game(self, key_value: Dict[str, int]) -> bool:
        for key, value in key_value.items():
            self.__text_boxes[self.__box_index(key)].write(str(value))
        self.draw_input_boxes()
        return self.update_clock()

    # Handles the updates necessary for the new round.
    def new_round_stage(self, key_value: Dict[str, int]):
        self.reset_clock()
        self.handle_in_game(key_value)

    # Changes the boxes that won't be updated anymore to output only, and those
    # that will be to input. The naming is weird, but input are the only ones
    # that get updated.
    def initialize_game(self):
        for box in self.__text_boxes:
            if box.has_name():
                if box.get_name() != Constants.CHARACTERS \
                        and box.get_name() != Constants.FOODS:
                    box.change_type()
