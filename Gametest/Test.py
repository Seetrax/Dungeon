import pygame
import sys
import os

DIRECTION=0

pygame.init()
WIDTH, HEIGHT = 400,400
COL, ROW = 4,4
GRID_SIZE = WIDTH//COL


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

PLAYER_IMG=pygame.transform.scale(pygame.image.load(os.path.join('Agents','Player.jpg')),(GRID_SIZE,GRID_SIZE))
WUMPUS_IMG=pygame.transform.scale(pygame.image.load(os.path.join('Agents','Wumpus.jpg')),(GRID_SIZE,GRID_SIZE))
PIT_IMG=pygame.transform.scale(pygame.image.load(os.path.join('Agents','pit.png')),(GRID_SIZE,GRID_SIZE))
GOLD_IMG=pygame.transform.scale(pygame.image.load(os.path.join('Agents','Gold.png')),(GRID_SIZE,GRID_SIZE))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Game")

player_x, player_y = 0, 0

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_player(x, y):
    if DIRECTION==0:##RIGHT
        
        screen.blit(pygame.transform.flip(PLAYER_IMG,True,False),(player_x* GRID_SIZE,player_y* GRID_SIZE))
    elif DIRECTION==1:##LEFT

        screen.blit(PLAYER_IMG,(player_x* GRID_SIZE,player_y* GRID_SIZE))
    elif DIRECTION==2:##UP
        screen.blit(pygame.transform.rotate(PLAYER_IMG,270),(player_x* GRID_SIZE,player_y* GRID_SIZE))
    elif DIRECTION==3:##DOWN
        screen.blit(pygame.transform.rotate(PLAYER_IMG,90),(player_x* GRID_SIZE,player_y* GRID_SIZE))
    #pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
                DIRECTION=2
            elif event.key == pygame.K_DOWN and player_y < ROW - 1:
                player_y += 1
                DIRECTION=3
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
                DIRECTION=1
            elif event.key == pygame.K_RIGHT and player_x < COL - 1:
                player_x += 1
                DIRECTION=0


    screen.fill((0, 0,0))

    draw_grid()
    draw_player(player_x, player_y)
    pygame.display.flip()

pygame.quit()
sys.exit()
