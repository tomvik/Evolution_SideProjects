from typing import List, Tuple

# Simulation constants
FILE_NAME: str = "Evolution/Stats/stats_of_run_"

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

CHARACTERS = "Characters"
FOODS = "Foods"
TTL = "Ttl"
FPS = "Fps"
DAYS = "Days"
MAX_GENERATION = "Max_Generations"
OLDEST_GENERATION = "Oldest_Generation"
NEWEST_GENERATION = "Newest_Generation"
PERISHED = "Perished"
NEWBORN = "Newborn"

TEXTBOX_MATRIX_IS_INPUT = [False, True,
                           False, True,
                           False, True,
                           False, True,
                           False, True,
                           False, False,
                           False, False,
                           False, False,
                           False, False,
                           False, False]

TEXTBOX_MATRIX = [("", "Time of Round (s):"), (TTL, "5  "),
                  ("", "fps:"), (FPS, "40 "),
                  ("", "Max generations:"), (MAX_GENERATION, "10 "),
                  ("", "# of Characters:"), (CHARACTERS, "50 "),
                  ("", "# of Foods:"), (FOODS, "50 "),
                  ("", "days:"), (DAYS, "0  "),
                  ("", "Oldest generation:"), (OLDEST_GENERATION, "0  "),
                  ("", "Newest generation:"), (NEWEST_GENERATION, "0  "),
                  ("", "Perished yesterday:"), (PERISHED, "0  "),
                  ("", "Newborn:"), (NEWBORN, "0  ")]

INSTRUCTIONS_TEXTBOXES = [("", "Pre-game Instructions:"), ("", " "),
                          ("", "Input the data into"), ("", " "),
                          ("", "the boxes and"), ("", " "),
                          ("", "afterwards press enter."), ("", " "),
                          ("", " "), ("", " "),
                          ("", "In-game Instructions:"), ("", " "),
                          ("", "Key:  "), ("", "Effect:"),
                          ("", "Exit   "), ("", "Quit the game"),
                          ("", "Space "), ("", "End the round")]

INSTRUCTIONS_INPUT = [False] * len(INSTRUCTIONS_TEXTBOXES)


# Character constants
REPRODUCTION: int = 50  # 50%
TRAVERSE_CHARACTERS: bool = True

# Food constants
FOOD_COLOR: List[int] = WHITE
