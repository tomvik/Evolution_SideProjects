import pygame

import Color
import Coordinate
import PositionAndDimension


class Character:
    window_width = 500
    window_heigth = 500

    def __init__(self, position_dimensions, color, background_color, vel, win):
        self.position_dimensions = position_dimensions
        self.color = color
        # TODO: Can be upgraded to multiple backgrounds
        self.background_color = background_color
        self.vel = vel
        self.win = win
        self.draw()

    def __del__(self):
        self.draw_background()

    def get_character_array(self):
        return (self.position_dimensions, self.color, self.vel)

    def get_vertices(self):
        return self.position_dimensions.get_vertices()

    def get_vertex_limits(self):
        return self.position_dimensions.get_vertex_limits()

    def draw(self):
        pygame.draw.rect(self.win,
                         self.color.get_color(),
                         self.position_dimensions.get_position_dimensions())

    def draw_background(self):
        pygame.draw.rect(self.win,
                         self.background_color.get_color(),
                         self.position_dimensions.get_position_dimensions())

    def is_move_possible(self, direction, delimiting_vertices):
        a, b = delimiting_vertices
        if direction == "UP":
            return self.position_dimensions.coordinate.y - self.vel >= a.y
        elif direction == "RIGHT":
            return self.position_dimensions.coordinate.x + self.vel +\
                self.position_dimensions.dimension.width <=\
                b.x
        elif direction == "DOWN":
            return self.position_dimensions.coordinate.y + self.vel +\
                self.position_dimensions.dimension.heigth <=\
                b.y
        elif direction == "LEFT":
            return self.position_dimensions.coordinate.x - self.vel >= a.x

    def move(self, direction):
        self.draw_background()
        if direction == "UP":
            self.position_dimensions.coordinate.y -= self.vel
        elif direction == "RIGHT":
            self.position_dimensions.coordinate.x += self.vel
        elif direction == "DOWN":
            self.position_dimensions.coordinate.y += self.vel
        elif direction == "LEFT":
            self.position_dimensions.coordinate.x -= self.vel
        self.draw()

    def reset_position(self, x, y):
        self.draw_background()
        self.position_dimensions.coordinate.x = x
        self.position_dimensions.coordinate.y = y
        self.draw()
