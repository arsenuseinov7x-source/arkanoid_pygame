import pygame
import settings as cfg
from screens.game_screen import run as game_screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Arkanoid")
    clock = pygame.time.Clock()

    running = True
    while running:
        # Main Loop
        game_screen(screen, clock, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Press "close" button
                running = False

        # screen.fill(cfg.BLACK)

        pygame.display.flip()   # Screen Update
        clock.tick(cfg.FPS)         # FPS (Frames Per Second)

    pygame.quit()

if __name__ == "__main__":
    main()
