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
    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
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
        
        # loop over for n iterations
        for i in range(self.iterations):
            
            # dictionary to track best q values for each state
            newValues = util.Counter()
            
            # get all states for mdp
            for s in self.mdp.getStates():
               
                # list to track values for the given state
                values = []
                
                # check if state is a terminal state
                if self.mdp.isTerminal(s):
                    values.append(0)
                
                # track max value for each state
                #max_value = float("-inf")
                
                # get all actions for a state 's'
                for a in self.mdp.getPossibleActions(s):
                    
                   # compute Q value for state 's' and action 'a'
                   values.append(self.computeQValueFromValues(s, a))
                   
                # take the max value
                maxValue = max(values)
                
                # update the dictionary with max value for a state 's'
                newValues[s] = maxValue
        
            self.values = newValues
           
            

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
        
        value = 0.0
        
         # get transition state for given action 'a' and state 's'
        for (nextState, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
                        
            # calculate reward for being in state 's', taking an action 'a' and ending up in next state 's`'
            reward = self.mdp.getReward(state, action, nextState) 
                                    
            # calculate new value
            value += float(prob) * (reward + (self.discount * float(self.values[nextState])))
        
        return value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        
        # dictionary to track policies for the given state
        policies = util.Counter()
        
        # get all actions for a state
        actions = self.mdp.getPossibleActions(state)
        
        # if actions size is 0 and state is terminal state
        if len(actions) == 0 & self.mdp.isTerminal(state):
            return None
            
        # loop over all the actions
        for a in actions:
            
            # get Q value for a given action
            policies[a] = self.getQValue(state, a)
            
        # find the action with best policy
        return policies.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
