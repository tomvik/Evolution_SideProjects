import pygame
import random
from typing import List, Tuple

import Rectangle
from Character import Character
from Food import Food
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
def move_characters(characters: List[Character], foods: List[Food],
                    walls: List[Rectangle.Rectangle]):
    for i in range(len(characters)):
        if characters[i].finished() is False:
            movement = get_direction(characters[i], walls, foods)
            move_character(characters[i], movement[0], movement[1],
                           get_blockings(characters, walls, i), foods)
    for food in foods:
        food.draw()


# Initializes the stage.
def initialize_stage(stage_size: Tuple[int, int],
                     stage_colors: Tuple[List[int], List[int]],
                     fps: int, clock_position: Tuple[int, int],
                     clock_font: Tuple[str, int], clock_font_color: List[int],
                     ttl: int,
                     text_position: Tuple[int, int],
                     text_font: Tuple[str, int],
                     text_colors: Tuple[List[int], List[int]],
                     win: pygame.Surface) -> Stage.Stage:
    stage = Stage.Stage(stage_size[0], stage_size[1],
                        stage_colors[0], stage_colors[1],
                        win, fps, clock_font,
                        clock_font_color, ttl, text_font)
    pygame.display.update()
    return stage


def initialize_characters_and_food(stage: Stage.Stage, character_size: int,
                                   character_color: List[int],
                                   character_speed: int,
                                   character_sensing: int,
                                   food_size: int,
                                   food_color: List[int],
                                   food_value: int) -> Tuple[List[Character],
                                                             List[Food]]:
    print("Select amount of characters and foods. Afterwards, press enter")
    wait_for_enter(stage)
    number_of_characters, number_of_foods = load_state(stage)

    characters = span_random_characters(number_of_characters,
                                        stage.get_stage(),
                                        character_size,
                                        character_size,
                                        character_color,
                                        stage.get_stage_color(),
                                        stage.get_win(),
                                        character_speed,
                                        character_sensing)

    foods = span_random_foods(number_of_foods,
                              stage.get_stage(),
                              food_size,
                              food_size,
                              food_color,
                              stage.get_stage_color(),
                              stage.get_win(),
                              characters,
                              food_value)
    return characters, foods


def wait_for_enter(stage: Stage.Stage):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            stage.check_box(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


def load_state(stage: Stage.Stage) -> List[int]:
    return stage.get_text_values()
