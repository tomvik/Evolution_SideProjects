import pygame
import random

import Color
import Coordinate
import Dimensions
import PositionAndDimension
import Character
import Collisions

pygame.init()

delay_ms = 100
background_color = Color.RBGColor(0, 0, 0)
win_height = 500
win_width = 500
win_title = "First game"
win_life = True

vel = 10
possible_movements = ["UP", "RIGHT", "DOWN", "LEFT"]
number_of_characters = 2
characters = []
mov = []

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption(win_title)

coordinate_1 = Coordinate.Coordinate(50, 50)
dimension_1 = Dimensions.TwoDDimension(40, 60)
start_and_dimension_1 = PositionAndDimension.PositionAndDimension(coordinate_1,
                                                                  dimension_1)

coordinate_2 = Coordinate.Coordinate(120, 50)
dimension_2 = Dimensions.TwoDDimension(40, 80)
start_and_dimension_2 = PositionAndDimension.PositionAndDimension(coordinate_2,
                                                                  dimension_2)

color_1 = Color.RBGColor(255, 0, 0)
color_2 = Color.RBGColor(0, 0, 255)

characters.append(Character.Character(
    start_and_dimension_1, color_1, background_color, vel, win))
characters.append(Character.Character(
    start_and_dimension_2, color_2, background_color, vel, win))

for i in range(number_of_characters):
    mov.append(random.choice(possible_movements))

while win_life:
    # Use actual timer later on
    pygame.time.delay(delay_ms)
    pygame.display.update()

    if Collisions.IsCollision(characters[0], characters[1]):
        pygame.time.delay(delay_ms+1000)
        characters[0].reset_position(50, 50)
        characters[1].reset_position(120, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False

    for i in range(number_of_characters):
        mov[i] = random.choice(possible_movements)
        while characters[i].move_is_possible(mov[i]) is False:
            mov[i] = random.choice(possible_movements)
        characters[i].move(mov[i])


pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
