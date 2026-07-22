import pygame

import settings as cfg

class Paddle:
    """ Our main player, Paddle, moves only horizontally. """

    def __init__(self) -> None:
        self.rect = pygame.Rect(0, 0, cfg.PADDLE_WIDTH, cfg.PADDLE_HEIGHT)
        self.rect.midbottom = (cfg.WIDTH // 2, cfg.HEIGHT - 20)
        self.speed = cfg.PADDLE_SPEED
        self.vx = 0
        self.extended = False
        self.laser = False

        self.base_width = cfg.PADDLE_WIDTH
        self.size_effect_end_time = 0  # 0 means "no active size bonus"

    def apply_size_bonus(self, multiplier: float, duration_ms: int) -> None:
        """ Resizes the Paddle for `duration_ms` milliseconds (used by shrink / extend). """
        center = self.rect.center
        self.rect.width = int(self.base_width * multiplier)
        self.rect.center = center
        self.size_effect_end_time = pygame.time.get_ticks() + duration_ms

    def update(self) -> None:
        """ Restores the Paddle's normal size once its size effect expires. """
        if self.size_effect_end_time and pygame.time.get_ticks() >= self.size_effect_end_time:
            center = self.rect.center
            self.rect.width = self.base_width
            self.rect.center = center
            self.size_effect_end_time = 0

    def move(self, keys: pygame.key.ScancodeWrapper):
        """ Moves the Paddle if the key is pressed. """
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.vx = self.speed
        
        self.rect.x += self.vx

        # Restrict the Paddle's movement
        if self.rect.left < cfg.FIELD_LEFT:
            self.rect.left = cfg.FIELD_LEFT
        if self.rect.right > cfg.FIELD_RIGHT:
            self.rect.right = cfg.FIELD_RIGHT

    def draw(self, screen: pygame.Surface) -> None:
        """ Renders the Paddle on the screen. """
        pygame.draw.rect(screen, cfg.PADDLE_COLOR, self.rect, border_radius=5)


class Brick:
    """
        Class for Game's brick.

        HP = -1: Level Boundary
        HP = 0: Indestructable
        HP = 1, 2: One / Two hit
    """
    
    def __init__(self, col: int, row: int, hp: int) -> None:
        self.hp = hp
        self.color = cfg.BRICK_COLORS[hp]
        self.rect = pygame.Rect(
            cfg.FIELD_LEFT + col * cfg.BRICK_WIDTH,
            cfg.TOP_OFFSET + row * cfg.BRICK_HEIGHT,
            cfg.BRICK_WIDTH,
            cfg.BRICK_HEIGHT,
        )

    def draw(self, screen: pygame.Surface) -> None:
        """ Renders a Brick in a certain row and col. """
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, cfg.DARK_GRAY, self.rect, 2)
    
    def hit(self) -> bool:
        """ Handles the Brick Hit. Returns True if the brick was destroyed. """
        if self.hp > 0:
            self.hp -= 1
            if self.hp > 0:
                self.color = cfg.BRICK_COLORS[self.hp]
                return False
            return True
        return False

class Ball:
    """ Ball Actor class. """

    def __init__(self, x: int, y: int) -> None:
        self.base_radius = cfg.BALL_RADIUS
        self.radius = self.base_radius
        self.rect = pygame.Rect(
            x - self.radius,
            y - self.radius,
            2 * self.radius,
            2 * self.radius,
        )
        self.vx = cfg.BALL_SPEED_X
        self.vy = cfg.BALL_SPEED_Y

        self.speed_multiplier = 1.0
        self.speed_effect_end_time = 0  # 0 means "no active speed bonus"
        self.size_effect_end_time = 0  # 0 means "no active size bonus"

    def _set_radius(self, new_radius: int) -> None:
        """ Resizes the Ball's rect around its current center. """
        center = self.rect.center
        self.radius = new_radius
        self.rect = pygame.Rect(0, 0, 2 * self.radius, 2 * self.radius)
        self.rect.center = center

    def update(self) -> None:
        """ Updates the Ball's position for the each frame. """
        self.rect.x += self.vx * self.speed_multiplier
        self.rect.y += self.vy * self.speed_multiplier

        if self.speed_effect_end_time and pygame.time.get_ticks() >= self.speed_effect_end_time:
            self.speed_multiplier = 1.0
            self.speed_effect_end_time = 0

        if self.size_effect_end_time and pygame.time.get_ticks() >= self.size_effect_end_time:
            self._set_radius(self.base_radius)
            self.size_effect_end_time = 0

    def apply_speed_bonus(self, multiplier: float, duration_ms: int) -> None:
        """ Temporarily scales the Ball's speed (used by speed_up / speed_down bonuses). """
        self.speed_multiplier = multiplier
        self.speed_effect_end_time = pygame.time.get_ticks() + duration_ms

    def apply_size_bonus(self, multiplier: float, duration_ms: int) -> None:
        """ Temporarily grows the Ball (used by the grow bonus). """
        self._set_radius(int(self.base_radius * multiplier))
        self.size_effect_end_time = pygame.time.get_ticks() + duration_ms

    def draw(self, screen: pygame.surface) -> None:
        """ Renders the Ball. """
        colour = cfg.BALL_COLOR
        pygame.draw.circle(screen, colour, self.rect.center, self.radius)


class Bonus:
    """ A falling bonus dropped by a destroyed brick. Caught by the Paddle. """

    def __init__(self, x: int, y: int, kind: str) -> None:
        self.kind = kind
        self.rect = pygame.Rect(0, 0, cfg.BONUS_SIZE, cfg.BONUS_SIZE)
        self.rect.center = (x, y)
        self.vy = cfg.BONUS_FALL_SPEED

    def update(self) -> None:
        """ Moves the Bonus down the screen. """
        self.rect.y += self.vy

    def draw(self, screen: pygame.Surface) -> None:
        """ Renders the Bonus as a small labeled square. """
        color = cfg.BONUS_COLORS.get(self.kind, cfg.WHITE)
        pygame.draw.rect(screen, color, self.rect, border_radius=4)
        pygame.draw.rect(screen, cfg.WHITE, self.rect, 2, border_radius=4)