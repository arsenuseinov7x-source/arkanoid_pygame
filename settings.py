"""settings.py – static config for in-game variables.

No logic here.
Feel free to experiment with variables.
"""

from pathlib import Path

# --- Paths -------------------------------------------------------------------
# Relative paths to resolve file names
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
LEVELS_DIR = BASE_DIR / "levels"

# --- Screen, Timer -----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

# --- Playing Field -------------------------------------------------------------
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
TOP_OFFSET = 60  # Top Offset for UI status bar
FIELD_LEFT = 40  # Left Offset for bricks 

# Calculation of the playing field rows and cols
FIELD_COLS = (WIDTH - 2 * FIELD_LEFT) // BRICK_WIDTH
FIELD_RIGHT = FIELD_LEFT + FIELD_COLS * BRICK_WIDTH

# --- Paddle, Ball -----------------------------------------------------------
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 12
PADDLE_SPEED = 7

BALL_RADIUS = 8
BALL_SPEED_X = 4
BALL_SPEED_Y = -5
SLIDE_FACTOR = 0.8
MAX_BALL_SPEED_X = 8

# --- Bonuses ---------------------------------------------------------------------
BONUS_PROBABILITY = 0.3  # Chance that destroyed brick will drop a bonus
BONUS_TYPES = ["shrink", "extend", "grow", "speed_up", "speed_down"]

BONUS_SIZE = 20  # Falling bonus square size
BONUS_FALL_SPEED = 3  # How fast the bonus falls down
BONUS_DURATION = 6000  # ms, how long a bonus effect lasts once caught
BONUS_SPEED_UP_FACTOR = 1.6
BONUS_SPEED_DOWN_FACTOR = 0.6
BONUS_PADDLE_SHRINK_FACTOR = 0.5  # Paddle width multiplier while shrunk
BONUS_PADDLE_EXTEND_FACTOR = 1.6  # Paddle width multiplier while extended
BONUS_BALL_GROW_FACTOR = 1.7  # Ball radius multiplier while grown

# --- Lives / Game state --------------------------------------------------------
STARTING_LIVES = 3

# --- Visual Effects -----------------------------------------------------------
TRAIL_LENGTH = 6  # Ball's Motion Trail Length
PARTICLE_COUNT = 10  # Particles in brick's burst
PARTICLE_LIFETIME = (12, 24)  # Min/max frames for the partivle to live
PARTICLE_SPEED = (1.5, 4.0)  # Min/max parrticle speed
PARTICLE_GRAVITY = 0.15  # Particle's acceleration
MAX_PARTICLES = 200  # Max particles number

# --- Colors -------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (60, 60, 60)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PADDLE_COLOR = CYAN
BALL_COLOR = WHITE

# Brick Color and HP
BRICK_COLORS = {
    2: ORANGE,
    1: RED,
    0: GRAY, # Indestructable brick
    -1: DARK_GRAY,  # Indestructable Level Boundaries
}

# Bonus Colors
BONUS_COLORS = {
    "shrink": RED,
    "extend": GREEN,
    "grow": MAGENTA,
    "speed_up": ORANGE,
    "speed_down": CYAN,
}