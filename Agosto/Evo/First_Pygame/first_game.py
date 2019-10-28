import pygame
import random

import Color
import Character
import Collisions

pygame.init()

delay_ms = 100
background_color = Color.RBGColor(0, 0, 0)
win_heigth = 700
win_width = 1200
win_title = "First game"
win_life = True

vel = 5
possible_movements = ["UP", "RIGHT", "DOWN", "LEFT"]
number_of_characters = 2
characters = []
mov = []

win = pygame.display.set_mode((win_width, win_heigth))
pygame.display.set_caption(win_title)

window_rect = pygame.Rect(0, 0, win_width, win_heigth)
rect_1 = pygame.Rect(50, 50, 10, 15)
rect_2 = pygame.Rect(120, 50, 10, 15)

color_1 = Color.RBGColor(255, 0, 0)
color_2 = Color.RBGColor(0, 0, 255)

characters.append(Character.Character(
    rect_1, color_1, background_color, vel, win))
characters.append(Character.Character(
    rect_2, color_2, background_color, vel, win))

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
            and characters[0].is_move_possible("UP", window_rect):
        characters[0].move("UP")
    elif keys[pygame.K_RIGHT] \
            and characters[0].is_move_possible("RIGHT", window_rect):
        characters[0].move("RIGHT")
    elif keys[pygame.K_DOWN] \
            and characters[0].is_move_possible("DOWN", window_rect):
        characters[0].move("DOWN")
    elif keys[pygame.K_LEFT] \
            and characters[0].is_move_possible("LEFT", window_rect):
        characters[0].move("LEFT")
'''
    for i in range(number_of_characters):
        mov[i] = random.choice(possible_movements)
        while characters[i].is_move_possible(mov[i], window_rect) is False:
            mov[i] = random.choice(possible_movements)
        characters[i].move(mov[i])
'''

pygame.display.update()
pygame.time.delay(delay_ms)
pygame.quit()
