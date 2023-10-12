'''The GameState class captures the information about the agent
lion and the world at any point of time. This class will be
actively used in all projects and it is necessary to go through the
various values that this class captures'''

'''Some of the important functions it provides for the user are :

getActions : for any agent it returns a list of actions that are possible from
its current position.

generateSuccessor : for a given Gamestate this function produces all the
possible successor gamestates and its information

isGold : tells whether current treasure hunter position has gold or not

isWin : tells whether current gamestate is a winning state

isLose : tells whether current gamestate is a losing state.

'''

from world import World

class GameState:

    def __init__( self, prevState = None ):
        """ 
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None: # Initial state                                                                                                                                                               
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()


    def initialize(self, world):
        self.world=world
        self.agent_pos=(self.world.agent_col,self.world.agent_row)
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



class Grid:
    """
    A 2-dimensional array of objects backed by a list of lists.  Data is accessed
    via grid[x][y] where (x,y) are positions on a Pacman map with x horizontal,
    y vertical and the origin (0,0) in the bottom left corner.

    The __str__ method constructs an output that is oriented like a pacman board.
    """
    def __init__(self, width, height, initialValue=False, bitRepresentation=None):
        if initialValue not in [False, True]: raise Exception('Grids can only contain booleans')
        self.CELLS_PER_INT = 30

        self.width = width
        self.height = height
        self.data = [[initialValue for y in range(height)] for x in range(width)]
        if bitRepresentation:
            self._unpackBits(bitRepresentation)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other == None: return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item =True ):
        return sum([x.count(item) for x in self.data])

    def asList(self, key = True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key: list.append( (x,y) )
        return list

    def packBits(self):
        """
        Returns an efficient int list representation

        (width, height, bitPackedInts...)
        """
        bits = [self.width, self.height]
        currentInt = 0
        for i in range(self.height * self.width):
            bit = self.CELLS_PER_INT - (i % self.CELLS_PER_INT) - 1
            x, y = self._cellIndexToPosition(i)
            if self[x][y]:
                currentInt += 2 ** bit
            if (i + 1) % self.CELLS_PER_INT == 0:
                bits.append(currentInt)
                currentInt = 0
        bits.append(currentInt)
        return tuple(bits)

    def _cellIndexToPosition(self, index):
        x = index // self.height
        y = index % self.height
        return x, y

    def _unpackBits(self, bits):
        """
        Fills in data from a bit-level representation
        """
        cell = 0
        for packed in bits:
            for bit in self._unpackInt(packed, self.CELLS_PER_INT):
                if cell == self.width * self.height: break
                x, y = self._cellIndexToPosition(cell)
                self[x][y] = bit
                cell += 1

    def _unpackInt(self, packed, size):
        bools = []
        if packed < 0: raise ValueError("must be a positive integer")
        for i in range(size):
            n = 2 ** (self.CELLS_PER_INT - i - 1)
            if packed >= n:
                bools.append(True)
                packed -= n
            else:
                bools.append(False)
        return bools




class GameStateData:
    """

    """
    def __init__( self, prevState = None ):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if prevState != None:
            
            self.agent_pos=(prevState.world.agent_col,prevState.world.agent_row)                                                                                                                                                    
            self.world=prevState.world
            self.num_agents=prevState.num_agents
            self.gold_pos=prevState.gold_pos
            self.lion_pos=prevState.lion_pos
            self.wall_pos=prevState.wall_pos
            self.pits_pos=prevState.pits_pos
            self.score=prevState.score
            # self.last_move=prevState
            # for i in range(world.num_agents-1):
                # self.last_move.append(None)



            # self.food = prevState.food.shallowCopy()
            # self.capsules = prevState.capsules[:]
            # self.agentStates = self.copyAgentStates( prevState.agentStates )
            # self.layout = prevState.layout
            # self._eaten = prevState._eaten
            # self.score = prevState.score

        # self._foodEaten = None
        # self._foodAdded = None
        # self._capsuleEaten = None
        # self._agentMoved = None
        # self._lose = False
        # self._win = False
        # self.scoreChange = 0

    def deepCopy( self ):
        state = GameStateData( self )
        state.food = self.food.deepCopy()
        state.layout = self.layout.deepCopy()
        state._agentMoved = self._agentMoved
        state._foodEaten = self._foodEaten
        state._foodAdded = self._foodAdded
        state._capsuleEaten = self._capsuleEaten
        return state

    def copyAgentStates( self, agentStates ):
        copiedStates = []
        for agentState in agentStates:
            copiedStates.append( agentState.copy() )
        return copiedStates

    def __eq__( self, other ):
        """
        Allows two states to be compared.
        """
        if other == None: return False
        # TODO Check for type of other
        if not self.agentStates == other.agentStates: return False
        if not self.food == other.food: return False
        if not self.capsules == other.capsules: return False
        if not self.score == other.score: return False
        return True

    def __hash__( self ):
        """
        Allows states to be keys of dictionaries.
        """
        for i, state in enumerate( self.agentStates ):
            try:
                int(hash(state))
            except TypeError as e:
                print(e)
                #hash(state)
        return int((hash(tuple(self.agentStates)) + 13*hash(self.food) + 113* hash(tuple(self.capsules)) + 7 * hash(self.score)) % 1048575 )

    def __str__( self):
        width, height = self.layout.width, self.layout.height
        # width, height = width, height
        map = Grid(width, height)
        if type(self.food) == type((1,2)):
            self.food = reconstituteGrid(self.food)
        for x in range(width):
            for y in range(height):
                food, walls = self.food, self.layout.walls
                map[x][y] = self._foodWallStr(food[x][y], walls[x][y])

        for agentState in self.agentStates:
            if agentState == None: continue
            if agentState.configuration == None: continue
            x,y = [int( i ) for i in nearestPoint( agentState.configuration.pos )]
            agent_dir = agentState.configuration.direction
            if agentState.isPacman:
                map[x][y] = self._pacStr( agent_dir )
            else:
                map[x][y] = self._ghostStr( agent_dir )

        for x, y in self.capsules:
            map[x][y] = 'o'

        return str(map) + ("\nScore: %d\n" % self.score)

    def _foodWallStr( self, hasFood, hasWall ):
        if hasFood:
            return '.'
        elif hasWall:
            return '%'
        else:
            return ' '

    def _pacStr( self, dir ):
        if dir == Directions.NORTH:
            return 'v'
        if dir == Directions.SOUTH:
            return '^'
        if dir == Directions.WEST:
            return '>'
        return '<'

    def _ghostStr( self, dir ):
        return 'G'
        if dir == Directions.NORTH:
            return 'M'
        if dir == Directions.SOUTH:
            return 'W'
        if dir == Directions.WEST:
            return '3'
        return 'E'

    def initialize( self, world, numGhostAgents ):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        '''
        self.food = layout.food.copy()
        #self.capsules = []
        self.capsules = layout.capsules[:]
        self.layout = layout
        self.score = 0
        self.scoreChange = 0

        self.agentStates = []
        numGhosts = 0
        for isPacman, pos in layout.agentPositions:
            if not isPacman:
                if numGhosts == numGhostAgents: continue # Max ghosts reached already
                else: numGhosts += 1
            self.agentStates.append( AgentState( Configuration( pos, Directions.STOP), isPacman) )
        self._eaten = [False for a in self.agentStates]
        '''
        self.agent_pos = (world.agent_col, world.agent_row)
        self.world = world
        # self.num_agents = world.num_agents
        # self.gold_pos = world.gold_pos
        # self.lion_pos = world.lion_pos
        self.wall_pos = world.wall_pos
        # self.pits_pos = world.pits_pos
        self.score = world.score
        self.last_move = []
        for i in range(world.num_agents-1):
                self.last_move.append(None)


