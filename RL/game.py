import copy

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
        self._explore=0
        for i in range(world.num_agents-1):
                self.last_move.append(None)
    def getActions(self,agentindex=0):
        lis=[]
        opp={'u':'d','l':'r','r':'l','d':'u',None:None}
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
        self._explore+=1
        
        return state
    def isGold(self):
        return self.agent_pos in self.gold_pos
    def isLose(self):
        return self.agent_pos in self.pits_pos or self.agent_pos in self.lion_pos
    def isWin(self):
        return len(self.gold_pos)==0
    def getScore(self):
        return self.score
