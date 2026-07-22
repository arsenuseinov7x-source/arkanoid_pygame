import random
 
import pygame
import settings as cfg
from screens.game_screen import run as game_screen
from game.entities import Paddle, Brick, Ball, Bonus
from game.level import load_level
from game.sound import SoundManager
 
PLAYING = "playing"
GAME_OVER = "game_over"
WIN = "win"
 
 
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
    elif min_overlap == overlap_right and ball.vx < 0:
        ball.rect.left = rect.right
        ball.vx *= -1
 
 
def _handle_ball_vs_bricks(
    ball: Ball,
    bricks: list[Brick],
    bonuses: list[Bonus],
    sounds: SoundManager,
) -> int:
 
    scored = 0
    for brick in bricks[:]:
        if not ball.rect.colliderect(brick.rect):
            continue
        _bounce_off_rect(ball, brick.rect)
        if brick.hp == -1:
            continue
        destroyed = brick.hit()
        sounds.play("hit")
 
        if destroyed:
            bricks.remove(brick)
            scored += 10
            if random.random() < cfg.BONUS_PROBABILITY:
                kind = random.choice(cfg.BONUS_TYPES)
                bonuses.append(Bonus(brick.rect.centerx, brick.rect.centery, kind))
    return scored
 
 
def _handle_ball_vs_paddle(ball: Ball, paddle: Paddle) -> None:
    """ Handles Ball bounce over the Paddle. """
    _bounce_off_rect(ball, paddle.rect)
    offset = (ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
    max_vx = cfg.MAX_BALL_SPEED_X
    ball.vx = max(-max_vx, min(max_vx, offset * max_vx))
 
 
def _apply_bonus(kind: str, paddle: Paddle, ball: Ball) -> None:
    """ Applies the effect of a caught bonus. """
    if kind == "shrink":
        paddle.apply_size_bonus(cfg.BONUS_PADDLE_SHRINK_FACTOR, cfg.BONUS_DURATION)
    elif kind == "extend":
        paddle.apply_size_bonus(cfg.BONUS_PADDLE_EXTEND_FACTOR, cfg.BONUS_DURATION)
    elif kind == "grow":
        ball.apply_size_bonus(cfg.BONUS_BALL_GROW_FACTOR, cfg.BONUS_DURATION)
    elif kind == "speed_up":
        ball.apply_speed_bonus(cfg.BONUS_SPEED_UP_FACTOR, cfg.BONUS_DURATION)
    elif kind == "speed_down":
        ball.apply_speed_bonus(cfg.BONUS_SPEED_DOWN_FACTOR, cfg.BONUS_DURATION)
 
 
def _update_bonuses(
    bonuses: list[Bonus],
    paddle: Paddle,
    ball: Ball,
    sounds: SoundManager,
) -> None:
    """ Moves falling bonuses, handles catching them or letting them fall off-screen. """
    for bonus in bonuses[:]:
        bonus.update()
 
        if bonus.rect.colliderect(paddle.rect):
            _apply_bonus(bonus.kind, paddle, ball)
            sounds.play("bonus")
            bonuses.remove(bonus)
        elif bonus.rect.top > cfg.HEIGHT:
            bonuses.remove(bonus)
 
 
def _draw_hud(screen: pygame.Surface, font: pygame.font.Font, score: int, lives: int, muted: bool) -> None:
    """ Draws score, lives and mute status along the top of the screen. """
    score_surface = font.render(f"Score: {score}", True, cfg.WHITE)
    screen.blit(score_surface, (cfg.FIELD_LEFT, 10))
 
    lives_surface = font.render(f"Lives: {lives}", True, cfg.WHITE)
    lives_rect = lives_surface.get_rect(midtop=(cfg.WIDTH // 2, 10))
    screen.blit(lives_surface, lives_rect)
 
    mute_label = f"Mute: {'ON' if muted else 'OFF'}  (M)"
    mute_color = cfg.RED if muted else cfg.GRAY
    mute_surface = font.render(mute_label, True, mute_color)
    mute_rect = mute_surface.get_rect(topright=(cfg.WIDTH - 10, 10))
    screen.blit(mute_surface, mute_rect)
 
 
def _draw_center_message(screen: pygame.Surface, big_font: pygame.font.Font, small_font: pygame.font.Font,
                          title: str, color: tuple, score: int) -> None:
    """ Draws a translucent overlay with a title, final score and restart hint. """
    overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
 
    title_surface = big_font.render(title, True, color)
    title_rect = title_surface.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 - 40))
    screen.blit(title_surface, title_rect)
 
    score_surface = small_font.render(f"Final score: {score}", True, cfg.WHITE)
    score_rect = score_surface.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 10))
    screen.blit(score_surface, score_rect)
 
    hint_surface = small_font.render("Press R to Restart or ESC to Quit", True, cfg.GRAY)
    hint_rect = hint_surface.get_rect(center=(cfg.WIDTH // 2, cfg.HEIGHT // 2 + 50))
    screen.blit(hint_surface, hint_rect)
 
 
def _bricks_remaining(bricks: list[Brick]) -> int:
    """ Counts destructible bricks left (ignores indestructible / boundary bricks). """
    return sum(1 for brick in bricks if brick.hp > 0)
 
 
def main():
    pygame.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption("Arkanoid")
    clock = pygame.time.Clock()
    hud_font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 64)
    small_font = pygame.font.SysFont(None, 28)
 
    sounds = SoundManager()
 
    def new_game():
        bricks, rows, cols = load_level(1)
        return {
            "state": PLAYING,
            "paddle": Paddle(),
            "ball": Ball(cfg.WIDTH // 2, cfg.HEIGHT),
            "bricks": bricks,
            "bonuses": [],
            "score": 0,
            "lives": cfg.STARTING_LIVES,
        }
 
    def reset_after_life_lost(g):
        g["paddle"] = Paddle()
        g["ball"] = Ball(cfg.WIDTH // 2, cfg.HEIGHT)
        g["bonuses"] = []
 
    game = new_game()
    running = True
 
    while running:
        screen.fill(cfg.BLACK)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sounds.toggle_mute()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game["state"] != PLAYING:
                    game = new_game()
 
        if game["state"] == PLAYING:
            keys = pygame.key.get_pressed()
            paddle = game["paddle"]
            ball = game["ball"]
            bricks = game["bricks"]
            bonuses = game["bonuses"]
 
            paddle.move(keys)
            paddle.update()
 
            game["score"] += _handle_ball_vs_bricks(ball, bricks, bonuses, sounds)
            _update_bonuses(bonuses, paddle, ball, sounds)
 
            if ball.rect.colliderect(paddle.rect) and ball.vy > 0:
                _handle_ball_vs_paddle(ball, paddle)
 
            ball.update()
 
            # Ball fell below the paddle -> lose a life
            if ball.rect.top > cfg.HEIGHT:
                game["lives"] -= 1
                if game["lives"] <= 0:
                    game["state"] = GAME_OVER
                else:
                    reset_after_life_lost(game)
 
            # All destructible bricks cleared -> win
            elif _bricks_remaining(bricks) == 0:
                game["state"] = WIN
 
            for brick in bricks:
                brick.draw(screen)
            paddle.draw(screen)
            ball.draw(screen)
            for bonus in bonuses:
                bonus.draw(screen)
 
            _draw_hud(screen, hud_font, game["score"], game["lives"], sounds.muted)
 
        else:
            for brick in game["bricks"]:
                brick.draw(screen)
            game["paddle"].draw(screen)
            game["ball"].draw(screen)
            _draw_hud(screen, hud_font, game["score"], game["lives"], sounds.muted)
 
            if game["state"] == GAME_OVER:
                _draw_center_message(screen, big_font, small_font, "GAME OVER", cfg.RED, game["score"])
            else:
                _draw_center_message(screen, big_font, small_font, "YOU WIN!", cfg.GREEN, game["score"])
 
        pygame.display.flip()
        clock.tick(cfg.FPS)
 
    pygame.quit()
 
 
if __name__ == "__main__":
    main()
 