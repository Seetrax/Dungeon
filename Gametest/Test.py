import pygame
import sys


pygame.init()

GRID_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 19,19
WIDTH, HEIGHT = GRID_WIDTH*GRID_SIZE , GRID_HEIGHT*GRID_SIZE
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Game")

player_x, player_y = 0, 0

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            elif event.key == pygame.K_DOWN and player_y < GRID_HEIGHT - 1:
                player_y += 1
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            elif event.key == pygame.K_RIGHT and player_x < GRID_WIDTH - 1:
                player_x += 1


    screen.fill((0, 0,0))

    draw_grid()
    draw_player(player_x, player_y)
    pygame.display.flip()

pygame.quit()
sys.exit()
