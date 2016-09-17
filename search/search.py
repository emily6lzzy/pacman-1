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

class Coordinate:
    """
    This class defines the object that represents each pacman map's coordinate
    """

    def __init__(self, array):
        self.coordinate = array[0]
        self.direction = array[1] if len(array) > 1 else None
        self.cost = array[2] if len(array) > 2 else None

    def __eq__(self, other):
        return self.coordinate == other.coordinate

    def __str__(self):
        return "%s -- %s -- %d" % (str(self.coordinate), self.direction, self.cost)

    __repr__ = __str__
        

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
    from util import PriorityQueueWithFunction

    priorityFunction = lambda item: item.cost + (predecessors[str(item.coordinate)].cost \
        if str(item.coordinate) in predecessors else 0)

    node = Coordinate([problem.getStartState(), None, 0])
    predecessors = {}
    explored = []
    frontier = PriorityQueueWithFunction(priorityFunction)

    if problem.isGoalState(node.coordinate):
        return []

    frontier.push(node)
    while not frontier.isEmpty():
        node = frontier.pop()
        explored.append(node)

        for successor in problem.getSuccessors(node.coordinate):
            successor = Coordinate(successor)

            if successor not in explored:
                predecessors[str(successor.coordinate)] = node

                if problem.isGoalState(successor.coordinate):
                    return getPredecessorsDirections(predecessors, Coordinate([problem.getStartState()]), successor)

                try:
                    frontier.update(successor, priorityFunction(successor))
                except Exception, e:
                    frontier.push(successor)
                
    raise AssertionError("Error: solution not found")

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
    directions = []
    current = end
    while str(current.coordinate) in predecessors:
        directions.append(current.direction)
        current = predecessors[str(current.coordinate)]

    directions.reverse()
    return directions


def genericSearch(problem, frontier):
    """ 
    A generic search function that decides which nodes will be explored 
    base on frontier pop's policy
    """
    node = Coordinate([problem.getStartState(), None, 0])
    predecessors = {}
    explored = []

    frontier.push(node)
    while not frontier.isEmpty():
        node = frontier.pop()

        if problem.isGoalState(node.coordinate):
            return getPredecessorsDirections(predecessors, Coordinate([problem.getStartState()]), node)

        if node not in explored:
            explored.append(node)
        
            for successor in problem.getSuccessors(node.coordinate):
                successor = Coordinate(successor)
                if successor not in explored:
                    frontier.push(successor)
                    predecessors[str(successor.coordinate)] = node

    raise AssertionError("Error: solution not found")

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
