import turtle
import time

class ScreenInterface:

	def __init__(self, _window_width, _window_height, _window_start_x, _window_start_y):
		self.window_width = _window_width
		self.window_height = _window_height
		self.window_start_x = _window_start_x
		self.window_start_y = _window_start_y
		self.init_window(_window_width, _window_height, _window_start_x, _window_start_y)
		self.painter = turtle.Turtle()
		self.painter.speed(0)

	def __del__(self):
		time.sleep(3)
		turtle.done()

	def init_window(self, _width, _height, _start_x, _start_y):
		turtle.setup(width=_width, height=_height, startx=_start_x, starty=_start_y)

	def set_screen_size(self, _width, _height):
		turtle.screensize(_width, _height)

	def get_screen_size(self):
		return turtle.screensize()

	def draw_square(self, length, color, teta=0):
		self.painter.color(color)
		self.painter.begin_fill()
		self.painter.pendown()
		self.painter.setheading(teta)
		#Make generic
		self.painter.forward(length)
		self.painter.left(90)
		self.painter.forward(length)
		self.painter.left(90)
		self.painter.forward(length)
		self.painter.left(90)
		self.painter.forward(length)
		self.painter.penup()
		self.painter.end_fill()

#Add comments maybe make stage from figure
	def set_stage(self, _width, _height, _start_x, _start_y, _color):
		self.painter.goto(_start_x, _start_y)
		self.draw_square(_width, _color, 0)

	def draw_creature(self, _size, _start_x, _start_y, _color):
		self.painter.goto(_start_x, _start_y)
		self.draw_square(_size, _color, 0)

# Creamos una window
my_screen_interface = ScreenInterface(500, 500, 200, 200)
print(my_screen_interface.get_screen_size())

my_screen_interface.set_stage(100, 100, 0, 0, "green")

for y in range(0, 100, 5):
	for x in range(0, 100, 5):
		if (y%2 == 0):
			if (x%2 == 0):
				my_screen_interface.draw_creature(5, x, y, "red")
		elif (x%2 != 0):
			my_screen_interface.draw_creature(5, x, y, "blue")


### Draw a heart
# '''
# square 100, 45, red
# goto 0,80~
# square 50, 45, white
# goto -100, 90~
# square 400, 0, white
# '''
# draw_square(my_screen_interface.screen, 100, "green", 45)
# my_screen_interface.screen.goto(0, 80)
# draw_square(my_screen_interface.screen, 50, "white", 45)
# my_screen_interface.screen.goto(-100, 90)
# draw_square(my_screen_interface.screen, 400, "white")
# time.sleep(10)

# # Draw square of 100 pixels and Travel forward 50 pixels
# draw_square(my_screen_interface.screen, 100, "blue")
# my_screen_interface.screen.goto(50, 50)
# my_screen_interface.screen.setheading(0)
# #travel_forward(my_screen_interface.screen, 50)
# time.sleep(3)

# # Change screen size
# my_screen_interface.set_screen_size(3000, 3000)
# print(my_screen_interface.get_screen_size())

# # Draw square of 10 pixels
# draw_square(my_screen_interface.screen, 10, "green", 45)
# time.sleep(3)
