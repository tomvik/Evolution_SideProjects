from typing import List, Tuple

# Window constants
WINDOW_WIDTH: int = 1200
WINDOW_HEIGHT: int = 700
WINDOW_SIZE: Tuple[int, int] = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_TITLE: str = "Evolution Simulator"
WINDOW_CENTER: Tuple[int, int] = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

# Color pallete
CLEAR_GREY: List[int] = [211, 211, 211]
DARK_GREY: List[int] = [140, 140, 140]
BLACK: List[int] = [0, 0, 0]
WHITE: List[int] = [255, 255, 255]

# Stage constants
STAGE_COLORS: Tuple[List[int], List[int]] = (CLEAR_GREY, DARK_GREY)
STAGE_SIZE: Tuple[int, int] = (800, 500)

CLOCK_FONT: Tuple[str, int] = ("Trebuchet MS", 25)
CLOCK_COLOR: List[int] = BLACK
TEXT_FONT: Tuple[str, int] = ("Trebuchet MS", 15)

# Character constants
REPRODUCTION: int = 50  # 50%

# Food constants
FOOD_COLOR: List[int] = WHITE
