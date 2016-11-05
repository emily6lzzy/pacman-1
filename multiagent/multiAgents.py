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


from util import manhattanDistance
from game import Directions
import random, util
import sys
import pdb

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

    def terminalTest(self, gameState, level):
      return level / gameState.getNumAgents() >= self.depth or len(gameState.getLegalActions()) == 0;


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
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
        """
        return self.maxValue(gameState, 0)[0];


    def maxValue(self, gameState, level):
      if self.terminalTest(gameState, level):
        return self.evaluationFunction(gameState);

      values = [(None, -sys.maxsize)] + \
               [(pacmanAction, self.minValue(gameState.generateSuccessor(0, pacmanAction), level + 1)) 
                for pacmanAction in gameState.getLegalActions()];

      maxValueResult = max(values, key = lambda v: v[1]);
      if level != 0: return maxValueResult[1];
      else: return maxValueResult;


    def minValue(self, gameState, level):
      currentAgentIndex = level % gameState.getNumAgents();
      nextAgentIndex = (level + 1) % gameState.getNumAgents();

      if self.terminalTest(gameState, level):
        return self.evaluationFunction(gameState);

      values = [(None, sys.maxsize)];
      if nextAgentIndex == 0:
        values += [(agentAction, self.maxValue(gameState.generateSuccessor(currentAgentIndex, agentAction), level + 1)) 
                  for agentAction in gameState.getLegalActions(currentAgentIndex)];
      else:
        values += [(agentAction, self.minValue(gameState.generateSuccessor(currentAgentIndex, agentAction), level + 1)) 
                  for agentAction in gameState.getLegalActions(currentAgentIndex)];

      minValueResult = min(values, key = lambda v: v[1]);
      return minValueResult[1];


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.maxValue(gameState, 0, -sys.maxsize, sys.maxsize)[0];


    def maxValue(self, gameState, level, alpha, beta):
      if self.terminalTest(gameState, level):
        return self.evaluationFunction(gameState);

      value = (None, -sys.maxsize);
      for pacmanAction in gameState.getLegalActions():
        newValue = (pacmanAction, self.minValue(gameState.generateSuccessor(0, pacmanAction), level + 1, alpha, beta));
        value = max([value, newValue], key = lambda v: v[1]);
        alpha = max(alpha, value[1]);      
        
        if value[1] > beta:
          return value[1] if level != 0 else value;

      return value[1] if level != 0 else value;


    def minValue(self, gameState, level, alpha, beta):
      currentAgentIndex = level % gameState.getNumAgents();
      nextAgentIndex = (level + 1) % gameState.getNumAgents();

      if self.terminalTest(gameState, level):
        return self.evaluationFunction(gameState);

      value = (None, sys.maxsize);
      for agentAction in gameState.getLegalActions(currentAgentIndex):
        if nextAgentIndex == 0:
          newValue = (agentAction, self.maxValue(gameState.generateSuccessor(currentAgentIndex, agentAction), level + 1, alpha, beta));
        else:
          newValue = (agentAction, self.minValue(gameState.generateSuccessor(currentAgentIndex, agentAction), level + 1, alpha, beta));

        value = min([value, newValue], key = lambda v: v[1]);
        beta = min(beta, value[1]);

        if value[1] < alpha:
          return value[1];

      return value[1];

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        nextMove = max(self.maxValue(gameState, 0), key = lambda v: v[1])[0];
        return nextMove;


    def maxValue(self, gameState, level):
      if self.terminalTest(gameState, level):
        return self.evaluationFunction(gameState);

      pFactor = 1.0 / len(gameState.getLegalActions());
      values = \
               [(pacmanAction, self.minValue(gameState.generateSuccessor(0, pacmanAction), level + 1)) 
                for pacmanAction in gameState.getLegalActions()];

      if level != 0:
        return max(v[1] for v in values);
      else:
        return values;

    def minValue(self, gameState, level):
      currentAgentIndex = level % gameState.getNumAgents();
      nextAgentIndex = (level + 1) % gameState.getNumAgents();

      if self.terminalTest(gameState, level):
        return self.evaluationFunction(gameState);

      values = [];
      pFactor = 1.0 / len(gameState.getLegalActions(currentAgentIndex));

      if nextAgentIndex == 0:
        values += [(agentAction, pFactor * self.maxValue(gameState.generateSuccessor(currentAgentIndex, agentAction), level + 1)) 
                  for agentAction in gameState.getLegalActions(currentAgentIndex)];
      else:
        values += [(agentAction, pFactor * self.minValue(gameState.generateSuccessor(currentAgentIndex, agentAction), level + 1)) 
                  for agentAction in gameState.getLegalActions(currentAgentIndex)];

      return sum(v[1] for v in values);


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION 

      I considered four different metrics to build the evaluation function:
      * Food distance
      * Capsule distance
      * Ghost distance
      * scared ghost distance

      Also, I used weighted average in order to some metrics. The statements
      that defined the weights -- along with their values -- are descibred below:
      (1) The pacman should focus on pursue a ghost when it is scared (100)
      (2) The pacman should focus on eating capsules in favor of food (30) 
      (3) The pacman should avoid ghosts (-10)
      (4) The pacman should focus on eating food whenever it's possible (10)
    """
    FOOD_WEIGHT = 10.0;
    CAPSULE_WEIGHT = 30.0;
    SCARED_GHOST_WEIGHT = 100.0;
    GHOST_WEIGHT = -10.0;

    newPos = currentGameState.getPacmanPosition();
    foods = currentGameState.getFood().asList();
    capsules = currentGameState.getCapsules();
    ghosts = currentGameState.getGhostStates();

    distancesToFood = [manhattanDistance(newPos, foodPos) for foodPos in foods];
    distancesToCapsules = [manhattanDistance(newPos, capsulePos) for capsulePos in capsules];
    distancesToScaredGhosts = [manhattanDistance(newPos, ghostState.getPosition()) 
                              for ghostState in ghosts if ghostState.scaredTimer > 0];
    distancesToGhosts = [manhattanDistance(newPos, ghostState.getPosition()) 
                        for ghostState in ghosts if ghostState.scaredTimer == 0];
    
    minFoodDistance = min(distancesToFood) if len(distancesToFood) > 0 else 1;
    minCapsuleDistance = min(distancesToCapsules) if len(distancesToCapsules) > 0 else 1;
    minGhostDistance = min(distancesToGhosts) if len(distancesToGhosts) > 0 else 1;

    # Because it should be better for lower values
    foodValue = FOOD_WEIGHT / minFoodDistance;
    capsuleValue = CAPSULE_WEIGHT / minCapsuleDistance;
    ghostValue = GHOST_WEIGHT / sum(distancesToGhosts,1);
    scaredGhostValue = SCARED_GHOST_WEIGHT / sum(distancesToScaredGhosts, 1);
    scoreValue = currentGameState.getScore();

    evalutaedValue = scoreValue + ghostValue + scaredGhostValue + foodValue + capsuleValue;
    return evalutaedValue;


# Abbreviation
better = betterEvaluationFunction

# 