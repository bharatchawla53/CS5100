# multiAgents.py
# --------------
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


from math import inf
from tkinter import CENTER
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        # note : calculate distance to nearest food and also check if a ghost exists closer to pacman's location

        # list of food coordinates
        newFoodList = newFood.asList()

        # store distances to food item from a given pacman's position
        distances = []

        # loop through food list where the coordinates are true to find the closest distance to food palet
        for food in newFoodList:

            # calculate manhattan distance between pacman's position and food position
            d = util.manhattanDistance(food, newPos)

            # append calculated distance
            distances.append(d)

        # get the min distance to the food
        closestFood = float(inf)
        if (len(distances) != 0):
            closestFood = min(distances)
        
        # after calculating closest distance to food, check if there is a ghost close to pacman's location 
        # and if so, return negative value for score
        for ghostState in newGhostStates:
            
            # calculate manhattan distance between pacman's position and ghost positon 
            # and if it's less than 3, then return the minimum float value since actions takes the max value
            if (util.manhattanDistance(ghostState.getPosition(), newPos)) < 3:
                return -float(inf)

        # taking reciprocal of distance to food than just the values themselves 
        return successorGameState.getScore() + 1 / closestFood

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
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
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def minimax(self, gameState: GameState, agentIndex, depth):

        # check if the game state is a terminal state
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return "", self.evaluationFunction(gameState)

        # check if the next agent is PACMAN i.e. agentIndex = 0, else ghosts
        if (agentIndex == 0):
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.minValue(gameState, agentIndex, depth)

    def maxValue(self, gameState: GameState, agentIndex, depth):
        #v = -float(inf)
        value = -float(inf)
        action = ""

        for a in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, a)
            v = self.minimax(successor, agentIndex + 1, depth)[1]
            
            if v > value:
                value = v
                action = a

        return action, value

    def minValue(self, gameState: GameState, agentIndex, depth):
        #v = float(inf)
        value = float(inf)
        action = ""

        # check if agentIndex has reached max agents and if so, set the index back to pacman
        nextAgent = agentIndex + 1
        if (nextAgent == gameState.getNumAgents()):
            nextAgent = 0
            depth = depth + 1

        for a in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, a)
            v = self.minimax(successor, nextAgent, depth)[1]
            
            if v < value:
                value = v
                action = a

        return action, value


    def getAction(self, gameState: GameState):
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
        
        # agent's index that we are evaluating i.e. PACMAN
        agentIndex = self.index
        result = self.minimax(gameState, agentIndex, 0)
        return result[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def alphaBetaMinimax(self, gameState: GameState, agentIndex, depth, alpha, beta):
 
        # check if the game state is a terminal state
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return "", self.evaluationFunction(gameState)
            
        # check if the next agent is PACMAN i.e. agentIndex = 0, else ghosts
        if (agentIndex == 0):
            return self.maxValue(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.minValue(gameState, agentIndex, depth, alpha, beta)
            
    def maxValue(self, gameState: GameState, agentIndex, depth, alpha, beta):
        value = -float(inf)
        action = ""

        for a in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, a)
            v = self.alphaBetaMinimax(successor, agentIndex + 1, depth, alpha, beta)[1]
            
            if v > value:
                value = v
                action = a
            
            if value > beta:
                return action, value
            
            alpha = max(alpha, value)
             
        return action, value
                
    def minValue(self, gameState: GameState, agentIndex, depth, alpha, beta):
        value = float(inf)
        action = ""
            
        # check if agentIndex has reached max agents and if so, set the index back to pacman
        nextAgent = agentIndex + 1
        if (nextAgent == gameState.getNumAgents()):
            nextAgent = 0
            depth = depth + 1
                
        for a in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, a)
            v = self.alphaBetaMinimax(successor, nextAgent, depth, alpha, beta)[1]
            
            if v < value:
                value = v
                action = a
            
            if value < alpha:
                return action, value
            
            beta = min(beta, value)
            
        return action, value

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        # agent's index that we are evaluating i.e. PACMAN
        agentIndex = self.index; 
        
        # pacman's best option on path to root
        alpha = -float(inf)
        
        # ghost's best option on path to root
        beta = float(inf)
        
        result = self.alphaBetaMinimax(gameState, agentIndex, 0, alpha, beta)
        return result[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def expectiMax(self, gameState: GameState, agentIndex, depth):
 
        # check if the game state is a terminal state
        if (gameState.isWin() or gameState.isLose() or depth == self.depth):
            return "", self.evaluationFunction(gameState)
            
        # check if the next agent is PACMAN i.e. agentIndex = 0, else ghosts
        if (agentIndex == 0):
            return self.maxValue(gameState, agentIndex, depth)
        else:
            return self.expValue(gameState, agentIndex, depth)
            
    def maxValue(self, gameState: GameState, agentIndex, depth):
        value = -float(inf)
        action = ""

        for a in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, a)
            v = self.expectiMax(successor, agentIndex + 1, depth)[1]
            
            if v > value:
                value = v
                action = a
            
        return action, value
                
    def expValue(self, gameState: GameState, agentIndex, depth):
        value = 0
        action = ""
                    
        # check if agentIndex has reached max agents and if so, set the index back to pacman
        nextAgent = agentIndex + 1
        if (nextAgent == gameState.getNumAgents()):
            nextAgent = 0
            depth = depth + 1
            
        # successor's probability
        p = 1.0 / float(len(gameState.getLegalActions(agentIndex)))
        
        for a in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, a)
            value += p * self.expectiMax(successor, nextAgent, depth)[1]
            
        return action, value

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        # agent's index that we are evaluating i.e. PACMAN
        agentIndex = self.index
        result = self.expectiMax(gameState, agentIndex, 0)
        return result[0]

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
