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

def depthFirstSearch(problem):
    """Performs DFS in order to find a path for the solution"""
    from util import Stack
    return genericSearch(problem, Stack())

def breadthFirstSearch(problem):
    """Performs BFS in order to find a path for the solution"""
    from util import Queue
    return genericSearch(problem, Queue())


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def getPredecessorsDirections(predecessors, start, end):
    """Build directions array from predecessors sequence."""
    directions = [end[1]]
    current = end[0]
    while predecessors[str(current)][0] != start:
        directions.append(predecessors[str(current)][1])
        current = predecessors[str(current)][0]

    directions.reverse()
    return directions


def genericSearch(problem, frontier):
    """ 
    A generic search function that decides which nodes will be explored 
    base on frontier pop's policy
    """
    node = [problem.getStartState()]
    pathCost = 0
    predecessors = {}
    explored = set()

    if problem.isGoalState(node[0]):
        return predecessors

    frontier.push(node)
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.add(node[0])
        
        for successor in problem.getSuccessors(node[0]):
            if successor[0] not in explored and successor not in frontier.list:
                predecessors[str(successor[0])] = node

                if problem.isGoalState(successor[0]):
                    return getPredecessorsDirections(predecessors, problem.getStartState(), successor)

                frontier.push(successor)

    raise AssertionError("Error: solution not found")

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
