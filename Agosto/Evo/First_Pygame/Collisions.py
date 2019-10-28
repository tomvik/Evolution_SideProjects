import matplotlib.path as mplPath
import numpy as np

import Coordinate
import Dimensions
import PositionAndDimension
import Character

# Returns line in form of (m, b) y = mx +b
# Y = MX + B
# M = (by-ay/bx-ax)
# B = ay - (by-ay/bx-ax)ax
# TODO: x != x


def line_for(a, b):
    m = (b.y - a.y)/(b.x - a.x)
    b = a.y - (m * a.x)
    return (m, b)


def collision_coordinate(line_a, line_b):
    Xp = (b[1] - a[1]) / (a[0] - b[0])
    Yp = (a[0] * Xp) + a[1]
    return Coordinate(Xp, Yp)


def is_point_between_points(a, b, vip):
    if (a.x <= vip.x <= b.x or a.x >= vip.x >= b.x):
        if (a.y <= vip.y <= b.y or a.y >= vip.x >= b.y):
            return True
    return False


def is_point_inside_character(character, vip):
    a, b = character.get_vertex_limits()
    return is_point_between_points(a, b, vip)


def is_collision(character_a, character_b):
    b_vertices = character_b.get_vertices()
    for v in b_vertices:
        if is_point_inside_character(character_a, v):
            return True
    return False


# First element is slope, second is offset.
# Point equal:
# M1X1 + B1 - Y1 == M2X2 + B2 - Y2
# (X1, Y1) == (X2, Y2)
# M1X + B1 - Y == M2X + B2 -Y
# M1X + B1 == M2X + B2
# (M1 - M2)*X == B2 - B1
# Xp = (B2 - B1) / (M1 - M2)
# Yp = M1Xp + B1
# IF Xp BETWEEN (X1 AND X2) AND Yp BETWEEN (Y1 AND Y2)
# TRUE
# TODO: Slopes can't be the same
