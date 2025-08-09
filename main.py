import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

bird_img = pygame.image.load("flappy_bird_pipe.png").convert_alpha()
bird_width = 50
bird_height = int(bird_img.get_height() * (bird_width / bird_img.get_width()))
bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))

pipe_width = 80
pipe_gap = 180
pipe_speed = 4

gravity = 0.5
jump_strength = -10

def create_pipe():
    height = random.randint(100, HEIGHT - pipe_gap - 100)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(win, GREEN, pipe)

def check_collision(bird_rect, pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

def main():
    bird_x = WIDTH * 0.15
    bird_y = HEIGHT // 2
    bird_movement = 0
    score = 0
    pipes = []
    pipes.extend(create_pipe())
    running = True
    game_over = False

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if not game_over and event.key == pygame.K_SPACE:
                    bird_movement = jump_strength
                elif game_over:
                    if event.key == pygame.K_c:
                        bird_y = HEIGHT // 2
                        bird_movement = 0
                        pipes.clear()
                        pipes.extend(create_pipe())
                        score = 0
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False

        if not game_over:
            bird_movement += gravity
            bird_y += bird_movement

            for pipe in pipes:
                pipe.x -= pipe_speed

            if pipes[0].right < 0:
                pipes.pop(0)
                pipes.pop(0)
                pipes.extend(create_pipe())
                score += 1

            bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
            if check_collision(bird_rect, pipes):
                game_over = True

        win.fill(WHITE)
        win.blit(bird_img, (bird_x, bird_y))
        draw_pipes(pipes)

        score_text = font.render(f"Score: {score}", True, BLACK)
        win.blit(score_text, (10, 10))

        if game_over:
            lines = [
                "GAME OVER!",
                "C - Restart",
                "Q - Quit"
            ]
            for i, line in enumerate(lines):
                over_text = font.render(line, True, RED)
                win.blit(over_text, (WIDTH // 10, HEIGHT // 2 + i * 50))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
