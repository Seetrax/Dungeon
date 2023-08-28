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
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState,world, costFn = lambda x: 1, start=None):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        
        self.startState = gameState.agent_pos
        if start != None: self.startState = start
        self.goal = (world.num_cols-1,world.num_rows-1)
        self.costFn = costFn
        self.world=world
        
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        '''# For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable'''

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
def dfs(problem: SearchProblem):
    
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
def bfs(problem: SearchProblem):
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

def ucs(problem: SearchProblem):
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
