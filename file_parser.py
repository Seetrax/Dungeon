"""
4 5     # number of rows and cols
A 4 0   # agent starting coordinates
W 1 0   # wumpus coordinates
G 1 1   # gold coordinates
P 0 3   # 1st pit coordinates
P 1 2   # 2nd pit coordinates
P 3 2   # 3rd pit coordinates
"""
'''File parser class reads the configuration of the level given as txt file
and gives a 2D array which is essential for GameState and world classes to
produce level information'''
class File_Parser:
    def __init__(self, world_file):
        self.row_col = []
        self.agent = []
        self.lions = []

        #self.pits = [[]]

        file = open(world_file, 'r')

        self.row_col = file.readline()
        self.row_col = self.row_col.rstrip('\r\n')
        self.row_col = self.row_col.split(" ")
        # print(self.row_col)

        self.agent = file.readline()
        self.agent = self.agent.rstrip('\r\n')
        self.agent = self.agent.split(" ")
        

        self.golds=[]
        self.pits = []
        self.walls=[]
        while True:
            wum = file.readline()
            if len(wum) == 0 :
                break
            wum = wum.rstrip('\r\n')
            wum = wum.split(" ")
        
            if wum==['']:
                break
            self.lions.append(wum)
        while True:
            gol = file.readline()
            if len(gol) == 0 :
                break
            gol = gol.rstrip('\r\n')
            gol = gol.split(" ")
        
            if gol==['']:
                break
            self.golds.append(gol)
        
        while True:
            pit = file.readline()
            if len(pit) == 0 :
                break
            pit = pit.rstrip('\r\n')
            pit = pit.split(" ")
        
            if pit==['']:
                break
            self.pits.append(pit)
        while True:
            wall = file.readline()
            if len(wall) == 0:
                break
            wall = wall.rstrip('\r\n')
            wall = wall.split(" ")
            
            self.walls.append(wall)
        # print(self.pits)
