import pygame

import Color


class Character:
    window_width = 500
    window_heigth = 500

    def __init__(self, rectangle, color, background_color, vel, win):
        self.rectangle = rectangle
        self.color = color
        # TODO: Can be upgraded to multiple backgrounds
        self.background_color = background_color
        self.vel = vel
        self.win = win
        self.draw()

    def __del__(self):
        self.draw_background()

    def get_character_array(self):
        return (self.rectangle, self.color, self.vel)

    def draw(self):
        pygame.draw.rect(self.win, self.color.get_color(), self.rectangle)

    def draw_background(self):
        pygame.draw.rect(
            self.win, self.background_color.get_color(), self.rectangle)

    def is_move_possible(self, direction, delimiting_rectangle):
        if direction == "UP":
            return self.rectangle.y - self.vel >= delimiting_rectangle.y
        elif direction == "RIGHT":
            return self.rectangle.x + self.vel + self.rectangle.width <= \
                delimiting_rectangle.x + delimiting_rectangle.width
        elif direction == "DOWN":
            return self.rectangle.y + self.vel + self.rectangle.height <= \
                delimiting_rectangle.y + delimiting_rectangle.height
        elif direction == "LEFT":
            return self.rectangle.x - self.vel >= delimiting_rectangle.x

    def move(self, direction):
        self.draw_background()
        if direction == "UP":
            self.rectangle.move_ip(0, -self.vel)
        elif direction == "RIGHT":
            self.rectangle.move_ip(self.vel, 0)
        elif direction == "DOWN":
            self.rectangle.move_ip(0, self.vel)
        elif direction == "LEFT":
            self.rectangle.move_ip(-self.vel, 0)
        self.draw()

    def reset_position(self, x, y):
        self.draw_background()
        self.rectangle.x = x
        self.rectangle.y = y
        self.draw()
