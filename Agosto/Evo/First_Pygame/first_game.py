import pygame

import Color
import Coordinate
import Dimensions
import PositionAndDimension
import Character
import Collisions

pygame.init()

delay_ms = 1000
background_color = Color.RBGColor(0, 0, 0)
vel = 5

win_height = 500
win_width = 500
win_title = "First game"
win_life = True

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

character_1 = Character.Character(
    start_and_dimension_1, color_1, background_color, vel, win)
character_2 = Character.Character(
    start_and_dimension_2, color_1, background_color, vel, win)
# character_1.DrawItself(win)
while win_life:
    # Use actual timer later on
    pygame.time.delay(delay_ms)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            win_life = False
'''
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        character_1.move("UP")
    elif keys[pygame.K_RIGHT]:
        character_1.move("RIGHT")
    elif keys[pygame.K_DOWN]:
        character_1.move("DOWN")
    elif keys[pygame.K_LEFT]:
        character_1.move("LEFT")
    character_1.draw()
'''


pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
