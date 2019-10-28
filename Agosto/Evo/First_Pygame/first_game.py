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
win_height = 700
win_width = 1200
win_title = "First game"
win_life = True

vel = 10
possible_movements = ["UP", "RIGHT", "DOWN", "LEFT"]
number_of_characters = 2
characters = []
mov = []

window_pd = PositionAndDimension.PositionAndDimension(
    Coordinate.Coordinate(0, 0),
    Dimensions.TwoDDimension(win_width, win_height))

win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption(win_title)

coordinate_1 = Coordinate.Coordinate(50, 50)
dimension_1 = Dimensions.TwoDDimension(10, 15)
start_and_dimension_1 = PositionAndDimension.PositionAndDimension(coordinate_1,
                                                                  dimension_1)

coordinate_2 = Coordinate.Coordinate(120, 50)
dimension_2 = Dimensions.TwoDDimension(10, 15)
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

    if Collisions.is_collision(characters[0], characters[1]):
        pygame.time.delay(delay_ms+1000)
        characters[0].reset_position(50, 50)
        characters[1].reset_position(120, 50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] \
            and characters[0].is_move_possible("UP",
                                               window_pd.get_vertex_limits()):
        characters[0].move("UP")
    elif keys[pygame.K_RIGHT] \
            and characters[0].is_move_possible("RIGHT",
                                               window_pd.get_vertex_limits()):
        characters[0].move("RIGHT")
    elif keys[pygame.K_DOWN] \
            and characters[0].is_move_possible("DOWN",
                                               window_pd.get_vertex_limits()):
        characters[0].move("DOWN")
    elif keys[pygame.K_LEFT] \
            and characters[0].is_move_possible("LEFT",
                                               window_pd.get_vertex_limits()):
        characters[0].move("LEFT")
'''
    for i in range(number_of_characters):
        mov[i] = random.choice(possible_movements)
        while \
                characters[i].is_move_possible(mov[i],
                                               window_pd.get_vertex_limits()) \
                is False:
            mov[i] = random.choice(possible_movements)
        characters[i].move(mov[i])
'''

pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
