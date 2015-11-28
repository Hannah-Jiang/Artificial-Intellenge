# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from multiprocessing.managers import State

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
    """print "score ",scores
    print "choice", legalMoves[chosenIndex]
    print "action", legalMoves[chosenIndex]"""

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
    if action == 'Stop':
        return 0
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    foodList = newFood.asList()
    score = 0
    ghostScore = 0
    ghostDistance = min([util.manhattanDistance(newPos,ghost.getPosition()) for ghost in newGhostStates])
    if ghostDistance < 3:
            ghostScore -= ghostDistance / 100;
        
    if len(foodList) > 0:
        foodDistance = min([util.manhattanDistance(newPos, food) for food in foodList])
    else:
        foodDistance = 0

    score = 3.0 / (1 + len(foodList)) + ghostScore + 1.0/(1000 + foodDistance)
    return score

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

    Directions.STOP:
    The stop direction, which is always legal

    gameState.generateSuccessor(agentIndex, action):
    Returns the successor game state after an agent takes an action
    
    gameState.getNumAgents():
    Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    
    score = float('-inf');
    returnAction = Directions.STOP
    for action in legalMoves:
        state= gameState.generateSuccessor(0,action)
        tempScore = self.min_value(state, 1)
        if score <= tempScore:
            returnAction = action
            score = tempScore

    return returnAction

  def max_value(self, gameState, depth):
    if depth > self.depth:
        return self.evaluationFunction(gameState)
    else:
        depth += 1
    score = []
    actions = gameState.getLegalActions(0)
    if Directions.STOP in actions:
        actions.remove(Directions.STOP)
    if len(actions) > 0:
        for action in actions:
            state = gameState.generateSuccessor(0, action)
            s = self.min_value(state, depth)
            score.append(s)
    else:
        score.append(self.evaluationFunction(gameState))
    return max(score)
        
  def min_value(self, gameState, depth):
    if depth > self.depth:
        return self.evaluationFunction(gameState)
    else:
        depth += 1
    score = []
    numAgent = gameState.getNumAgents()
    i = 1
    while i <= numAgent-1:
        actions = gameState.getLegalActions(i)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)
        if len(actions) > 0:
            for action in actions:
                state = gameState.generateSuccessor(i, action)
                s = self.max_value(state, depth)
                score.append(s)
        else:
            score.append(self.evaluationFunction(gameState))
        i += 1
    return min(score)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    legalMoves = gameState.getLegalActions(0)
    
    score = float('-inf')
    max = -100000000000000
    min = 100000000000000
    returnAction = Directions.STOP
    for action in legalMoves:
        state= gameState.generateSuccessor(0,action)
        tempScore = self.min_value(state, 1, max, min)
        if score <= tempScore:
            returnAction = action
            score = tempScore

    return returnAction

  def max_value(self, gameState, depth, max, min):
    if depth > self.depth:
        return self.evaluationFunction(gameState)
    else:
        depth += 1
    actions = gameState.getLegalActions(0)
    if Directions.STOP in actions:
        actions.remove(Directions.STOP)
    if len(actions) > 0:
        for action in actions:
            state = gameState.generateSuccessor(0, action)
            s = self.min_value(state, depth, max, min)
            if s > min:
                    return s
            if max > s: max = max
            else: max = s
    else:
        s = self.evaluationFunction(gameState)
    if max > s: return max
    else: return s
        
  def min_value(self, gameState, depth, max, min):
    if depth > self.depth:
        return self.evaluationFunction(gameState)
    else:
        depth += 1
    numAgent = gameState.getNumAgents()
    i = 1
    while i <= numAgent-1:
        actions = gameState.getLegalActions(i)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)
        if len(actions) > 0:
            for action in actions:
                state = gameState.generateSuccessor(i, action)
                s = self.max_value(state, depth, max, min)
                if s < max:
                    return s
                if min < s: min = min
                else: min = s
        else:
            s = self.evaluationFunction(gameState)
        i += 1
    if min < s: return min
    else: return s

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
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"
    legalMoves = gameState.getLegalActions(0)
    
    score = float('-inf');
    returnAction = Directions.STOP
    for action in legalMoves:
        state= gameState.generateSuccessor(0,action)
        tempScore = self.exp_value(state, 1)
        if score <= tempScore:
            returnAction = action
            score = tempScore

    return returnAction

  def max_value(self, gameState, depth):
    if depth > self.depth:
        return self.evaluationFunction(gameState)
    else:
        depth += 1
    score = []
    actions = gameState.getLegalActions(0)
    if Directions.STOP in actions:
        actions.remove(Directions.STOP)
    if len(actions) > 0:
        for action in actions:
            state = gameState.generateSuccessor(0, action)
            s = self.exp_value(state, depth)
            score.append(s)
    else:
        score.append(self.evaluationFunction(gameState))
    return max(score)
        
  def exp_value(self, gameState, depth):
    if depth > self.depth:
        return self.evaluationFunction(gameState)
    else:
        depth += 1
    score = []
    numAgent = gameState.getNumAgents()
    i = 1
    while i <= numAgent-1:
        actions = gameState.getLegalActions(i)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)
        if len(actions) > 0:
            for action in actions:
                state = gameState.generateSuccessor(i, action)
                s = self.max_value(state, depth)
                score.append(s)
        else:
            score.append(self.evaluationFunction(gameState))
        i += 1
    return sum(score)/len(score)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """successorGameState = currentGameState;
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodList = newFood.asList()
    score = 0
    ghostDistance = min([util.manhattanDistance(newPos,ghost.getPosition()) for ghost in newGhostStates])
        
    if len(foodList) > 0:
        foodDistance = min([util.manhattanDistance(newPos, food) for food in foodList])
    else:
        foodDistance = 0
    
    currentScore = currentGameState.getScore()
    
    if currentScore > 1000:
        score = 10.0 / (1 + len(foodList)) - ghostDistance/80 + 9.0/(1000 + foodDistance)
    elif currentScore > 500:
        score = 8.0 / (1 + len(foodList)) - ghostDistance/100 + 7.0/(1000 + foodDistance)
    elif currentScore > 300:
        score = 6.0 / (1 + len(foodList)) - ghostDistance/100 + 5.0/(1000 + foodDistance)
    elif currentScore > 0:
        score = 5.0 / (1 + len(foodList)) - ghostDistance/100 + 3.0/(1000 + foodDistance)
    elif currentGameState.getScore() < 0:
        score = 1.0 / (1 + len(foodList)) - ghostDistance/100 + 1.0/(1000 + foodDistance)
    elif currentGameState.getScore() < -200:
        score = 0.0 / (1 + len(foodList)) - ghostDistance/100 + 1.0/(1000 + foodDistance)
    elif currentGameState.getScore() < -400:
        score = 0.0 / (1 + len(foodList)) - ghostDistance/100 + 0.0/(1000 + foodDistance)
    return score
    """
    successorGameState = currentGameState;
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    capsuleList = successorGameState.getCapsules()
    foodList = newFood.asList()
    score = 0
    ghostDistance = min([util.manhattanDistance(newPos,ghost.getPosition()) for ghost in newGhostStates])
        
    if len(foodList) > 0:
        foodDistance = min([util.manhattanDistance(newPos, food) for food in foodList])
    else:
        foodDistance = 0
    
    if ghostDistance <= 1 and newScaredTimes[0] <= 1 :
        return -9999
    
    if len(capsuleList) > 0:
        capsulesDistance = min([util.manhattanDistance(newPos,capsule) for capsule in capsuleList])
    else:
        capsulesDistance = 0
    
    currentScore = currentGameState.getScore()
    
    ghostDistance = ghostDistance
   
        
    foodDistance = 1000 + foodDistance
    capsulesDistance = 1 / (100 + capsulesDistance)
    if currentScore > 1000:
        score = 10.0 / (1 + len(foodList)) - ghostDistance/100 + 9.0/foodDistance + capsulesDistance
    elif currentScore > 500:
        score = 8.0 / (1 + len(foodList)) - ghostDistance/100 + 7.0/foodDistance + capsulesDistance
    elif currentScore > 300:
        score = 6.0 / (1 + len(foodList)) - ghostDistance/100 + 5.0/foodDistance + capsulesDistance
    elif currentScore > 0:
        score = 5.0 / (1 + len(foodList)) - ghostDistance/100 + 3.0/foodDistance + capsulesDistance
    elif currentGameState.getScore() < 0:
        score = 3.0 / (1 + len(foodList)) - ghostDistance/100 + 1.0/foodDistance + capsulesDistance
    
    return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"

