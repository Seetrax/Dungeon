# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"


    '''
    #DFS using stack
    #following GeeksForGeeks logic
    
    #each state is a tuple ( x , y )
    
    #problem.getStartState() returns start state ( x0 , y0 )
    #problem.getSuccessors(state) returns list of tuples. Tuple consist of (NextState,direction,cost)
    #problem.isGoalState(state) returns True if state is goal state, else false. 

    #INPUT : StartState, isGoalState(), getSuccessors()
    #OUTPUT : sequence of moves from StartState to GoalState

    #DFS LOGIC
    #Explore nodes from StartState. Avoid re-exploring nodes. Set parents of each states. 
    #If goal state is reached, traceback the parents. There you will get the directions from StartState
    #to GoalState. Put those directions in a list and return. 

    #IMPLEMENTATION
    #Maintain following Data structures : 
        #Stack S
        #Visited List visitedList
        #Parent Dictionary parent

    if problem.isGoalState(problem.getStartState()):
        return []
    
    from util import Stack

    visitedList=list()
    visitedList.append(problem.getStartState())

    parent=dict()

    s=Stack()
    Successors=problem.getSuccessors(problem.getStartState())
    for Successor in Successors:
        s.push(Successor)
        parent[Successor]=problem.getStartState()

    #to store the goalState for finding the path from StartState to GoalState
    goalStateWithFullInfo=[]
    
    while(s.isEmpty()==False):

        stateWithFullInfo=s.pop()
        state=stateWithFullInfo[0]
        visitedList.append(state)

        if problem.isGoalState(state)==True:
            goalStateWithFullInfo=stateWithFullInfo
            break

        Successors=problem.getSuccessors(state)
        for Successor in Successors:
            if Successor[0] not in visitedList:
                s.push(Successor)
                parent[Successor]=stateWithFullInfo
                
    else:
        return []
    

    GoalState=goalStateWithFullInfo
    path=[]#stores the directions
    currentState=GoalState
    path.append(GoalState[1])
    while True:
        currentState=parent[currentState]
        print(currentState)
        if currentState==problem.getStartState():
            return path
        else:
            path.insert(0,currentState[1])

    '''

    if problem.isGoalState(problem.getStartState()):
        return []

    from util import Stack

    Frontier=Stack()
    #frontier contains the unexplored nodes(RELEVANT) ordered with respect to the estimated minimum cost 
    #of path from startState to Goal state through that node. 

    PathQueue=Stack()
    #PathQueue stores the cost of the paths for each nodes in the Frontier(i.e, the priority queue that
    #contains the unexplored RELEVANT nodes. )

    #GUTENS of this procedure : eventually the Goal State will be added to the Frontier(unexplored
    #RELEVANT priority queue) and when it is popped, we get the exact minimum cost path from the startState
    #to the goalState. The only thing heuristic do is to reduce the search space. 


    exploredStates=[]
    currentPath=[]


    Frontier.push(problem.getStartState())
    currentState=Frontier.pop()

    while(problem.isGoalState(currentState)==False):
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            Successors =problem.getSuccessors(currentState)
            for Successor in Successors:
                if Successor not in exploredStates:
                    #cost=problem.getCostOfActions(currentPath+[Successor[1]])
                    #cost+=heuristic(Successor[0],problem)
                    Frontier.push(Successor[0])
                    PathQueue.push(currentPath+[Successor[1]])
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()
        else:
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()

    return currentPath

    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    '''
    if problem.isGoalState(problem.getStartState()):
        return []
   
    from util import Queue

    visitedList=list()
    visitedList.append(problem.getStartState())

    parent=dict()

    s=Queue()
    Successors=problem.getSuccessors(problem.getStartState())
    for Successor in Successors:
        s.push(Successor)
        parent[Successor]=problem.getStartState()
        visitedList.append(Successor[0])

    #to store the goalState for finding the path from StartState to GoalState
    goalStateWithFullInfo=[]
   
    while(s.isEmpty()==False):

        stateWithFullInfo=s.pop()
        state=stateWithFullInfo[0]
       

        if problem.isGoalState(state)==True:
            goalStateWithFullInfo=stateWithFullInfo
            break

        Successors=problem.getSuccessors(state)
        for Successor in Successors:
            if Successor[0] not in visitedList:
                s.push(Successor)
                parent[Successor]=stateWithFullInfo
                visitedList.append(Successor[0])
               
    else:
        return []
   

    GoalState=goalStateWithFullInfo
    path=[]#stores the directions
    currentState=GoalState
    path.append(GoalState[1])
    while True:
        currentState=parent[currentState]
        print(currentState)
        if currentState==problem.getStartState():
            return path
        else:
            path.insert(0,currentState[1])
    '''

    if problem.isGoalState(problem.getStartState()):
        return []

    from util import Queue

    Frontier=Queue()
    #frontier contains the unexplored nodes(RELEVANT) ordered with respect to the estimated minimum cost 
    #of path from startState to Goal state through that node. 

    PathQueue=Queue()
    #PathQueue stores the cost of the paths for each nodes in the Frontier(i.e, the priority queue that
    #contains the unexplored RELEVANT nodes. )

    #GUTENS of this procedure : eventually the Goal State will be added to the Frontier(unexplored
    #RELEVANT priority queue) and when it is popped, we get the exact minimum cost path from the startState
    #to the goalState. The only thing heuristic do is to reduce the search space. 


    exploredStates=[]
    currentPath=[]


    Frontier.push(problem.getStartState())
    currentState=Frontier.pop()

    while(problem.isGoalState(currentState)==False):
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            Successors =problem.getSuccessors(currentState)
            for Successor in Successors:
                if Successor not in exploredStates:
                    #cost=problem.getCostOfActions(currentPath+[Successor[1]])
                    #cost+=heuristic(Successor[0],problem)
                    Frontier.push(Successor[0])
                    PathQueue.push(currentPath+[Successor[1]])
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()
        else:
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()

    return currentPath

    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    '''

    #INPUT : StartState, isGoalState(), getSuccessors()
    #OUTPUT : A solution or Failure
    #Solution : Sequence of moves from StartState to GoalState

    #Required Data Structures : 
        #Node : Tuple of State=StartState and Path_Cost=0. 
        #Frontier : A Priority Queue ordered by Path Cost, initially only contains Node
        #Explored : An Empty List, same as visitedList

    #Additional Book-keeping :
        #Parent Dictionary parent

    #Problem : 
        #1. Getting the sequence of actions
        

    if problem.isGoalState(problem.getStartState()):
        return []

    from util import PriorityQueue

    Frontier=PriorityQueue()
    Explored=[]
    Node=[problem.getStartState(),0]

    parent={}
    goalState=[]

    Frontier.push(Node[0],Node[1])

    print("I am going to explore")

    while Frontier.isEmpty()==False:
        #Just in case
        heapForCheck=Frontier.heap
        t=heapForCheck[0]
        Node[0]=t[2];Node[1]=t[0]

        Frontier.pop()

        if problem.isGoalState(Node[0]):
            print("I have found the goal state")
            goalState=Node[0]
            break
        
        Explored.append(Node[0])

        print(Node[0],"I haven't found the goal state")
        Successors=problem.getSuccessors(Node[0])
        for Successor in Successors:
            if Successor[0] not in Explored:
                Frontier.update(Successor[0],Successor[2]+Node[1])
                
                for (priority,_,item) in heapForCheck:
                    if item==Successor[0]:
                        if priority==Successor[2]+Node[1]:
                            parent[Successor[0]]=(Node[0],Successor[1])
                        else:
                            pass
        
    else:
        return []
   
    path=[]#stores the directions
    currentState=[goalState]
    print("Going to enter the True while loop")
    while True:
        if currentState[0]==problem.getStartState():
            print("I am in if")
            print(path)
            return path
            break
        else:
            currentState=parent[currentState[0]]
            path.insert(0,currentState[1])
    '''

    if problem.isGoalState(problem.getStartState()):
        return []

    from util import PriorityQueue

    Frontier=PriorityQueue()
    #frontier contains the unexplored nodes(RELEVANT) ordered with respect to the estimated minimum cost 
    #of path from startState to Goal state through that node. 

    PathQueue=PriorityQueue()
    #PathQueue stores the cost of the paths for each nodes in the Frontier(i.e, the priority queue that
    #contains the unexplored RELEVANT nodes. )

    #GUTENS of this procedure : eventually the Goal State will be added to the Frontier(unexplored
    #RELEVANT priority queue) and when it is popped, we get the exact minimum cost path from the startState
    #to the goalState. The only thing heuristic do is to reduce the search space. 


    exploredStates=[]
    currentPath=[]


    Frontier.push(problem.getStartState(),0)
    currentState=Frontier.pop()

    while(problem.isGoalState(currentState)==False):
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            Successors =problem.getSuccessors(currentState)
            for Successor in Successors:
                if Successor not in exploredStates:
                    cost=problem.getCostOfActions(currentPath+[Successor[1]])
                    #cost+=heuristic(Successor[0],problem)
                    Frontier.push(Successor[0],cost)
                    PathQueue.push(currentPath+[Successor[1]],cost)
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()
        else:
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()

    return currentPath

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #INPUT : StartState, isGoalState(), getSuccessors()
    #OUTPUT : A solution or Failure
    #Solution : Sequence of moves from StartState to GoalState

    #Required Data Structures : 
        #Node : Tuple of State=StartState and Path_Cost=0. 
        #Frontier : A Priority Queue ordered by Path Cost, initially only contains Node
        #Explored : An Empty List, same as visitedList

    #Additional Book-keeping :
        #Parent Dictionary parent

    #Problem : 
        #1. Getting the sequence of actions
    
    
    if problem.isGoalState(problem.getStartState()):
        return []

    from util import PriorityQueue

    Frontier=PriorityQueue()
    #frontier contains the unexplored nodes(RELEVANT) ordered with respect to the estimated minimum cost 
    #of path from startState to Goal state through that node. 

    PathQueue=PriorityQueue()
    #PathQueue stores the cost of the paths for each nodes in the Frontier(i.e, the priority queue that
    #contains the unexplored RELEVANT nodes. )

    #GUTENS of this procedure : eventually the Goal State will be added to the Frontier(unexplored
    #RELEVANT priority queue) and when it is popped, we get the exact minimum cost path from the startState
    #to the goalState. The only thing heuristic do is to reduce the search space. 


    exploredStates=[]
    currentPath=[]


    Frontier.push(problem.getStartState(),0)
    currentState=Frontier.pop()

    while(problem.isGoalState(currentState)==False):
        if currentState not in exploredStates:
            exploredStates.append(currentState)

            Successors =problem.getSuccessors(currentState)
            for Successor in Successors:
                if Successor not in exploredStates:
                    cost=problem.getCostOfActions(currentPath+[Successor[1]])
                    cost+=heuristic(Successor[0],problem)
                    Frontier.push(Successor[0],cost)
                    PathQueue.push(currentPath+[Successor[1]],cost)
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()
        else:
            currentPath=PathQueue.pop()
            currentState=Frontier.pop()

    return currentPath


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
