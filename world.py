from file_parser import File_Parser
# from pandas import *

'''The world class takes all information that a particular configuration of
the game specifies. It consists of all information about the game before it
begins (such as no of columns, rows, gold pos pit pos etc.) It is not required
for you to read this file, rather think of it as an abstract class that gives
the gamestate required info'''
class World:
    def __init__(self):
        self.world = [[]]
        self.num_rows = 0
        self.num_cols = 0
        self.wall_pos=[]
        self.agent_row = 0
        self.agent_col = 0
        self.cave_entrance_row = 0
        self.cave_entrance_col = 0
        self.num_agents=0
        self.agent_pos=()
        self.pits_pos=[]
        self.gold_pos=[]
        self.lion_pos=[]
        self.score=0
    def generate_world(self, file_name):

        file_parser = File_Parser(file_name)
        """
        print(file_parser.row_col)
        print(file_parser.agent)
        print(file_parser.wumpus)
        print(file_parser.gold)
        print(file_parser.pits)
        """
        self.num_rows = int(file_parser.row_col[0])
        self.num_cols = int(file_parser.row_col[1])
        self.num_agents=int(file_parser.row_col[2])
        self.world = [[[] for i in range(self.num_cols)] for j in range(self.num_rows)]

        self.agent_row = int(file_parser.agent[1])
        self.agent_col = int(file_parser.agent[2])
        self.agent_pos=(self.agent_col,self.agent_row)
        self.world[self.agent_row][self.agent_col].append('A')
        '''if len(file_parser.wumpus)>1:
            
            self.world[int(file_parser.wumpus[1])][int(file_parser.wumpus[2])].append(file_parser.wumpus[0])
            self.wumpus_pos.append((int(file_parser.wumpus[2]),int(file_parser.wumpus[1])))
        if len(file_parser.gold)>1:
            
            self.world[int(file_parser.gold[1])][int(file_parser.gold[2])].append(file_parser.gold[0])
            self.gold_pos.append((int(file_parser.gold[2]),int(file_parser.gold[1])))'''
        
        
        if len(file_parser.lions[0])>1:
            for wum in file_parser.lions:
            
                self.world[int(wum[1])][int(wum[2])].append(wum[0])
                self.lion_pos.append((int(wum[2]),int(wum[1])))
        if len(file_parser.golds[0])>1:
            for gold in file_parser.golds:
            
                self.world[int(gold[1])][int(gold[2])].append(gold[0])
                self.gold_pos.append((int(gold[2]),int(gold[1])))

        if len(file_parser.pits[0])>1:
            for pit in file_parser.pits:
            
                self.world[int(pit[1])][int(pit[2])].append(pit[0])
                self.pits_pos.append((int(pit[2]),int(pit[1])))
        if len(file_parser.walls[0])>1:
            for wall in file_parser.walls:
                self.world[int(wall[1])][int(wall[2])].append(wall[0])
                self.wall_pos.append((int(wall[2]),int(wall[1])))
        # print(DataFrame(self.world))


        #self.populate_indicators()

    """
    def generate_walls(self, filename):
    	file_parser = File_Parser(file_name)
        self.num_rows = int(file_parser.row_col[0])
        self.num_cols = int(file_parser.row_col[1])
        self.num_agents=int(file_parser.row_col[2])
        self.world = [[[] for i in range(self.num_cols)] for j in range(self.num_rows)]

        self.agent_row = int(file_parser.agent[1])
        self.agent_col = int(file_parser.agent[2])
        self.agent_pos=(self.agent_col,self.agent_row)
        self.world[self.agent_row][self.agent_col].append('A')
        '''if len(file_parser.wumpus)>1:
            
            self.world[int(file_parser.wumpus[1])][int(file_parser.wumpus[2])].append(file_parser.wumpus[0])
            self.wumpus_pos.append((int(file_parser.wumpus[2]),int(file_parser.wumpus[1])))
        if len(file_parser.gold)>1:
            
            self.world[int(file_parser.gold[1])][int(file_parser.gold[2])].append(file_parser.gold[0])
            self.gold_pos.append((int(file_parser.gold[2]),int(file_parser.gold[1])))'''
        
        
        if len(file_parser.lions[0])>1:
            for wum in file_parser.lions:
            
                self.world[int(wum[1])][int(wum[2])].append(wum[0])
                self.lion_pos.append((int(wum[2]),int(wum[1])))
        if len(file_parser.golds[0])>1:
            for gold in file_parser.golds:
            
                self.world[int(gold[1])][int(gold[2])].append(gold[0])
                self.gold_pos.append((int(gold[2]),int(gold[1])))

        if len(file_parser.pits[0])>1:
            for pit in file_parser.pits:
            
                self.world[int(pit[1])][int(pit[2])].append(pit[0])
                self.pits_pos.append((int(pit[2]),int(pit[1])))
        if len(file_parser.walls[0])>1:
            for wall in file_parser.walls:
                self.world[int(wall[1])][int(wall[2])].append(wall[0])
                self.wall_pos.append((int(wall[2]),int(wall[1])))
    """

    def populate_indicators(self):

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                for k in range(len(self.world[i][j])):
                    """
                    if self.world[i][j][k] == 'A':
                        print("Agent at [" + str(i) + ", " + str(j) + "]")
                    """

                    if self.world[i][j][k] == 'L':
                        # print("Wumpus at [" + str(i) + ", " + str(j) + "]")

                        try:
                            if i-1 >= 0 and (j,i-1) not in self.wall_pos:
                                if 'R' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('R')
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols and (j+1,i) not in self.wall_pos:
                                if 'R' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('R')
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows and (j,i+1) not in self.wall_pos:
                                if 'R' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('R')
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0 and (j-1,i) not in self.wall_pos:
                                if 'R' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('R')
                        except IndexError:
                            pass

                    """
                    if self.world[i][j][k] == 'G':
                        print("Gold at [" + str(i) + ", " + str(j) + "]")
                    """

                    if self.world[i][j][k] == 'P' :
                        # print("Pit at [" + str(i) + ", " + str(j) + "]")

                        try:
                            if i-1 >= 0 and (j,i-1) not in self.wall_pos:
                                if 'B' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('B')
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols and (j+1,i) not in self.wall_pos:
                                if 'B' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('B')
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows and (j,i+1) not in self.wall_pos:
                                if 'B' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('B')
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0 and (j-1,i) not in self.wall_pos:
                                if 'B' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('B')
                        except IndexError:
                            pass
