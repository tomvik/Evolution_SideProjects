import pygame

import Color
import StartAndDimension

class Character:

	def __init__(self, position_dimensions, color,  background_color, vel, win):
		self.position_dimensions = position_dimensions
		self.color = color
		# TODO: Can be upgraded to multiple backgrounds
		self.background_color = background_color
		self.vel = vel
		self.win = win
		pygame.draw.rect(self.win,
			self.color.get_color(),
			self.position_dimensions.get_position_dimensions())

	def __del__(self):
		pygame.draw.rect(self.win,
			self.background_color.get_color(),
			self.position_dimensions.get_position_dimensions())

	def get_character_array(self):
		return (self.position_dimensions, self.color, self.vel)