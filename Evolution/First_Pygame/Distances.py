import pygame
import random
import math
from typing import List, Tuple
from collections import deque
from numpy.random import choice

from Rectangle import Rectangle
import Constants
from Common_Types import *


# Returns the Euclidean distance between two points.
def L2(a: Point, b: Point) -> float:
    return math.sqrt(math.pow((a.x-b.x), 2) + math.pow((a.y-b.y), 2))


# Returns the L infinite between two points.
# L infinite is commonly the max, not the min.
def Linf(a: Point, b: Point) -> int:
    return min(abs(a.x-b.x), abs(a.y-b.y))


# Returns the closest corner L2 distance between two Rectangles.
def closest_L2(a: Rectangle, b: Rectangle) -> float:
    a_corners = a.get_corners()
    b_corners = b.get_corners()

    minimum = 10000
    for first in a_corners:
        for second in b_corners:
            current = L2(first, second)
            minimum = min(current, minimum)
    return minimum


# Returns the closest corner Linf distance between two Rectangles.
def closest_Linf(a: Rectangle, b: Rectangle) -> int:
    a_corners = a.get_corners()
    b_corners = b.get_corners()

    minimum = 10000
    for first in a_corners:
        for second in b_corners:
            current = Linf(first, second)
            minimum = min(current, minimum)
    return minimum


# Returns the closest rectangle to a in L2 distance.
def closest_of_all_L2(a: Rectangle, bs: List[Rectangle], r: int) -> Rectangle:
    closest_d = 10000
    center = a.get_center()
    x_min = center.x - r
    x_max = center.x + r
    closest = bs[0]
    for b in bs:
        lim = b.get_limits()
        if lim.x_max < x_min:
            continue
        elif lim.x_min > x_min:
            break
        current_d = closest_L2(a, b)
        if current_d < closest_d:
            closest_d = current_d
            closest = b
    return closest


# Returns the closest rectangle to a in Linf distance.
def closest_of_all_Linf(a: Rectangle, bs: List[Rectangle]) -> Rectangle:
    closest_d = 10000
    closest = bs[0]
    for b in bs:
        current_d = closest_Linf(a, b)
        if current_d < closest_d:
            closest_d = current_d
            closest = b
    return closest


# Returns the direction [dx, dy] from point a to point b.
def direction_to_point(a: Point, b: Point) -> Direction:
    dx = b.x - a.x
    dy = b.y - a.y
    total = abs(dx) + abs(dy)

    if total == 0:
        return Direction(0, 0)
    dx = float(dx) / float(total)
    dy = float(dy) / float(total)

    return Direction(dx, dy)


# Returns the direction [dx, dy] from object a to object b.
# If it's not within the sensing radius r, it returns a random movement.
# It also returns True if it is within the area.
def sensing_direction(a: Rectangle, b: Rectangle, r: int) -> \
        Tuple[Direction, bool]:
    a_center = a.get_center()
    corners = b.get_corners()
    for corner in corners:
        if r < L2(a_center, corner):
            return get_weighted_random_move(a.get_center(),
                                            a.get_direction()), False

    return direction_to_point(a_center, b.get_center()), True


def cardinal_system_direction(a: Rectangle, b: Rectangle) -> Direction:
    corners = b.get_corners()
    vip = a.get_corners()
    vip = vip[0]

    right = 0
    left = 0
    down = 0
    up = 0
    for corner in corners:
        if vip[0] <= corner[0]:
            right += 1
        if vip[0] >= corner[0]:
            left += 1
        if vip[1] <= corner[1]:
            down += 1
        if vip[1] >= corner[1]:
            up += 1

    if right == 4:
        return Direction(1, 0)
    elif left == 4:
        return Direction(-1, 0)
    elif down == 4:
        return Direction(0, 1)
    elif up == 4:
        return Direction(0, -1)
    return get_weighted_random_move(a.get_center(), a.get_direction())


# Returns the index of which direction is the optimal to go.
# 0 = up, 1 = up-right
# 2 = right, 3 = down-right
# 4 = down, 5 = down-left
# 6 = left, 7 = up-left
def index_direction_to_point(a: Point, b: Point) -> int:
    dx, dy = direction_to_point(a, b)
    if -0.25 < dx <= 0.25:  # This means dx = 0 or does not move in x.
        if dy > 0:  # It should go down.
            return 4
        else:  # It should go up.
            return 0
    elif 0.25 < dx <= 0.75:  # This means dx = 0.5 or goes right.
        if dy > 0:  # It should go down.
            return 3
        else:  # It should go up.
            return 1
    elif -0.75 < dx <= -0.25:  # This means dx = -0.5 or goes left.
        if dy > 0:  # It should go down.
            return 5
        else:  # It should go up.
            return 7
    elif 0.75 < dx:  # This means dx = 1 or goes completely right.
        return 2
    else:  # This means dx = -1 or goes completely left.
        return 6


# Returns a random weighted movement towards the direction.
def get_weighted_random_move(a: Point, direction: int) -> Direction:
    index = index_direction_to_point(a, Constants.INTEREST_POINTS[direction])
    index = get_weighted_index(Constants.PROBABILITIES_MOVES,
                               index,
                               Constants.MOVES_INDEXES)
    return Constants.POSSIBLE_MOVES[index]


def get_weighted_index(probabilities: List[float],
                       rotate_index: int,
                       choices: List[int]) -> int:
    probabilities = deque(probabilities)
    probabilities.rotate(rotate_index)
    return choice(choices, 1, False, probabilities)[0]


def smart_collide(character: Rectangle, foods: List[Rectangle]) -> List[int]:
    indexes = []
    lim = character.get_limits()
    for i in range(len(foods)):
        f_lim = foods[i].get_limits()
        if f_lim.x_max < lim.x_min:
            continue
        elif f_lim.x_min > lim.x_max:
            return indexes
        if character.collides(foods[i]):
            indexes.append(i)
    return indexes
