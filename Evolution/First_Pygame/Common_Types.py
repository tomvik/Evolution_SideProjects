from typing import NamedTuple


class Color(NamedTuple):
    red: int
    green: int
    blue: int


class Point(NamedTuple):
    x: int
    y: int


class Size(NamedTuple):
    width: int
    height: int


class PointSize(NamedTuple):
    x: int
    y: int
    width: int
    height: int


class Corners(NamedTuple):
    top_left: int
    top_right: int
    bottom_right: int
    bottom_left: int


class Limits(NamedTuple):
    x_min: int
    y_min: int
    x_max: int
    y_max: int


class Direction(NamedTuple):
    dx: float
    dy: float


class Font(NamedTuple):
    letter: str
    size: int


class KeyValue(NamedTuple):
    key: str
    value: int
