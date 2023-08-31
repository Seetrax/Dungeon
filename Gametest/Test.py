import pygame
import sys
import os
from world import World
import time

count=0

fps=60
timer=pygame.time.Clock()
DIRECTION=0
DIRECTION_L=0

pygame.init()
WIDTH, HEIGHT = 400,400
COL, ROW = 5,5
GRID_SIZE = WIDTH//COL


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

PLAYER_IMG_U = [pygame.transform.scale(pygame.image.load(f'Agents/Player/Player_u{i}.png'),(GRID_SIZE,GRID_SIZE)) for i in range (1,4)]
PLAYER_IMG_D = [pygame.transform.scale(pygame.image.load(f'Agents/Player/Player_d{i}.png'),(GRID_SIZE,GRID_SIZE)) for i in range (1,4)]
PLAYER_IMG_R = [pygame.transform.scale(pygame.image.load(f'Agents/Player/Player_r{i}.png'),(GRID_SIZE,GRID_SIZE)) for i in range (1,4)]
PLAYER_IMG_L = [pygame.transform.flip(i,True,False) for i in PLAYER_IMG_R]

WUMPUS_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','lion.png')),(GRID_SIZE,GRID_SIZE))
PIT_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','pit2.png')),(GRID_SIZE,GRID_SIZE))
GOLD_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','Gold.png')),(GRID_SIZE,GRID_SIZE))
BG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','forest2.png')),(WIDTH,HEIGHT))
BUSH_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','bush.jpg')),(GRID_SIZE,GRID_SIZE))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Game")

player_x, player_y = 0, 0
lion_x,lion_y= 1,3

W=World()
W.generate_world('world.txt')

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))


def draw_entity(x, y,img):
    screen.blit(img,(x* GRID_SIZE,y* GRID_SIZE))


def draw_lion(x, y):
    if DIRECTION_L==0:##RIGHT
        
        screen.blit(pygame.transform.flip(WUMPUS_IMG,True,False),(x* GRID_SIZE,y* GRID_SIZE))
    elif DIRECTION_L==1:##LEFT

        screen.blit(WUMPUS_IMG,(x* GRID_SIZE,y* GRID_SIZE))
    elif DIRECTION_L==2:##UP
        screen.blit(pygame.transform.rotate(WUMPUS_IMG,270),(x* GRID_SIZE,y* GRID_SIZE))
    elif DIRECTION_L==3:##DOWN
        screen.blit(pygame.transform.rotate(WUMPUS_IMG,90),(y* GRID_SIZE,y* GRID_SIZE))
    

def draw_player(x, y):
    global count
    if DIRECTION==0:##RIGHT
        screen.blit(PLAYER_IMG_R[count//8],(x* GRID_SIZE,y* GRID_SIZE))
    elif DIRECTION==1:##LEFT

        screen.blit(PLAYER_IMG_L[count//8],(x* GRID_SIZE,y* GRID_SIZE))
    elif DIRECTION==2:##UP
        screen.blit(PLAYER_IMG_U[count//8],(x* GRID_SIZE,y* GRID_SIZE))
    elif DIRECTION==3:##DOWN
        screen.blit(PLAYER_IMG_D[count//8],(x* GRID_SIZE,y* GRID_SIZE))
    #pygame.draw.rect(screen, GREEN, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def main(world,omni=False):
    global DIRECTION,count
    lost=False
    player_x=world.agent_col
    player_y=world.agent_row
    lion_pos=world.lion_pos
    pit_pos=world.pits_pos
    gold_pos=world.gold_pos
    world.world[player_y][player_x].append('.')
    running = True
    while running:
        timer.tick(fps)
        if count<23:
            count+=1
        else:
            count=0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_y > 0:
                    player_y-=1
                    #player=(player[0],player[1]-1)
                    if '.' not in world.world[player_y][player_x]:
                        world.world[player_y][player_x].append('.')
                    DIRECTION=2
                elif event.key == pygame.K_DOWN and player_y < ROW - 1:
                    player_y+=1
                    #player=(player[0],player[1]+1)
                    if '.' not in world.world[player_y][player_x]:
                        world.world[player_y][player_x].append('.')
                    DIRECTION=3
                elif event.key == pygame.K_LEFT and player_x > 0:
                    player_x-=1
                    #player=(player[0]-1,player[1])
                    if '.' not in world.world[player_y][player_x]:
                        world.world[player_y][player_x].append('.')
                    DIRECTION=1
                elif event.key == pygame.K_RIGHT and player_x < COL - 1:
                    player_x+=1
                    #player=(player[0]+1,player[1])
                    if '.' not in world.world[player_y][player_x]:
                        world.world[player_y][player_x].append('.')
                    DIRECTION=0

        screen.fill((0, 0,0))
        screen.blit(BG, (0, 0))
        #draw_grid()
        draw_player(player_x,player_y)
        for i in range(world.num_rows):
            for j in range(world.num_cols):
                if 'L' in world.world[i][j]:
                    draw_lion(j, i)
                if 'P' in world.world[i][j]:
                    draw_entity(j, i,PIT_IMG)
                if 'G' in world.world[i][j]:
                    draw_entity(j, i,GOLD_IMG)
                if '.' not in world.world[i][j] and omni==False:
                    draw_entity(j, i,BUSH_IMG)
        if (player_x,player_y) in gold_pos:
            world.world[player_y][player_x].remove('G')
            gold_pos.remove((player_x,player_y))
        if (player_x,player_y) in pit_pos or (player_x,player_y) in lion_pos:
            lost=True
            running=False
        if len(gold_pos)==0:
            running=False
        
        '''for i in lion_pos:
            draw_lion(i[0], i[1])
        for i in pit_pos:
            draw_entity(i[0],i[1],PIT_IMG)
        for i in gold_pos:
            draw_entity(i[0],i[1],GOLD_IMG)'''
        pygame.display.flip()
    if lost==True:
        print("YOU LOST")
    elif lost==False:
        print("YOU WIN")
    pygame.quit()
    sys.exit()
main(W)
