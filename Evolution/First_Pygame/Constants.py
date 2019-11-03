from typing import List, Tuple
from Common_Types import *

# Simulation constants
FILE_NAME: str = "Evolution/Stats/stats_of_run_"

# Window constants
WINDOW_WIDTH: int = 1200
WINDOW_HEIGHT: int = 700
WINDOW_SIZE: Size = Size(WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_TITLE: str = "Evolution Simulator"

# Color pallete
CLEAR_GREY: Color = Color(211, 211, 211)
DARK_GREY: Color = Color(140, 140, 140)
BLACK: Color = Color(0, 0, 0)
WHITE: Color = Color(255, 255, 255)

# Stage constants
STAGE_SIZE: Size = Size(800, 500)
WALLS_DIMENSIONS: Size = Size(((WINDOW_WIDTH-STAGE_SIZE.width)/2),
                              ((WINDOW_HEIGHT-STAGE_SIZE.height)/2))
STAGE_COLORS: Tuple[Color, Color] = (CLEAR_GREY, DARK_GREY)
STAGE_CENTER: Point = Point(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

CLOCK_FONT: Font = Font("Trebuchet MS", 25)
CLOCK_COLOR: Color = BLACK
TEXT_FONT: Font = Font("Trebuchet MS", 15)

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

TEXTBOX_MATRIX = [("", "Time of Round (s):"), (TTL, "5    "),
                  ("", "fps:"), (FPS, "60   "),
                  ("", "Max generations:"), (MAX_GENERATION, "15   "),
                  ("", "# of Characters:"), (CHARACTERS, "30   "),
                  ("", "# of Foods:"), (FOODS, "30   "),
                  ("", "days:"), (DAYS, "0    "),
                  ("", "Oldest generation:"), (OLDEST_GENERATION, "0    "),
                  ("", "Newest generation:"), (NEWEST_GENERATION, "0    "),
                  ("", "Perished yesterday:"), (PERISHED, "0    "),
                  ("", "Newborn:"), (NEWBORN, "0    ")]

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

# Food constants
FOOD_COLOR: Color = WHITE
FOOD_SIZE = Size(5, 5)

# Character constants
REPRODUCTION: int = 50  # 50%
TRAVERSE_CHARACTERS: bool = True
CHARACTER_SIZE = Size(22, 22)

MIN_SPEED = 2
MAX_SPEED = CHARACTER_SIZE.height * 2  # diff = 24
STEP_SPEED = 1  # 24 steps to max
SLOPE_SPEED = 255/(MAX_SPEED-MIN_SPEED)
B_SPEED = SLOPE_SPEED*MIN_SPEED

MIN_SENSING = CHARACTER_SIZE.height * 2  # 44
MAX_SENSING = CHARACTER_SIZE.height * 6  # 132 diff: 88
STEP_SENSING = 4  # 22 steps to max
SLOPE_SENSING = 255/(MAX_SENSING-MIN_SENSING)
B_SENSING = SLOPE_SENSING*MIN_SENSING

MIN_MOVEMENTS = 60
MAX_MOVEMENTS = 200  # diff: 140
STEP_MOVEMENTS = 4  # 32 steps to max
SLOPE_MOVEMENTS = 255/(MAX_MOVEMENTS-MIN_MOVEMENTS)
B_MOVEMENTS = SLOPE_MOVEMENTS*MIN_MOVEMENTS

PROBABILITIES_STEP: List[float] = [0.2, 0.35, 0.45]
STEP_INDEXES: List[int] = range(3)

PROBABILITIES_MUTATIONS: List[float] = [0.1, 0.2, 0.4, 0.2, 0.1]
MUTATIONS_INDEXES: List[int] = range(5)

# Moves constants

INTEREST_POINTS: List[Point] = \
    [STAGE_CENTER,
     Point(WALLS_DIMENSIONS.width,
           WALLS_DIMENSIONS.height),
     Point(WALLS_DIMENSIONS.width + STAGE_SIZE.width,
           WALLS_DIMENSIONS.height),
     Point(WALLS_DIMENSIONS.width,
           WALLS_DIMENSIONS.height + STAGE_SIZE.height),
     Point(WALLS_DIMENSIONS.width + STAGE_SIZE.width,
           WALLS_DIMENSIONS.height + STAGE_SIZE.height)]

POSSIBLE_MOVES: List[Direction] = [Direction(0, -1), Direction(0.5, -0.5),
                                   Direction(1, 0), Direction(0.5, 0.5),
                                   Direction(0, 1), Direction(-0.5, 0.5),
                                   Direction(-1, 0), Direction(-0.5, -0.5)]

MOVES_INDEXES: List[int] = range(8)

PROBABILITIES_MOVES: List[float] = [0.4, 0.2, 0.1, 0, 0, 0, 0.1, 0.2]
