from lAgents import ValueEstAgent
import MDP,util
class ValueIterAgent(ValueEstAgent):
    def __init__(self,world,omni=False, discount = 0.9, iterations = 100):
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
        self.mdp = MDP.MDP(world)
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"
        for l in range(self.iterations):
            delta=0
            S=self.mdp.getStates()
            
            prev=self.values.copy()
            #print(S)
            for i in S:
                if not (self.mdp.Terminal(i)):
                    maxi=-999999999
                    for a in self.mdp.getActions(i):
                        T=self.mdp.TransitionStates(i,a)
                        v=0
                        for k in T:
                            v+=k[1]*(self.mdp.getReward(i,a,k[0])+self.discount*(prev[k[0]])) 
                        if maxi<v:
                               maxi=v
                    self.values[i]=maxi
        print(self.values)
    def getValue(self, state):
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        if self.mdp.Terminal(state):
            return None
        act=self.mdp.getActions(state)
        T=self.mdp.TransitionStates(state,action)
        v=0
        for k in T:
            v+=k[1]*(self.mdp.getReward(state,action,k[0])+self.discount*(self.values[k[0]]))
        return v
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        if self.mdp.Terminal(state):
            return None
        act=self.mdp.getActions(state)
        maxi=-999999999
        maxa=None
        for a in self.mdp.getActions(state):
                    v=self.computeQValueFromValues(state,a)
                    if maxi<v:
                           maxi=v
                           maxa=a
        return maxa
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
