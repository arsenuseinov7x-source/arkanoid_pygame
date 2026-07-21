import pygame
from game.entities import Paddle

def run(screen: pygame.Surface, clock: pygame.time.Clock, level: int) -> None:
    paddle = Paddle()

    paddle.draw(screen)
