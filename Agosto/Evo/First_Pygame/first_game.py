import pygame

import Color
import Coordinate
import Dimensions
import StartAndDimension
import Character

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
start_and_dimension_1 = StartAndDimension.StartAndDimension(coordinate_1,
                                                            dimension_1)

color_1 = Color.RBGColor(255, 0, 0)

character_1 = Character.Character(
    start_and_dimension_1, color_1, background_color, vel, win)
# character_1.DrawItself(win)
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
