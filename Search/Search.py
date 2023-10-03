import util


'''SearchProblem class gives a general outlook of a search problem statement.
Any search problem statement must have start state , goal state,  and cost fn.
This abstract class shows the functions :

getStartState:
    retruns the start state of the agent
isGoalState :
    checks whetjer the agent has reached goal state
getSuccessors :
    generates successors for a given state of the agent (position)
getCostofActions
class SearchProblem:
    def getStartState(self):
        return None

    def isGoalState(self, state):
        return None

    def getSuccessors(self, state):
        
        return None'''


class PosProblem(SearchProblem):

    def __init__(self, gameState,world,goal=(1,1), costFn = lambda x: 1, start=None):
        """
        Stores the start and goal.

        gameState: A GameState object (game.py)
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

        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)
        #print(successors)
        return successors

    
''' Write ur implementation of dfs in this function.
Dfs explores the entire depth of the tree from a node
before it starts exploration of nest node'''
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
def astar(problem, heuristic=nullHeuristic):
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


##Methods :
bfs=BreadthFirstSearch
dfs=DepthFirstSearch
ucs=UniformCostSearch
astar=AstarSearch
