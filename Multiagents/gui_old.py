from tkinter import *
from human import Agent
from world import World
import Search
from grid_label import Grid_Label
import time
import MultiAgents
import copy
Lost=False
SCORE=0
arrival_act=[]
player='human'
mode='default'
searchMethod='bfs'
#def settings(commands):
explored=0    
opp={'u':'d','l':'r','r':'l','d':'u',None:None}
class GameState:
    def __init__(self,world):
        self.agent_pos=(world.agent_col,world.agent_row)
        self.world=world
        self.num_agents=world.num_agents
        self.gold_pos=world.gold_pos
        self.lion_pos=world.lion_pos
        self.wall_pos=world.wall_pos
        self.pits_pos=world.pits_pos
        self.score=world.score
        self.last_move=[]
        for i in range(world.num_agents-1):
                self.last_move.append(None)
    def getActions(self,agentindex=0):
        lis=[]
        global arrival_act,opp
        if self.isWin() or self.isLose():
            return []
        if agentindex==0:
            if self.agent_pos[1]-1 >= 0 and (self.agent_pos[0],self.agent_pos[1]-1) not in self.world.wall_pos:
                lis.append('u')
            if self.agent_pos[0]+1 < self.world.num_cols and (self.agent_pos[0]+1,self.agent_pos[1]) not in self.world.wall_pos:
                lis.append('r')
            if self.agent_pos[1]+1 < self.world.num_rows and (self.agent_pos[0],self.agent_pos[1]+1) not in self.world.wall_pos:
                lis.append('d')
            if self.agent_pos[0]-1 >= 0 and (self.agent_pos[0]-1,self.agent_pos[1]) not in self.world.wall_pos:
                lis.append('l')
        else:
            if self.world.lion_pos[agentindex-1][1]-1 >= 0 and (self.world.lion_pos[agentindex-1][0],self.world.lion_pos[agentindex-1][1]-1) not in self.world.wall_pos:
                lis.append('u')
            if self.world.lion_pos[agentindex-1][0]+1 < self.world.num_cols and (self.world.lion_pos[agentindex-1][0]+1,self.world.lion_pos[agentindex-1][1]) not in self.world.wall_pos:
                lis.append('r')
            if self.world.lion_pos[agentindex-1][1]+1 < self.world.num_rows and (self.world.lion_pos[agentindex-1][0],self.world.lion_pos[agentindex-1][1]+1) not in self.world.wall_pos:
                lis.append('d')
            if self.world.lion_pos[agentindex-1][0]-1 >= 0 and (self.world.lion_pos[agentindex-1][0]-1,self.world.lion_pos[agentindex-1][1]) not in self.world.wall_pos:
                lis.append('l')
            #print(lis)
            if opp[self.last_move[agentindex-1]] in lis and len(lis)!=1:
                lis.remove(opp[self.last_move[agentindex-1]])
                
        return lis
    def generateSuccessor(self,agentindex,action):
        global explored
        if self.isWin() or self.isLose():
            raise Exception('Can\'t generate a successor of a terminal state.')
        
        state = copy.deepcopy(self)
        if agentindex!=0:
            state.last_move[agentindex-1]=action
        actions=state.getActions(agentindex)
        
        if agentindex == 0:
            if action in actions:
                if action=='u':
                    state.agent_pos=(state.agent_pos[0],state.agent_pos[1]-1)
                elif action=='r':
                    state.agent_pos=(state.agent_pos[0]+1,state.agent_pos[1])
                elif action=='d':
                    state.agent_pos=(state.agent_pos[0],state.agent_pos[1]+1)
                elif action=='l':
                    state.agent_pos=(state.agent_pos[0]-1,state.agent_pos[1])
            if state.isGold():
                state.score+=50
                state.gold_pos.remove(state.agent_pos)
            elif state.isWin():
                state.score+=1000
            '''else:
                state.score-=1'''
        else:
            #print(actions)
            if action in actions:
                if action=='u':
                    state.lion_pos[agentindex-1]=(state.lion_pos[agentindex-1][0],state.lion_pos[agentindex-1][1]-1)
                elif action=='r':
                    state.lion_pos[agentindex-1]=(state.lion_pos[agentindex-1][0]+1,state.lion_pos[agentindex-1][1])
                elif action=='d':
                    state.lion_pos[agentindex-1]=(state.lion_pos[agentindex-1][0],state.lion_pos[agentindex-1][1]+1)
                elif action=='l':
                    state.lion_pos[agentindex-1]=(state.lion_pos[agentindex-1][0]-1,state.lion_pos[agentindex-1][1])
        
        
        if state.isLose():
            state.score=state.score-1000
        explored+=1
        
        return state
    def isGold(self):
        return self.agent_pos in self.gold_pos
    def isLose(self):
        return self.agent_pos in self.pits_pos or self.agent_pos in self.lion_pos
    def isWin(self):
        return len(self.gold_pos)==0
    def getScore(self):
        return self.score
def solve_wumpus_world(master, world_file):
    global SCORE, arrival_act
    world = World()
    world.generate_world(world_file)
    # print(DataFrame(world.world))
    label_grid = [[Grid_Label(world,master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]
    agent = Agent(world, label_grid,omni=True)
    game=GameState(world)
    entities=[]
    for i in range(world.num_agents):
        entities.append(MultiAgents.lion(i+1))
        arrival_act.append(None)
    act_index=0
    player='minimax'
    g=0
    while agent.exited == False:
        time.sleep(0)
        game=GameState(world)
        
        for i in range(world.num_agents-1):
                game.last_move[i]=arrival_act[i]
        if game.isLose():
            world.score-=1000
        agent.repaint_world()
        if game.isLose():
            print("U lost")
            break
        if game.isWin():
            print("You have exited with the gold!")
            break
        
        else:
            #print('no')
            pass
        if player=='human':
            
            master.bind('<Left>', 
                        lambda event: agent.move('l'))
            master.bind('<Right>', 
                        lambda event: agent.move('r'))
            
            master.bind('<Up>', 
                        lambda event: agent.move('u'))
            master.bind('<Down>', 
                        lambda event: agent.move('d'))
            
        elif player=='minimax':
            predict=MultiAgents.MinimaxAgent()
            #print(predict.getAction(game))
            agent.move(predict.getAction(game),0)
            game=GameState(world)
            for i in range(world.num_agents-1):
                game.last_move[i]=arrival_act[i]
            if game.isGold():
                g+=1
                world.score+=50
                world.gold_pos.remove((world.agent_col,world.agent_row))
            elif game.isLose():
                world.score-=1000
            elif game.isWin():
                world.score+=1000
            '''else:
                world.score-=1'''
            
            agent.repaint_world()
            if game.isLose():
                print("U lost")
                break
            if game.isWin():
                print("You have exited with the gold!")
                break
            else:
                #print('no')
                pass
            for i in range(world.num_agents-1):
                #print(game.lion_pos)
                a=entities[i].Act(game)
                agent.move(a,i+1)
                arrival_act[i]=a
            

           
    agent.repaint_world()
    try:
        agent.world_knowledge[agent.world.agent_row][agent.world.agent_col].remove('A')
    except ValueError:
        pass
    print(world.score)
    print(g)
    
    agent.repaint_world()
    
master = Tk()
master.title("Wumpus World")
#master.geometry('600x600')
#key = Keyboard_Input(master)

maze="world2.txt"
world = World()
world.generate_world(maze)

label_grid = [[Grid_Label(world,master, i, j) for j in range(world.num_cols)] for i in range(world.num_rows)]

solve_wumpus_world(master, maze)
mainloop()
