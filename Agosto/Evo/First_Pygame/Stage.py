import pygame
from typing import List, Tuple

from Rectangle import Rectangle
from Clock import Clock
from TextBox import TextBox
import Distances


class Stage:
    def __init__(self, width: int, height: int, stage_color: List[int],
                 walls_color: List[int], win: pygame.Surface, fps: int,
                 clock_font: Tuple[str, int], clock_font_color: List[int],
                 ttl: int, text_box_font: Tuple[str, int]):
        self.__width = width
        self.__height = height
        self.__stage_color = stage_color
        self.__walls_color = walls_color
        self.__win = win

        self.__window_width, self.__window_height = self.__win.get_size()
        self.__wall_width = (self.__window_width - self.__width) / 2
        self.__wall_height = (self.__window_height - self.__height) / 2

        self.__walls, self.__stage = self.__initialize_stage()
        self.__text_boxes = self.__initialize_text_boxes(text_box_font)

        clock_pos = (self.__width + self.__wall_width + 1,
                     self.__height + self.__wall_height)
        self.__clock = Clock(fps, clock_pos,
                             self.__stage_color, self.__walls_color,
                             clock_font[0], clock_font[1],
                             clock_font_color, ttl, self.__win)

    # Initializes the stage and returns its walls and stage.
    def __initialize_stage(self) -> Tuple[List[Rectangle], Rectangle]:
        wall_rects = (pygame.Rect(0, 0,
                                  self.__wall_width, self.__window_height),
                      pygame.Rect(0, 0,
                                  self.__window_width, self.__wall_height),
                      pygame.Rect(self.__wall_width+self.__width, 0,
                                  self.__wall_width, self.__window_height),
                      pygame.Rect(0, self.__wall_height+self.__height,
                                  self.__window_width, self.__wall_height))
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
    def __initialize_text_boxes(self, font: Tuple[str, int]) -> List[TextBox]:
        text_boxes = list()

        position = (self.__width+(self.__wall_width)+10, self.__wall_height)
        text_boxes.append(TextBox(position, self.__stage_color,
                                  self.__walls_color, True,
                                  self.__walls_color, font[0], font[1],
                                  False, self.__win,
                                  "# of Characters:"))
        current_x, current_y = position
        position = (current_x + (text_boxes[-1].get_size())[0] + 5, current_y)
        text_boxes.append(TextBox(position, self.__walls_color,
                                  self.__stage_color, False,
                                  self.__walls_color, font[0], font[1],
                                  True, self.__win,
                                  "100"))
        position = (current_x, current_y + (text_boxes[-1].get_size())[1] + 10)
        text_boxes.append(TextBox(position, self.__stage_color,
                                  self.__walls_color, True,
                                  self.__walls_color, font[0], font[1],
                                  False, self.__win,
                                  "# of Foods:"))
        position = (current_x + (text_boxes[-1].get_size())[0] + 5,
                    current_y + (text_boxes[-1].get_size())[1] + 10)
        text_boxes.append(TextBox(position, self.__walls_color,
                                  self.__stage_color, False,
                                  self.__walls_color, font[0], font[1],
                                  True, self.__win,
                                  "100"))

        return text_boxes

    # Returns the walls.
    def get_walls(self) -> List[Rectangle]:
        return self.__walls

    # Returns the stage.
    def get_stage(self) -> Rectangle:
        return self.__stage

    # Returns the stage color.
    def get_stage_color(self) -> List[int]:
        return self.__stage_color

    # Returns the window.
    def get_win(self) -> pygame.Surface:
        return self.__win

    # Returns the Stage limits as in: x_min, y_min, x_max, y_max
    def get_stage_limits(self) -> List[int]:
        return (self.__stage.get_limits())

    # Returns True if it's under its Time To Live, otherwise False.
    def update_clock(self):
        self.__clock.update_clock()
        self.__clock.draw()
        return self.__clock.still_valid()

    # Return the value of each text_box on a list.
    def get_text_values(self) -> List[int]:
        return_values = list()
        for text_box in self.__text_boxes:
            if text_box.is_input():
                return_values.append(text_box.get_value())
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

    # Handle the events for each text box.
    def handle_event(self, event: pygame.event):
        for text_box in self.__text_boxes:
            text_box.handle_event(event)
            text_box.draw()

    def handle_in_game(self, characters: int, foods: int) -> bool:
        self.__text_boxes[1].write(str(characters))
        self.__text_boxes[1].draw()
        self.__text_boxes[3].write(str(foods))
        self.__text_boxes[3].draw()

        return self.update_clock()
