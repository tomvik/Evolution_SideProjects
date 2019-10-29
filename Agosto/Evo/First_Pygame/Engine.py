import pygame
import random
from typing import List, Tuple

import Color
import Rectangle
from Character import Character
from Food import Food


# Spans the selected amount of food randomly throughout the stage,
# avoiding collisions.
def span_random_foods(amount: int, delimiter: Rectangle.Rectangle,
                      width: int, height: int, color: Color.RBGColor,
                      background_color: Color.RBGColor, win: pygame.Surface,
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
                           width: int, height: int, color: Color.RBGColor,
                           background_color: Color.RBGColor,
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
    return Rectangle.cardinal_system_direction(character, wall)


def goto_closer_food(character: Character,
                     foods: List[Food]) -> Tuple[int, int]:
    possible_movements = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    if len(foods) is 0:
        return random.choice(possible_movements)
    food = Rectangle.closest_of_all_L2(character, foods)
    return Rectangle.sensing_direction(character, food,
                                       character.get_sensing())


def get_direction(character: Character, walls: List[Rectangle.Rectangle],
                  foods: List[Food]) -> Tuple[int, int]:
    if (character.is_hungry() is False):
        return goto_closer_wall(character, walls)
    return goto_closer_food(character, foods)
    return random.choice([(0, -1), (1, 0), (0, 1), (-1, 0)])


# Moves the character a certain dx and dy times its own speed, plus
# checks on the foods and eats if the character is hungry.
def move_character(character: Character, dx: int, dy: int,
                   blockings: List[Rectangle.Rectangle], foods: List[Food]):
    character.move(dx, dy, blockings)
    counter = 0
    fed = False
    if character.get_hunger() is not 0:
        for food in foods:
            if character.rectangle.colliderect(food.rectangle):
                character.feed(food.get_nutritional_value())
                fed = True
                break
            counter += 1
        if fed:
            print("Someone ate")
            del foods[counter]
            character.draw()


# Moves all the characters on the list and some may eat some food.
def move_characters(number_of_characters: int, characters: List[Character],
                    foods: List[Food], walls: List[Rectangle.Rectangle]):
    for i in range(number_of_characters):
        movement = get_direction(characters[i], walls, foods)
        move_character(characters[i], movement[0], movement[1],
                       get_blockings(characters, walls, i), foods)
    for food in foods:
        food.draw()
