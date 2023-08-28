import random
import util
def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()
def mh(x1,x2):
    return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])
def normalize(dic):
    tt=sum(dic.values())
    for i in dic.keys():
        dic[i]=dic[i]/tt
class Entity:
    def __init__(self, index=0):
        self.index = index

    def Act(self, state):
        return None
    def prob(self,state):
        return None
def sample(distribution, values=None):
    items = sorted(distribution.items())
    distribution = [i[1] for i in items]
    values = [i[0] for i in items]
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    choice = random.random()
    i, total = 0, distribution[0]
    while choice > total:
        i += 1
        total += distribution[i]
    return values[i]
class lion(Entity):
    def __init__(self,index):
        self.index=index
    def Act(self,state):
        dist = self.prob(state)
        if len(dist) == 0 or dist==None:
            return None
        else:
            return util.chooseFromDistribution(dist)
    def prob(self,state):
        poss_act=state.getActions(self.index)
        #print(poss_act)
        agentindex=self.index
        if poss_act!=[]:
            new_pos=[]
            for i in poss_act:
                if i=='u':
                    new_pos.append([(state.world.lion_pos[agentindex-1][0],state.world.lion_pos[agentindex-1][1]-1),i])
                elif i=='r':
                    new_pos.append([(state.world.lion_pos[agentindex-1][0]+1,state.world.lion_pos[agentindex-1][1]),i])
                elif i=='d':
                    new_pos.append([(state.world.lion_pos[agentindex-1][0],state.world.lion_pos[agentindex-1][1]+1),i])
                elif i=='l':
                    new_pos.append([(state.world.lion_pos[agentindex-1][0]-1,state.world.lion_pos[agentindex-1][1]),i])
            distances=[mh(pos[0],state.agent_pos) for pos in new_pos]
            best_dist=min(distances)
            dist=util.Counter()
            bestAct=[]
            bestProb=0.8
            
            for i in range(len(new_pos)):
                if distances[i]==best_dist:
                    bestAct.append(new_pos[i][1])
            for a in bestAct:
                dist[a] = bestProb / len(bestAct)
            for a in poss_act:
                dist[a] += (1-bestProb) / len(poss_act)
            '''print(poss_act)
            print(bestAct)
            print(dist)
            print("FFF")'''
            normalize(dist)
            
            return dist
class MultiAgentSearchAgent(Entity):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evalFn = evalFn
        self.depth = int(depth)
    def evaluationFunction(self,state):
        if self.evalFn== 'scoreEvaluationFunction':
            return scoreEvaluationFunction(state)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def evals(self,gameState,index,depth):
        if   depth==0 or gameState.getActions(index)==[]:
            if gameState.isWin():
                return self.evaluationFunction(gameState)
            elif gameState.isLose():
                return self.evaluationFunction(gameState)
            else:
                return self.evaluationFunction(gameState)
        elif index==0:
            maxi=-9999999999999999999999999999999999999999999999999999999
            for i in gameState.getActions(index):
                if index+1==self.n:
                    ev=self.evals(gameState.generateSuccessor(index,i),0,depth-1)
                else:
                    ev=self.evals(gameState.generateSuccessor(index,i),index+1,depth)
                maxi=max(maxi,ev)
            return maxi
        elif index!=0:
            mini=9999999999999999999999999999999999999999999999999999999999999
            for i in gameState.getActions(index):
                if index+1==self.n:
                    ev=self.evals(gameState.generateSuccessor(index,i),0,depth-1)
                else:
                    ev=self.evals(gameState.generateSuccessor(index,i),index+1,depth)
                
                mini=min(mini,ev)

            return mini

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        ut={}
        self.n=gameState.num_agents
        for i in gameState.getActions(self.index):
            if self.n>1:
                    ut[i]=self.evals(gameState.generateSuccessor(self.index,i),self.index+1,self.depth)
            else:
                    ut[i]=self.evals(gameState.generateSuccessor(self.index,i),self.index,self.depth)
            ##ut[i]=self.evals(gameState.generateSuccessor(self.index,i),self.depth-1)
        print(ut)
        m1=max(ut.values())
        
        return list(ut.keys())[list(ut.values()).index(m1)]
        util.raiseNotDefined()
