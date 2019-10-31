import pygame
import random
import math
from typing import List, Tuple

from Rectangle import Rectangle


# Returns the Euclidean distance between two points.
def L2(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    return math.sqrt(math.pow((a[0]-b[0]), 2) + math.pow((a[1]-b[1]), 2))


# Returns the L infinite between two points.
# L infinite is commonly the max, not the min.
def Linf(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return min(abs(a[0]-b[0]), abs(a[1]-b[1]))


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
def closest_of_all_L2(a: Rectangle, bs: List[Rectangle]) -> Rectangle:
    closest_d = 10000
    closest = bs[0]
    for b in bs:
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


# Returns the direction [dx, dy] from object a to object b.
# If it's not within the sensing radius r, it returns a random movement.
def sensing_direction(a: Rectangle, b: Rectangle, r: int) -> Tuple[int, int]:
    a_center = a.get_rectangle().center
    corners = b.get_corners()
    for corner in corners:
        if r < L2(a_center, corner):
            return a.get_random_move()

    b_center = b.get_rectangle().center
    move_x = b_center[0] - a_center[0]
    move_y = b_center[1] - a_center[1]
    total = abs(move_x) + abs(move_y)

    if total == 0:
        return (0, 0)
    move_x = float(move_x) / float(total)
    move_y = float(move_y) / float(total)

    return (move_x, move_y)


def cardinal_system_direction(a: Rectangle, b: Rectangle) -> Tuple[int, int]:
    corners = b.get_corners()
    vip = a.get_corners()
    vip = vip[0]

    right = 0
    left = 0
    down = 0
    up = 0
    for corner in corners:
        if vip[0] < corner[0]:
            right += 1
        if vip[0] > corner[0]:
            left += 1
        if vip[1] < corner[1]:
            down += 1
        if vip[1] > corner[1]:
            up += 1

    if right == 4:
        return (1, 0)
    elif left == 4:
        return (-1, 0)
    elif down == 4:
        return (0, 1)
    elif up == 4:
        return (0, -1)
    return a.get_random_move()
