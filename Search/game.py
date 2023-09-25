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
