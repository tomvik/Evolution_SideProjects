import pygame

class StartAndDimensions:

	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def get_position_dimensions_array(self):
		return (self.x, self.y, self.width, self.height)

class RBGColor:

	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue

	def get_color_array(self):
		return (self.red, self.green, self.blue)


class Character:

	def __init__(self, position_dimensions, color,  background_color, vel):
		self.position_dimensions = position_dimensions
		self.color = color
		# TODO: Can be upgraded to multiple backgrounds
		self.background_color = background_color
		self.vel = vel
		pygame.draw.rect(win,
			self.color.get_color_array(),
			self.position_dimensions.get_position_dimensions_array())

	def __del__(self):
		pygame.draw.rect(win,
			self.background_color.get_color_array(),
			self.position_dimensions.get_position_dimensions_array())

	def get_character_array(self):
		return (self.position_dimensions, self.color, self.vel)

pygame.init()

delay_ms = 1000
background_color = RBGColor(0, 0, 0)
vel = 5

win_height = 500
win_width = 500
win_title = "First game"
win_life = True

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption(win_title)

start_and_dimension_1 = StartAndDimensions(50, 50, 40, 60)
#start_and_dimension_2 = StartAndDimensions(120, 50, 40, 60)
color_1 = RBGColor(255, 0, 0)

character_1 = Character(start_and_dimension_1, color_1, background_color, vel)

while win_life:
	# Use actual timer later on
	pygame.time.delay(delay_ms)
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			win_life = False

pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()