import pygame
import sys
import os
from world import World
import time
import Search
from game import GameState 
count=0
countl=0

fps=60
timer=pygame.time.Clock()
DIRECTION=0
DIRECTION_L=0

pygame.init()
W=World()
W.generate_world('Medmaze.txt')
WIDTH, HEIGHT = 800,700
COL, ROW = W.num_cols,W.num_rows
GRID_W = WIDTH//COL
GRID_L=HEIGHT//ROW
GRID_SIZE=(GRID_W,GRID_L)
print(GRID_SIZE)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WALL_IMG = pygame.transform.scale(pygame.image.load(f'Agents/wall.jpg'),GRID_SIZE)
PLAYER_IMG_U = [pygame.transform.scale(pygame.image.load(f'Agents/Player/Player_u{i}.png'),GRID_SIZE) for i in range (1,4)]
PLAYER_IMG_D = [pygame.transform.scale(pygame.image.load(f'Agents/Player/Player_d{i}.png'),GRID_SIZE) for i in range (1,4)]
PLAYER_IMG_R = [pygame.transform.scale(pygame.image.load(f'Agents/Player/Player_r{i}.png'),GRID_SIZE) for i in range (1,4)]
PLAYER_IMG_L = [pygame.transform.flip(i,True,False) for i in PLAYER_IMG_R]
LION_IMG_U = [pygame.transform.scale(pygame.image.load(f'Agents/lion/{i}.png'),GRID_SIZE) for i in range (1,5)]
LION_IMG_R = [pygame.transform.scale(pygame.image.load(f'Agents/lion/{i}.png'),GRID_SIZE) for i in range (1,5)]
LION_IMG_L = [pygame.transform.flip(i,True,False) for i in LION_IMG_R]
LION_IMG_D = [pygame.transform.scale(pygame.image.load(f'Agents/lion/{i}.png'),GRID_SIZE) for i in range (1,5)]

WUMPUS_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','lion.png')),GRID_SIZE)
PIT_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','pit2.png')),GRID_SIZE)
GOLD_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','Gold.png')),GRID_SIZE)
BG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','forest2.png')),(WIDTH,HEIGHT))
BUSH_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Agents','bush.jpg')),GRID_SIZE)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid Game")

player_x, player_y = 0, 0
lion_x,lion_y= 1,3



def draw_grid():
    for x in range(0, WIDTH, GRID_W):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_L):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))


def draw_entity(x, y,img):
    screen.blit(img,(x* GRID_W,y* GRID_L))


def draw_lion(x, y):
    if DIRECTION_L==0:##RIGHT
        screen.blit(LION_IMG_R[countl//8],(x* GRID_W,y* GRID_L))
    elif DIRECTION_L==1:##LEFT

        screen.blit(LION_IMG_L[countl//8],(x* GRID_W,y* GRID_L))
    elif DIRECTION_L==2:##UP
        screen.blit(LION_IMG_U[countl//8],(x* GRID_W,y* GRID_L))
    elif DIRECTION_L==3:##DOWN
        screen.blit(LION_IMG_D[countl//8],(x* GRID_W,y* GRID_L))
    

def draw_player(x, y):
    global count
    if DIRECTION==0:##RIGHT
        screen.blit(PLAYER_IMG_R[count//8],(x* GRID_W,y* GRID_L))
    elif DIRECTION==1:##LEFT

        screen.blit(PLAYER_IMG_L[count//8],(x* GRID_W,y* GRID_L))
    elif DIRECTION==2:##UP
        screen.blit(PLAYER_IMG_U[count//8],(x* GRID_W,y* GRID_L))
    elif DIRECTION==3:##DOWN
        screen.blit(PLAYER_IMG_D[count//8],(x* GRID_W,y* GRID_L))


def main(world,omni=False,player='human'):
    global DIRECTION,count,countl
    frames=0
    clock=pygame.time.Clock()
    lost=False
    player_x=world.agent_col
    player_y=world.agent_row
    lion_pos=world.lion_pos
    pit_pos=world.pits_pos
    gold_pos=world.gold_pos
    world.world[player_y][player_x].append('.')
    g=GameState(world)
    problem=Search.PosProblem(g,world,goal=(world.num_cols-1,world.num_rows-1))
    if (player=='agent'):
        acts=Search.bfs(problem)
        print(acts)
        index=0
        curr_act=acts[index]
    running = True
    
    while running:
        
        
        if countl<31:
            countl+=1
        else:
            countl=0
        if count<23:
            count+=1
        else:
            count=0
        if player=='human':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Handle player movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and player_y > 0 and (player_x,player_y-1) not in world.wall_pos:
                        player_y-=1
                        #player=(player[0],player[1]-1)
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=2
                    elif event.key == pygame.K_DOWN and player_y < ROW - 1 and (player_x,player_y+1) not in world.wall_pos:
                        player_y+=1
                        #player=(player[0],player[1]+1)
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=3
                    elif event.key == pygame.K_LEFT and player_x > 0 and (player_x-1,player_y) not in world.wall_pos:
                        player_x-=1
                        #player=(player[0]-1,player[1])
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=1
                    elif event.key == pygame.K_RIGHT and player_x < COL - 1 and (player_x+1,player_y) not in world.wall_pos:
                        player_x+=1
                        #player=(player[0]+1,player[1])
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=0
        elif player=='agent':
                    if frames == 10:
            
                        index+=1
                        curr_act=acts[index]
                        frames=0
                    else :
                        frames+=1
                    if curr_act == 'u' and player_y > 0 and (player_x,player_y-1) not in world.wall_pos:
                        player_y-=1
                        #player=(player[0],player[1]-1)
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=2
                        curr_act=None
                    elif curr_act == 'd' and player_y < ROW - 1 and (player_x,player_y+1) not in world.wall_pos:
                        player_y+=1
                        #player=(player[0],player[1]+1)
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=3
                        curr_act=None
                    elif curr_act == 'l' and player_x > 0 and (player_x-1,player_y) not in world.wall_pos:
                        player_x-=1
                        #player=(player[0]-1,player[1])
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=1
                        curr_act=None
                    elif curr_act == 'r' and player_x < COL - 1 and (player_x+1,player_y) not in world.wall_pos:
                        player_x+=1
                        #player=(player[0]+1,player[1])
                        if '.' not in world.world[player_y][player_x]:
                            world.world[player_y][player_x].append('.')
                        DIRECTION=0
                        curr_act=None
                    
                    

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
                if 'V' in world.world[i][j]:
                    draw_entity(j, i,WALL_IMG)
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
        pygame.display.flip()
        clock.tick(fps)
    if lost==True:
        print("YOU LOST")
    elif lost==False:
        print("YOU WIN")
    pygame.quit()
    sys.exit()
main(W,omni=True,player='agent')
