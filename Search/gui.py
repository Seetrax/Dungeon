from tkinter import *
from human import Agent
from world import World
import Search
from grid_label import Grid_Label
import time
Lost=False
SCORE=0

player='human'
mode='default'
searchMethod='astar'
#def settings(commands):
    

class GameState:
    def __init__(self,world):
        self.agent_pos=(world.agent_col,world.agent_row)
        self.world=world
        self.gold_pos=world.gold_pos
        self.lion_pos=world.lion_pos
        self.wall_pos=world.wall_pos
        self.pits_pos=world.pits_pos
    def getActions(self,agentindex=0):
        lis=[]
        if self.world.agent_row-1 >= 0 and (self.world.agent_col,self.world.agent_row-1) not in self.world.wall_pos:
            lis.append('u')
        if self.world.agent_col+1 < self.world.num_cols and (self.world.agent_col+1,self.world.agent_row) not in self.world.wall_pos:
            lis.append('r')
        if self.world.agent_row+1 < self.world.num_rows and (self.world.agent_col,self.world.agent_row+1) not in self.world.wall_pos:
            lis.append('d')
        if self.world.agent_col-1 >= 0 and (self.world.agent_col-1,self.world.agent_row) not in self.world.wall_pos:
            lis.append('l')
        return lis
    def isGold(self):
        return self.agent_pos in self.gold_pos
    def isLose(self):
        return self.agent_pos in self.pits_pos or self.agent_pos in self.lion_pos
    def isWin(self):
        return len(self.world.gold_pos)==0
    def getScore(self):
        global SCORE
        return SCORE
def solve_wumpus_world(master, world_file):
    global SCORE
    world = World()
    world.generate_world(world_file)
    # print(DataFrame(world.world))
    label_grid = [[Grid_Label(world,master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]
    agent = Agent(world, label_grid,omni=True)
    game=GameState(world)
    problem=Search.PositionSearchProblem(game,world,goal=(world.num_cols-1,world.num_rows-1))
    if searchMethod=='bfs':
        actions=Search.bfs(problem)
    if searchMethod=='dfs':
        actions=Search.dfs(problem)
    if searchMethod=='ucs':
        actions=Search.ucs(problem)
    if searchMethod=='astar':
        actions=Search.aStarSearch(problem,heuristic=Search.mh)
    act_index=0
    player='agent'
    while agent.exited == False:
        time.sleep(0)
        game=GameState(world)
        
        if player=='human':
            
            master.bind('<Left>', 
                        lambda event: agent.move('l',0))
            master.bind('<Right>', 
                        lambda event: agent.move('r',0))
            
            master.bind('<Up>', 
                        lambda event: agent.move('u',0))
            master.bind('<Down>', 
                        lambda event: agent.move('d',0))
            
        elif player=='agent':
            agent.move(actions[act_index],0)
            act_index+=1
        if game.isGold():
            SCORE+=100
        elif game.isLose():
            SCORE-=100
        elif game.isWin():
            SCORE+=500
        else:
            SCORE-=10
        #agent.move(global_key_input)
        
        agent.repaint_world()
        if game.isLose():
            break
        if game.isWin():
            break
        if agent.valid_exit() == True:
            print("hi")
            break
        else:
            #print('no')
            pass
        # if agent.found_gold == True:
        #     agent.leave_cave()
        #break
        #initial()   
    print("You have exited with the gold!")
    agent.repaint_world()
    try:
        agent.world_knowledge[agent.world.agent_row][agent.world.agent_col].remove('A')
    except ValueError:
        pass
    print(problem._expanded)
    print(SCORE)
    agent.repaint_world()
    
master = Tk()
master.title("Wumpus World")
#master.geometry('600x600')
#key = Keyboard_Input(master)

maze="Medmaze.txt"
world = World()
world.generate_world(maze)

label_grid = [[Grid_Label(world,master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]

solve_wumpus_world(master, maze)
mainloop()
