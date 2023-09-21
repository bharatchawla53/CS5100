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
    # a LIFO stack 
    frontier = util.Stack()

    # a set to track visited nodes
    visited = []

    # add state to the stack and initial empty list for the path
    frontier.push((problem.getStartState(), []))

    while not frontier.isEmpty():
        # chooses the shallowest node in the frontier
        node, path = frontier.pop()

        # check if the node is a goal state
        if (problem.isGoalState(node)):
            return path

        # add node to the visited set if it has not been visited
        if node not in visited:
            visited.append(node)

            # explore node's successors
            for successor, action, stepCost in problem.getSuccessors(node):
                frontier.push((successor, path + [action]))                    

    return None

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # a FIFO queue 
    frontier = util.Queue()

    # a set to track visited nodes
    visited = []

    # add state to the queue and initial empty list for the path
    frontier.push((problem.getStartState(), []))

    while not frontier.isEmpty():
        # chooses the shallowest node in the frontier
        node, path = frontier.pop()

        # check if the node is a goal state
        if (problem.isGoalState(node)):
            return path

        # add node to the visited set if it has not been visited 
        if node not in visited:
            visited.append(node)

            # explore node's successors
            for successor, action, stepCost in problem.getSuccessors(node):
                frontier.push((successor, path + [action]))                    

    return None

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # a priority queue to track varying cost for each path
    frontier = util.PriorityQueue()

    # a set to track visited nodes
    visited = []

    # add state to the queue, initial empty list for the path, and cost so far for the priority queue to maintain
    frontier.push((problem.getStartState(), [], 0), 0)

    while not frontier.isEmpty():
        # chooses the lowest-cost node 
        node, path, cost = frontier.pop()

        # check if the node is a goal state
        if (problem.isGoalState(node)):
            return path

        # add node to the visited set if it has not been visited 
        if node not in visited:
            visited.append(node)

            # explore node's successors
            for successor, action, stepCost in problem.getSuccessors(node):
                # update frontier if child is in frontier with higher path cost, else update will insert it to the priority queue
                frontier.update((successor, path + [action], cost + stepCost), cost + stepCost)

    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # a priority queue to track varying cost for each path
    frontier = util.PriorityQueue()

    # a set to track visited nodes
    visited = []

    # calculate heuristic cost 
    heuristicCost = heuristic(problem.getStartState(), problem)
    # add state to the queue, initial empty list for the path, and cost so far for the priority queue to maintain
    frontier.push((problem.getStartState(), [], 0), 0 + heuristicCost)

    while not frontier.isEmpty():
        # chooses the lowest-cost node 
        node, path, cost = frontier.pop()

        # check if the node is a goal state
        if (problem.isGoalState(node)):
            return path

        # add node to the visited set if it has not been visited 
        if node not in visited:
            visited.append(node)

            # explore node's successors
            for successor, action, stepCost in problem.getSuccessors(node):
                # update frontier if child is in frontier with higher path cost (cost + heuristic cost), else update will insert it to the priority queue
                heuristicCost = heuristic(successor, problem)
                frontier.update((successor, path + [action], cost + stepCost), cost + stepCost + heuristicCost)

    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
