import random
'''MDP class defines all the necessary information required to properly
define a markov decision process. you may read through this class
to get a better understanding of how mdp is implemented for Reinforcement
learning in this game'''
class MDP:

    def __init__(self,world,noise=0.0,discount=1.0,livingreward=0.0):
        self.noise=noise
        self.discount=discount
        self.livingreward=livingreward
        self.start_state=(world.agent_col,world.agent_row)
        self.world=world
        self.num_agents=world.num_agents
        self.agent_pos=world.agent_pos
        self.gold_pos=world.gold_pos
        self.lion_pos=world.lion_pos
        self.pits_pos=world.pits_pos
        self.score=world.score
        self.num_rows=world.num_rows
        self.num_cols=world.num_cols
        self.states=[]
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.states.append((i,j))
        
    def update_agent(self,x,y):
        self.agent_pos=(x,y)

    def nextState(self,state,action):
        acts=self.PossibleActions(state)
        if action in acts:
                if action=='u':
                    state.agent_pos=(state.agent_pos[0],state.agent_pos[1]-1)
                elif action=='r':
                    state.agent_pos=(state.agent_pos[0]+1,state.agent_pos[1])
                elif action=='d':
                    state.agent_pos=(state.agent_pos[0],state.agent_pos[1]+1)
                elif action=='l':
                    state.agent_pos=(state.agent_pos[0]-1,state.agent_pos[1])
    def getStates(self):
        """
        Return a list of all states in the MDP.
        Not generally possible for large MDPs.
        """
        return self.states

    def getStartState(self):
        """
        Return the start state of the MDP.
        """
        return self.start_state

    def getActions(self, state):
        """
        Return list of possible actions from 'state'.
        """
        
        if self.Terminal(state):
            return []
        lis=[]
        if state[1]-1 >= 0 and (state[0],state[1]-1) not in self.world.wall_pos:
                lis.append('u')
        if state[0]+1 < self.world.num_cols and (state[0]+1,state[1]) not in self.world.wall_pos:
                lis.append('r')
        if state[1]+1 < self.world.num_rows and (state[0],state[1]+1) not in self.world.wall_pos:
                lis.append('d')
        if state[0]-1 >= 0 and (state[0]-1,state[1]) not in self.world.wall_pos:
                lis.append('l')
        return lis

    def TransitionStates(self, state, action):
        """
        Returns list of (nextState, prob) pairs
        representing the states reachable
        from 'state' by taking 'action' along
        with their transition probabilities.

        Note that in Q-Learning and reinforcment
        learning in general, we do not know these
        probabilities nor do we directly model them.
        """
        acts=self.getActions(state)
        lis=[]
        if acts!=[]:
            gamestates={'u':(state[0],state[1]-1),'r':(state[0]+1,state[1]),'l':(state[0]-1,state[1]),'d':(state[0],state[1]+1)}
            for a in acts:
                if action==a:
                    lis.append((gamestates[a],1.0-self.noise))
                else:
                    lis.append((gamestates[a],self.noise))
        return lis
    def getReward(self, state, action, nextState):
        """
        Get the reward for the state, action, nextState transition.

        Not available in reinforcement learning.
        """
        
        if not self.Terminal(nextState):
            return self.livingreward
        elif (nextState in self.gold_pos):
            return 10.0
        else:
            return -10.0
    def Terminal(self, state):
        """
        Returns true if the current state is a terminal state.  By convention,
        a terminal state has zero future rewards.  Sometimes the terminal state(s)
        may have no possible actions.  It is also common to think of the terminal
        state as having a self-loop action 'pass' with zero reward; the formulations
        are equivalent.
        """
        if (state in self.pits_pos) or (state in self.gold_pos) or (state in self.lion_pos):
            return True
        return False
