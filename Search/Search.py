import util

class SearchProblem:
    def getStartState(self):
        return None

    def isGoalState(self, state):
        return None

    def getSuccessors(self, state):
        
        return None

    def getCostOfActions(self, actions):
        
        return None


class PositionSearchProblem(SearchProblem):

    def __init__(self, gameState,world,goal=(1,1), costFn = lambda x: 1, start=None):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        
        self.startState = gameState.agent_pos
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.world=world
        
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal
        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        if state[1]-1 >= 0 and (state[0],state[1]-1) not in self.world.wall_pos:
            successors.append(((state[0],state[1]-1),'u',self.costFn((state[0],state[1]-1))))
        if state[0]+1 < self.world.num_cols and (state[0]+1,state[1]) not in self.world.wall_pos:
            successors.append(((state[0]+1,state[1]),'r',self.costFn((state[0]+1,state[1]))))
        if state[1]+1 < self.world.num_rows and (state[0],state[1]+1) not in self.world.wall_pos:
            successors.append(((state[0],state[1]+1),'d',self.costFn((state[0],state[1]+1))))
        if state[0]-1 >= 0 and (state[0]-1,state[1]) not in self.world.wall_pos:
            successors.append(((state[0]-1,state[1]),'l',self.costFn((state[0]-1,state[1]))))

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)
        #print(successors)
        return successors

    def getCostOfActions(self, actions):


        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

'''class fourgoldsProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    def __init__(self, startingGameState: pacman.GameState,warn=True, visualize=True):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.costFn = lambda x: 1
        self.visualize=visualize
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        self.goals=[(i,1,1,1,1) for i in self.corners]
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"
        print(self.corners)
        ss = [self.startingPosition,0,0,0,0]
        if self.startingPosition in self.corners:
            ss[self.corners.index(self.startingposition)+1]=1
        self.startState=tuple(ss)
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        return self.startState
        util.raiseNotDefined()

    def isGoalState(self, state: Any):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        isGoal = state in self.goals

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state[0])
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal
        util.raiseNotDefined()

    def getSuccessors(self, state: Any):
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            
            x,y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                NS=[nextState]
                for i in state[1:5]:
                    NS.append(i)
                
                if nextState in self.corners:
                    NS[self.corners.index(nextState)+1]=1
                cost = self.costFn(nextState)
                successors.append( ( tuple(NS), action, cost) )

        self._expanded += 1 # DO NOT CHANGE

        if state[0] not in self._visited:
            self._visited[state[0]] = True
            self._visitedlist.append(state[0])


        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)'''
def dfs(problem):
    
    visited2=[]
    parent2={}
    
    e=0
    actions={}
    act=[]
    path=[]
    flag=False
    ini=problem.getStartState()
    fin=()

    q=util.Stack()#Queue to store an elemnet which is poped and explored every iteration of while
    q.push(ini)
    visited2.append(ini)
    while ((q.isEmpty())==False):
        u=q.pop()
        visited2.append(u)
        e+=1
        if (problem.isGoalState(u)):
            fin=u
            break
        for v in problem.getSuccessors(u):
            if v[0] not in visited2:
                
                
                actions[tuple((u,v[0]))]=v[1]
                parent2[v[0]]=u
                q.push(v[0])
    x=fin
    path.append(x)
        
    while(parent2[x] !=ini): 
        act.append(actions[(parent2[x],x)])
        x = parent2[x]
        path.append(x)  
    path.append(ini)
    act.append(actions[(parent2[x],x)])
    path = path[::-1] 
    act=act[::-1]

    return act
def bfs(problem):
    """Search the shallowest nodes in the search tree first."""

    visited2=[]
    parent2={}
    tree2=[]
    adj={}
    actions={}
    act=[]
    path=[]
    flag=False
    ini=problem.getStartState()
    fin=()

    q=util.Queue()#Queue to store an elemnet which is poped and explored every iteration of while
    q.push(ini)
    visited2.append(ini)
    tree2.append(ini)
    while ((q.isEmpty())==False):
        
        u=q.pop()

        if (problem.isGoalState(u)):
            fin=u
            break
        for v in problem.getSuccessors(u):
            
            if v[0] not in visited2:
                tree2.append(v[0])
                visited2.append(v[0])
                actions[tuple((u,v[0]))]=v[1]
                parent2[v[0]]=u
                q.push(v[0])
                
                    
    x=fin
    path.append(x)
 
    while(parent2[x] !=ini): 
        act.append(actions[(parent2[x],x)])
        x = parent2[x]
        path.append(x)  
    path.append(ini)
    act.append(actions[(parent2[x],x)])
    path = path[::-1] 
    act=act[::-1]

    return act

def ucs(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited2=[]
    parent2={}
    actions={}
    act=[]
    path=[]
    ini=problem.getStartState()
    visited2.append(ini)
    fin=()
    g={}

    g[ini]=0
    q=util.PriorityQueue()#Queue to store an elemnet which is poped and explored every iteration of while
    q.push(ini,0)
    
    while ((q.isEmpty())==False):
        u=q.pop()

        if u not in visited2:
            visited2.append(u)
        
        if (problem.isGoalState(u)):
            fin=u
            break
        
        for v in problem.getSuccessors(u):
            if v[0] not in visited2:
                ##visited2.append(v[0])
                if v[0] not in g.keys():
                    g[v[0]]=g[u]+v[2]
                    actions[tuple((u,v[0]))]=v[1]
                    parent2[v[0]]=u
                    q.push(v[0],g[v[0]])
                else:
                    if g[v[0]]>g[u]+v[2]:
                        g[v[0]]=g[u]+v[2]
                        actions[tuple((u,v[0]))]=v[1]
                        parent2[v[0]]=u
                        q.push(v[0],g[v[0]])
        
    x=fin
    path.append(x)
        
    while(parent2[x] !=ini): 
        act.append(actions[(parent2[x],x)])
        x = parent2[x]
        path.append(x)  
    path.append(ini)
    act.append(actions[(parent2[x],x)])
    path = path[::-1] 
    act=act[::-1]
    return act

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
def mh(x1,problem):
    x2=problem.goal
    return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited2=[]
    parent2={}

    actions={}
    act=[]
    path=[]
    ini=problem.getStartState()
    visited2.append(ini)
    fin=()
    g={}
    print(ini)
    g[ini]=0
    q=util.PriorityQueue()#Queue to store an elemnet which is poped and explored every iteration of while
    q.push(ini,0)
    while ((q.isEmpty())==False):
        u=q.pop()

        if u not in visited2:
            visited2.append(u)
        
        if (problem.isGoalState(u)):
            fin=u
            break
        
        for v in problem.getSuccessors(u):
            if v[0] not in visited2:

                ##visited2.append(v[0])
                if v[0] not in g.keys():
                    g[v[0]]=g[u]+v[2]
                    actions[tuple((u,v[0]))]=v[1]
                    parent2[v[0]]=u
                    
                    q.push(v[0],g[v[0]]+heuristic(v[0],problem))
                else:
                    if g[v[0]]>g[u]+v[2]:
                        g[v[0]]=g[u]+v[2]
                        actions[tuple((u,v[0]))]=v[1]
                        parent2[v[0]]=u
                        q.push(v[0],g[v[0]]+heuristic(v[0],problem))
        
    x=fin
    path.append(x)
        
    while(parent2[x] !=ini): 
        act.append(actions[(parent2[x],x)])
        x = parent2[x]
        path.append(x)  
    path.append(ini)
    act.append(actions[(parent2[x],x)])
    path = path[::-1] 
    act=act[::-1]
    return act
