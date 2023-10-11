from human import Agent
import random,util,time

class ValueEstAgent(Agent):
    def __init__(self, alpha=1.0, epsilon=0.05, gamma=0.8, numTraining = 10):
        self.alpha = float(alpha)
        self.epsilon = float(epsilon)
        self.discount = float(gamma)
        self.numTraining = int(numTraining)
    def getQValue(self, state, action):
        util.raiseNotDefined()

    def getValue(self, state):
        util.raiseNotDefined()

    def getPolicy(self, state):
        util.raiseNotDefined()

    def getAction(self, state):
        util.raiseNotDefined()

class ReinforcementAgent(ValueEstAgent):
    def update(self, state, action, nextState, reward):
        util.raiseNotDefined()
    def getLegalActions(self,state):

        '''if (self.agent_pos in self.pit_pos) or (self.agent_pos in self.gold_pos) or (self.agent_pos in self.lion_pos)::
            return []'''
        lis=[]
        if self.world.agent_pos[1]-1 >= 0 and (self.world.agent_pos[0],self.world.agent_pos[1]-1) not in self.world.wall_pos:
                lis.append('u')
        if self.world.agent_pos[0]+1 < self.world.num_cols and (self.world.agent_pos[0]+1,self.world.agent_pos[1]) not in self.world.wall_pos:
                lis.append('r')
        if self.world.agent_pos[1]+1 < self.world.num_rows and (self.world.agent_pos[0],self.world.agent_pos[1]+1) not in self.world.wall_pos:
                lis.append('d')
        if self.world.agent_pos[0]-1 >= 0 and (self.world.agent_pos[0]-1,self.world.agent_pos[1]) not in self.world.wall_pos:
                lis.append('l')
        return lis

    def observeTransition(self, state,action,nextState,deltaReward):

        self.episodeRewards += deltaReward
        self.update(state,action,nextState,deltaReward)

    def startEpisode(self):
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def stopEpisode(self):
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            # Take off the training wheels
            self.epsilon = 0.0    # no exploration
            self.alpha = 0.0      # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def __init__(self, world,omni=False, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        """
        actionFn: Function which takes a state and returns the list of legal actions

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
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


        self.episodesSoFar = 0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

