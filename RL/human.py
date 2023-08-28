"""
Legend:
. = visited tile
A = agent
G = gold
W = wumpus
S = stench
w = potential wumpus
nw = no wumpus
P = pit
B = breeze
p = potential pit
np = no pit
"""

# from pandas import * # pip install pandas
#import time

class Agent:
    def __init__(self, world, label_grid,omni=False):
        self.world = world
        self.omni=omni
        if omni==False:
            self.world_knowledge = [[[] for i in range(self.world.num_cols)] for j in range(self.world.num_rows)]
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')

        else:
            self.world_knowledge = [[[] for i in range(self.world.num_cols)] for j in range(self.world.num_rows)]
            self.world_knowledge=[[] for j in range(self.world.num_rows)]
            for i in range(self.world.num_rows):
                for j in range(self.world.num_cols):
                    self.world_knowledge[i].append(self.world.world[i][j].copy())
            self.lion_pos=world.lion_pos
            self.pits_pos=world.pits_pos
            self.gold_pos=world.gold_pos
            self.wall_pos=world.wall_pos
        self.num_stenches = 0
        self.path_out_of_cave = [[self.world.agent_row, self.world.agent_col]]
        self.mark_tile_visited()
        self.world.cave_entrance_row = self.world.agent_row
        self.world.cave_entrance_col = self.world.agent_col
        self.found_gold = False # self.exit_cave(found_gold)
        self.took_gold = False
        self.exited = False
        self.label_grid = label_grid
        self.repaint_world()

    

    def repaint_world(self):
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                updated_text = []
                if 'A' in self.world_knowledge[i][j]:
                    updated_text.append('A')
                if 'L' in self.world_knowledge[i][j]:
                    updated_text.append('L')
                if 'p' in self.world_knowledge[i][j]:
                    updated_text.append('P')
                if 'B' in self.world_knowledge[i][j]:
                    updated_text.append('B')
                if 'R' in self.world_knowledge[i][j]:
                    updated_text.append('R')
                if 'G' in self.world_knowledge[i][j]:
                    updated_text.append('G')

                updated_str=""

                self.label_grid[i][j].change_text(updated_str.join(updated_text))
                if '.' in self.world_knowledge[i][j]:
                    self.label_grid[i][j].label.config(bg="gray40")
                self.label_grid[i][j].label.update()
        # print("repainted")

    # def go_back_one_tile(self):
    #     # print(self.path_out_of_cave)
    #     # print(self.path_out_of_cave[-1][0])

    #     if self.world.agent_row-1 == self.path_out_of_cave[-1][0]:
    #         self.move('u')
    #     if self.world.agent_row+1 == self.path_out_of_cave[-1][0]:
    #         self.move('d')
    #     if self.world.agent_col+1 ==  self.path_out_of_cave[-1][1]:
    #         self.move('r')
    #     if self.world.agent_col-1 ==  self.path_out_of_cave[-1][1]:
    #         self.move('l')


    #     del self.path_out_of_cave[-1]



    def leave_cave(self):
        for tile in reversed(self.path_out_of_cave):
            # print("Leaving from: " + str(self.path_out_of_cave))
            if self.world.agent_row-1 == tile[0]:
                self.move('u')
            if self.world.agent_row+1 == tile[0]:
                self.move('d')
            if self.world.agent_col+1 == tile[1]:
                self.move('r')
            if self.world.agent_col-1 == tile[1]:
                self.move('l')

            if self.world.cave_entrance_row == self.world.agent_row:
                if self.world.cave_entrance_col == self.world.agent_col:
                    if self.found_gold == True:
                        self.exited = True
                        break


    


    def move(self, direction,index):
        
        self.repaint_world()
        if self.found_gold == True and self.took_gold == False:
            self.took_gold == True
            if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('G')

        successful_move = False
        if direction == 'u':
            #if self.is_safe_move(self.world.agent_row-1, self.world.agent_col):
                
                successful_move = self.move_up(index)
        if direction == 'r':
            #if self.is_safe_move(self.world.agent_row, self.world.agent_col+1):
                successful_move = self.move_right(index)
        if direction == 'd':
            #if self.is_safe_move(self.world.agent_row+1, self.world.agent_col):
                successful_move = self.move_down(index)
        if direction == 'l':
            #if self.is_safe_move(self.world.agent_row, self.world.agent_col-1):
                successful_move = self.move_left(index)

        if successful_move:
            self.add_indicators_to_knowledge()
            self.mark_tile_visited()
            #self.predict_wumpus()
            #self.predict_pits()
            #self.clean_predictions()
            #self.confirm_wumpus_knowledge()

            # print(DataFrame(self.world_knowledge))
            # print("Agent: [" + str(self.world.agent_row) + ", " + str(self.world.agent_col) + "]")
            # print("Path out:" + str(self.path_out_of_cave))
            if index==0:
                if 'G' in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                    # print("You found the gold! Time to leave!")
                    self.found_gold = True
                    self.world.world[self.world.agent_row][self.world.agent_col].remove('G')
                    self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('G')
                    

                if self.found_gold == False:
                    self.path_out_of_cave.append([self.world.agent_row, self.world.agent_col])

            # print("Successful move: " + str(successful_move))

            #time.sleep(1.5)
        direction=None
        return successful_move


    def add_indicators_to_knowledge(self):
        if self.omni==False:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if 'B' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                    self.world_knowledge[self.world.agent_row][self.world.agent_col].append('B')
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if 'S' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                    self.world_knowledge[self.world.agent_row][self.world.agent_col].append('R')
        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'G' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('G')
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'P' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('P')
        if 'L' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'L' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
                self.world_knowledge[self.world.agent_row][self.world.agent_col].append('W')

                    
    def move_up(self,index):
        if index==0:
            try:
                if self.world.agent_row-1 >= 0 and (self.world.agent_col,self.world.agent_row-1) not in self.world.wall_pos:
                    self.remove_agent(0)
                    self.world.agent_row -= 1
                    self.world.agent_pos=(self.world.agent_col,self.world.agent_row)
                    self.add_agent(0)
                    return True
                else:
                    return False
            except IndexError:
                return False
        elif index!=0 and self.omni==True :
            
            try:
                if self.world.lion_pos[index-1][1]-1 >= 0 and (self.world.lion_pos[index-1][0],self.world.lion_pos[index-1][1]-1) not in self.world.wall_pos:
                    self.remove_agent(index)
                    self.world.lion_pos[index-1]=(self.world.lion_pos[index-1][0],self.world.lion_pos[index-1][1]-1)
                    self.add_agent(index)
                    return True
                else:
                    return False
            except IndexError:
                return False
            


    def move_right(self,index):
        if index==0:
            try:
                if self.world.agent_col+1 < self.world.num_cols and (self.world.agent_col+1,self.world.agent_row) not in self.world.wall_pos:
                    self.remove_agent(0)
                    self.world.agent_col += 1
                    self.world.agent_pos=(self.world.agent_col,self.world.agent_row)
                    self.add_agent(0)
                    return True
                else:
                    return False
            except IndexError:
                return False
        elif index!=0 and self.omni==True :
            try:
                if self.world.lion_pos[index-1][0]+1 < self.world.num_cols and (self.world.lion_pos[index-1][0]+1,self.world.lion_pos[index-1][1]) not in self.world.wall_pos:
                    self.remove_agent(index)
                    self.world.lion_pos[index-1]=(self.world.lion_pos[index-1][0]+1,self.world.lion_pos[index-1][1])
                    self.add_agent(index)
                    return True
                else:
                    return False
            except IndexError:
                return False


    def move_down(self,index):
        if index==0:
            try:
                if self.world.agent_row+1 < self.world.num_rows and (self.world.agent_col,self.world.agent_row+1) not in self.world.wall_pos:
                    self.remove_agent(0)
                    self.world.agent_row += 1
                    self.world.agent_pos=(self.world.agent_col,self.world.agent_row)
                    self.add_agent(0)
                    return True
                else:
                    return False
            except IndexError:
                return False
        elif index!=0 and self.omni==True :
            
            try:
                if self.world.lion_pos[index-1][1]+1 < self.world.num_rows and (self.world.lion_pos[index-1][0],self.world.lion_pos[index-1][1]+1) not in self.world.wall_pos:
                    self.remove_agent(index)
                    self.world.lion_pos[index-1]=(self.world.lion_pos[index-1][0],self.world.lion_pos[index-1][1]+1)
                    self.add_agent(index)
                    return True
                else:
                    return False
            except IndexError:
                return False


    def move_left(self,index):
        if index==0:
            try:
                if self.world.agent_col-1 >= 0 and (self.world.agent_col-1,self.world.agent_row) not in self.world.wall_pos:
                    self.remove_agent(0)
                    self.world.agent_col -= 1
                    self.world.agent_pos=(self.world.agent_col,self.world.agent_row)
                    self.add_agent(0)
                    return True
                else:
                    return False
            except IndexError:
                return False
        elif index!=0 and self.omni==True :
            
            try:
                if self.world.lion_pos[index-1][0]-1 >= 0 and (self.world.lion_pos[index-1][0]-1,self.world.lion_pos[index-1][1]) not in self.world.wall_pos:
                    self.remove_agent(index)
                    self.world.lion_pos[index-1]=(self.world.lion_pos[index-1][0]-1,self.world.lion_pos[index-1][1])
                    self.add_agent(index)
                    return True
                else:
                    return False
            except IndexError:
                return False

    def remove_agent(self,index):
        if index==0:
            self.world.world[self.world.agent_row][self.world.agent_col].remove('A')
            self.world_knowledge[self.world.agent_row][self.world.agent_col].remove('A')
        elif index!=0 and self.omni==True:
            self.world.world[self.world.lion_pos[index-1][1]][self.world.lion_pos[index-1][0]].remove('L')
            self.world_knowledge[self.world.lion_pos[index-1][1]][self.world.lion_pos[index-1][0]].remove('L')
            i=self.world.lion_pos[index-1][1]
            j=self.world.lion_pos[index-1][0]
            if self.omni==False:
                if i-1 >= 0 and (j,i-1) not in self.wall_pos:
                    if 'R' in self.world.world[i-1][j]:
                        self.world.world[i-1][j].remove('R')
                        self.world_knowledge[i-1][j].remove('R')
                if j+1 < self.world.num_cols and (j+1,i) not in self.wall_pos:
                    if 'R' in self.world.world[i][j+1]:

                        self.world.world[i][j+1].remove('R')
                        self.world_knowledge[i][j+1].remove('R')
                if i+1 < self.world.num_rows and (j,i+1) not in self.wall_pos:
                    if 'R' in self.world.world[i+1][j]:

                        self.world.world[i+1][j].remove('R')
                        self.world_knowledge[i+1][j].remove('R')
                if j-1 >= 0 and (j-1,i) not in self.wall_pos:
                    if 'R' in self.world.world[i][j-1]:
                        #print((j,i))
                        self.world.world[i][j-1].remove('R')
                        self.world_knowledge[i][j-1].remove('R')


    def add_agent(self,index):
        if index==0:
            self.world.world[self.world.agent_row][self.world.agent_col].append('A')
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('A')
        elif index!=0 and self.omni==True:
            self.world.world[self.world.lion_pos[index-1][1]][self.world.lion_pos[index-1][0]].append('L')
            self.world_knowledge[self.world.lion_pos[index-1][1]][self.world.lion_pos[index-1][0]].append('L')
            i=self.world.lion_pos[index-1][1]
            j=self.world.lion_pos[index-1][0]
            if self.omni==False:
                if i-1 >= 0 and (j,i-1) not in self.wall_pos:
                    if 'R' not in self.world.world[i-1][j]:
                        self.world.world[i-1][j].append('R')
                        self.world_knowledge[i-1][j].append('R')
                if j+1 < self.world.num_cols and (j+1,i) not in self.wall_pos:
                    
                    if 'R' not in self.world.world[i][j+1]:

                        self.world.world[i][j+1].append('R')
                        self.world_knowledge[i][j+1].append('R')
                if i+1 < self.world.num_rows and (j,i+1) not in self.wall_pos:
                    if 'R' not in self.world.world[i+1][j]:
                        self.world.world[i+1][j].append('R')
                        self.world_knowledge[i+1][j].append('R')
                if j-1 >= 0 and (j-1,i) not in self.wall_pos:
                    if 'R' not in self.world.world[i][j-1]:
                        self.world.world[i][j-1].append('R')
                        self.world_knowledge[i][j-1].append('R')

    def mark_tile_visited(self):
        if '.' not in self.world_knowledge[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append('.')
            self.world_knowledge[self.world.agent_row][self.world.agent_col].append('.')


    def is_dead(self):
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have been slain by the Wumpus!")
            return True
        elif 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have fallen in a pit!")
            return True
        else:
            return False


    def is_safe_move(self, row, col):
        try:
            if 'w' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'p' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'W' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass
        try:
            if 'P' in self.world_knowledge[row][col]:
                # print("UNSAFE MOVE")
                return False
        except IndexError:
            pass

        return True
    def valid_exit(self):
        if self.found_gold == True:
            if self.world.agent_row == self.world.cave_entrance_row \
                and self.world.agent_col == self.world.cave_entrance_col:
                self.exited = True
                self.remove_agent()
                return True
        return False
