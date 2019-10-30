import pygame
import random
from typing import List, Tuple

import Rectangle
from Character import Character
from Food import Food
import Clock
import Stage
import TextBox


# Spans the selected amount of food randomly throughout the stage,
# avoiding collisions.
def span_random_foods(amount: int, delimiter: Rectangle.Rectangle,
                      width: int, height: int, color: List[int],
                      background_color: List[int], win: pygame.Surface,
                      blockings: List[Character],
                      nutritional_value: int) -> List[Food]:
    foods = list()
    min_x = delimiter.rectangle.x
    min_y = delimiter.rectangle.y
    max_x = delimiter.rectangle.x + delimiter.rectangle.width - width
    max_y = delimiter.rectangle.y + delimiter.rectangle.height - height

    while len(foods) < amount:
        current_x = random.randint(min_x, max_x)
        current_y = random.randint(min_y, max_y)

        current_rectangle = pygame.Rect(current_x, current_y, width, height)
        blocks = False
        for blocking in blockings:
            if current_rectangle.colliderect(blocking.rectangle) is True:
                blocks = True
                break

        for food in foods:
            if current_rectangle.colliderect(food.rectangle) is True:
                blocks = True
                break

        if blocks is False:
            foods.append(Food(1, current_x, current_y, width, height,
                              color, background_color, win, nutritional_value))

    return foods


# Spans the selected amount of characters randomly throughout the stage,
# avoiding collisions.
def span_random_characters(amount: int, delimiter: Rectangle.Rectangle,
                           width: int, height: int, color: List[int],
                           background_color: List[int],
                           win: pygame.Surface, speed: int,
                           sensing_range: int) -> List[Character]:
    characters = list()
    min_x = delimiter.rectangle.x
    min_y = delimiter.rectangle.y
    max_x = delimiter.rectangle.x + delimiter.rectangle.width - width
    max_y = delimiter.rectangle.y + delimiter.rectangle.height - height

    while len(characters) < amount:
        current_x = random.randint(min_x, max_x)
        current_y = random.randint(min_y, max_y)

        current_rectangle = pygame.Rect(current_x, current_y, width, height)
        blocks = False
        for character in characters:
            if current_rectangle.colliderect(character.rectangle) is True:
                blocks = True
                break

        if blocks is False:
            characters.append(Character(current_x, current_y, width, height,
                                        color, background_color, win,
                                        1, speed, sensing_range))

    return characters


# Returns the blockings for the current index.
def get_blockings(characters: List[Character],
                  walls: List[Rectangle.Rectangle],
                  current: int) -> List[Rectangle.Rectangle]:
    left_hand = characters[:current]
    right_hand = characters[current+1:]
    return left_hand + right_hand + walls


def goto_closer_wall(character: Character,
                     walls: List[Rectangle.Rectangle]) -> Tuple[int, int]:
    wall = Rectangle.closest_of_all_Linf(character, walls)
    movement = Rectangle.cardinal_system_direction(character, wall)
    if character.would_collide(wall, movement):
        character.arrived_home()
        character.move_home()
        return (0, 0)
    return movement


def goto_closer_food(character: Character,
                     foods: List[Food]) -> Tuple[int, int]:
    if len(foods) is 0:
        return character.get_random_move()
    food = Rectangle.closest_of_all_L2(character, foods)
    return Rectangle.sensing_direction(character, food,
                                       character.get_sensing())


def get_direction(character: Character, walls: List[Rectangle.Rectangle],
                  foods: List[Food]) -> Tuple[int, int]:
    if (character.is_hungry() is False):
        return goto_closer_wall(character, walls)
    return goto_closer_food(character, foods)
    return character.get_random_move()


# Moves the character a certain dx and dy times its own speed, plus
# checks on the foods and eats if the character is hungry.
def move_character(character: Character, dx: int, dy: int,
                   blockings: List[Rectangle.Rectangle], foods: List[Food]):
    character.move(dx, dy, blockings)
    counter = 0
    fed = False
    if character.is_hungry():
        for food in foods:
            if character.rectangle.colliderect(food.rectangle):
                character.feed(food.get_nutritional_value())
                fed = True
                break
            counter += 1
        if fed:
            del foods[counter]
            character.draw()


# Moves all the characters on the list and some may eat some food.
def move_characters(number_of_characters: int, characters: List[Character],
                    foods: List[Food], walls: List[Rectangle.Rectangle]):
    for i in range(number_of_characters):
        if characters[i].finished() is False:
            movement = get_direction(characters[i], walls, foods)
            move_character(characters[i], movement[0], movement[1],
                           get_blockings(characters, walls, i), foods)
    for food in foods:
        food.draw()


def initialize_text_boxes(position: Tuple[int, int],
                          font: Tuple[str, int],
                          colors: Tuple[List[int], List[int]],
                          win: pygame.Surface) -> List[TextBox.TextBox]:
    text_boxes = list()
    text_boxes.append(TextBox.TextBox(position, colors[1], colors[0],
                                      True, colors[0], font[0], font[1],
                                      False, win, "# of Characters:"))
    current_x, current_y = position
    position = (current_x + (text_boxes[-1].get_size())[0] + 5, current_y)
    text_boxes.append(TextBox.TextBox(position, colors[0], colors[1],
                                      False, colors[0], font[0], font[1],
                                      True, win, "100"))
    position = (current_x, current_y + (text_boxes[-1].get_size())[1] + 10)
    text_boxes.append(TextBox.TextBox(position, colors[1], colors[0],
                                      True, colors[0], font[0], font[1],
                                      False, win, "# of Foods:"))
    position = (current_x + (text_boxes[-1].get_size())[0] + 5,
                current_y + (text_boxes[-1].get_size())[1] + 10)
    text_boxes.append(TextBox.TextBox(position, colors[0], colors[1],
                                      False, colors[0], font[0], font[1],
                                      True, win, "100"))

    return text_boxes


def initialize_stage(stage_size: Tuple[int, int],
                     stage_colors: Tuple[List[int], List[int]],
                     fps: int, clock_position: Tuple[int, int],
                     clock_font: Tuple[str, int], clock_font_color: List[int],
                     ttl: int,
                     text_position: Tuple[int, int],
                     text_font: Tuple[str, int],
                     text_colors: Tuple[List[int], List[int]],
                     win: pygame.Surface) -> Stage.Stage:
    clock = Clock.Clock(fps, clock_position, stage_colors[0], stage_colors[1],
                        clock_font[0], clock_font[1], clock_font_color,
                        ttl, win)

    width, height = win.get_size()
    text_initial_width = stage_size[0]+((width-stage_size[0])/2)+10
    text_initial_height = (height-stage_size[1])/2
    text_pos = (text_initial_width, text_initial_height)
    text_boxes = initialize_text_boxes(text_pos, text_font, text_colors, win)

    stage = Stage.Stage(stage_size[0], stage_size[1],
                        stage_colors[0], stage_colors[1],
                        win, clock, text_boxes)
    pygame.display.update()
    return stage


def wait_for_enter(stage: Stage.Stage):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            stage.check_box(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def load_state(stage: Stage.Stage) -> List[int]:
    wait_for_enter(stage)
    return stage.get_text_values()
