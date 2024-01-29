from lAgents import ReinforcementAgent
import random,util,math
import copy
'''QLearningAgent is a child class of ReinforcementAgent. Some of the important
features of this class :

    getQvalue - gets the Q-value corresponding to to a state action pair
    computeValueFromQValues - gets Value of a state (maximum of all Q values)
    computeActionFromQValues - gets an action that maximizes the Q value of that state action pair
    getAction -  return an action at random with probablity of epsilon or returns the Actions based on Q values
    getPolicy - returns policy associated with the state
    getValue - returns Value associated with the state
    update - this function updates the Q values everytime a reward is obtained on an episode by transition from 1 state to another
    '''
class QLearningAgent(ReinforcementAgent):
    def __init__(self, world,omni=False, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, world,omni=False, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1)
        "*** YOUR CODE HERE ***"
        self.Q=util.Counter()
    def getQValue(self, state, action):
        return self.Q[(state,action)]
        util.raiseNotDefined()

    def computeValueFromQValues(self, state):
        act=self.getLegalActions(state)
        if act==():
            return 0.0
        maxa=-99999999
        for i in act:
            if maxa<self.Q[(state,i)]:
                maxa=self.Q[(state,i)]
        return maxa
        
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        act=self.getLegalActions(state)
        if act==():
            return None
        maxi=-99999999
        maxa=None
        for i in act:
            if maxi<self.Q[(state,i)]:
                maxi=self.Q[(state,i)]
                maxa=i
        return maxa
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    def getAction(self, state):
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        
        st=random.choices([1,0],weights=[self.epsilon,1-self.epsilon],k=1)[0]
        if st==1:
            action=random.choice(legalActions)
        else:
            action=self.computeActionFromQValues(state)
        return action
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward: float):
        actions=self.getLegalActions(nextState)
        if actions==():
            sample=reward
        else:
            maxi=-999999999999
            for i in actions:
                if self.Q[(nextState,i)]>maxi:
                    maxi=self.Q[(nextState,i)]
            sample=reward+self.discount*(maxi)
        self.Q[(state,action)]=(1-self.alpha)*self.Q[(state,action)]+self.alpha*sample
            

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)
