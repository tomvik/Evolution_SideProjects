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

CHARACTERS_NAME = "Characters"
FOODS_NAME = "Foods"
TTL_NAME = "Ttl"
FPS_NAME = "Fps"
DAYS_NAME = "Days"
MAX_GENERATION_NAME = "Max_Generations"

TEXTBOX_MATRIX_IS_INPUT = [False, False,
                           False, False,
                           False, False,
                           False, False,
                           False, False,
                           False, True,
                           False, True,
                           False, True,
                           False, True,
                           False, True,
                           False, False,
                           False, False,
                           False, False,
                           False, False,
                           False, False,
                           False, False]

TEXTBOX_MATRIX = [("", "Pre-game Instructions:"), ("", " "),
                  ("", "Input the data into"), ("", " "),
                  ("", "the boxes and"), ("", " "),
                  ("", "afterwards press enter."), ("", " "),
                  ("", " "), ("", " "),
                  ("", "# of Characters:"), (CHARACTERS_NAME, "50 "),
                  ("", "# of Foods:"), (FOODS_NAME, "50 "),
                  ("", "Time of Round (s):"), (TTL_NAME, "5  "),
                  ("", "fps:"), (FPS_NAME, "40 "),
                  ("", "Max generations:"), (MAX_GENERATION_NAME, "10 "),
                  ("", "days:"), (DAYS_NAME, "0  "),
                  ("", " "), ("", " "),
                  ("", "In-game Instructions:"), ("", " "),
                  ("", "Key:  "), ("", "Effect:"),
                  ("", "Exit   "), ("", "Quit the game"),
                  ("", "Space "), ("", "End the round")]


# Character constants
REPRODUCTION: int = 50  # 50%
TRAVERSE_CHARACTERS: bool = True

# Food constants
FOOD_COLOR: List[int] = WHITE
