import pygame
import settings as cfg
from screens.game_screen import run as game_screen
from game.entities import Paddle, Brick, Ball

def _bounce_off_rect(ball: Ball, rect: pygame.Rect):
    """ Checks if the Ball collides with the given rect. """

    # Calculate ball's overlaps and find the smallest one
    overlap_left = ball.rect.right - rect.left
    overlap_right = rect.right - ball.rect.left
    overlap_top = ball.rect.bottom - rect.top
    overlap_bottom = rect.bottom - ball.rect.top

    min_overlap = min(
        overlap_bottom,
        overlap_left,
        overlap_right,
        overlap_top)
    
    # Calculate the Ball's final velocities
    if min_overlap == overlap_top and ball.vy > 0:
        ball.rect.bottom = rect.top
        ball.vy *= -1
    elif min_overlap == overlap_bottom and ball.vy < 0:
        ball.rect.top = rect.bottom
        ball.vy *= -1
    elif min_overlap == overlap_left and ball.vx > 0:
        ball.rect.right = rect.left
        ball.vx *= -1
    elif min_overlap == overlap_right and ball.vy < 0:
        ball.rect.left = rect.right
        ball.vx *= -1


def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Arkanoid")
    clock = pygame.time.Clock()

    running = True
    paddle = Paddle()
    bricks = [
        Brick(2, 2, 1),
        Brick(1, 5, 2),
        Brick(2, 1, 0),
        Brick(0, 0, -1)
    ]
    ball = Ball(cfg.WIDTH // 2, cfg.HEIGHT // 2)

    while running:
        # Main Loop
        screen.fill(cfg.BLACK)

        # Update Section
        keys = pygame.key.get_pressed()

        paddle.move(keys)
        ball.update()

        # Draw Section
        paddle.draw(screen)
        ball.draw(screen)

        for brick in bricks:
            _bounce_off_rect(ball, brick.rect)
            brick.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Press "close" button
                running = False

        pygame.display.flip()   # Screen Update
        clock.tick(cfg.FPS)         # FPS (Frames Per Second)

    pygame.quit()

if __name__ == "__main__":
    main()