# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action) --> Returns list of (nextState, prob) pairs
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #print("iter: ", self.iterations)
        for iter in range(self.iterations):
            #print("Iteration: ",iter)
            S = self.mdp.getStates()
            
            # print(S)  S:   ['TERMINAL_STATE', (0, 0), (0, 1), (0, 2)]
            # A = {'exit','north','west','south','east'}
            # A = 'exit' takes current state to terminal state and reward is 10
            # 'TERMINAL_STATE' loops forever with reward 0
            # self.values is a dictionary 
            # for i in range(len(S)):

            
            # test/p1/3 
            # ['TERMINAL_STATE', (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), 
            # (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
            # (2, 1), (2, 2), (2, 3), (2, 4), (2, 5)]

            #print( self.mdp.getPossibleActions((2,1)) )
            # for i in range(len(S)):
            #     print("state ",S[i]," ",self.mdp.getPossibleActions(S[i]),"\n")
            #     for j in range(len(S)):
            #         if( self.mdp.getReward(S[i], 'south', S[j])  == 10):
            #             print("i: ",i," j: ",j)

            # print(self.mdp.getPossibleActions(S[0]))
            # print(len(self.mdp.getPossibleActions(S[1])))
            # print(self.computeActionFromValues(S[1]))
            # print(self.mdp.getTransitionStatesAndProbs(S[1], 'exit'))
            # print(self.mdp.getReward(S[1], 'exit', S[0]))
            # print("values ",self.values)
            tmp_values = util.Counter()
            for i in range(len(S)):
                a_star = self.computeActionFromValues(S[i])
                #print(i,"-th action: ",a_star)
                tmp_values[S[i]] = self.computeQValueFromValues(S[i],a_star)
                #print("value: ",self.computeQValueFromValues(S[i],a_star))
            self.values = tmp_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        if(self.mdp.isTerminal(state)):
            return 0.0
        listOfStatesAndProbs = []
        listOfStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action) # [(state,prob)]
        # print("state: ", state)
        # print("action: ", action)
        # print(listOfStatesAndProbs)
        # print("Length: ",len(listOfStatesAndProbs))
        q = 0
        for i in range(len(listOfStatesAndProbs)):
            nextState = listOfStatesAndProbs[i][0]
            p = listOfStatesAndProbs[i][1]
            r = self.mdp.getReward(state, action, nextState)
            q += p * (r + self.discount * self.values[nextState])
        
        return q
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        
        if(self.mdp.isTerminal(state)):
            return None
        #print(state)
        A = self.mdp.getPossibleActions(state)
        # print("state: ", state)
        # print("Action: ", A)
        
        index = 0
        q = -888888888.0
        for i in range(len(A)):
            if(q < self.computeQValueFromValues(state,A[i])):
                q = self.computeQValueFromValues(state,A[i]) 
                index = i
        return A[index]    

        
        
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

