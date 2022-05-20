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

        "*** YOUR CODE HERE ***"
        from util import manhattanDistance
        
        if successorGameState.isWin():
            return 99999999999

        # Manhattan dist food from sucessor
        listefood = newFood.asList()
        foodDist = [0]
        for i in listefood:
            foodDist.append(manhattanDistance(newPos,i))

        # Manhattan dist ghost from sucessor 
        GhostX = []
        ghostDist = []
        for i in newGhostStates:
            GhostX.append(i.getPosition())
        for y in GhostX:
            ghostDist.append(manhattanDistance(newPos,y))

        # Manhattan ghost and now state
        ghostNow = []
        ghostNowPos = []
        for i in currentGameState.getGhostStates():
            ghostNow.append(i.getPosition())

        for y in ghostNow:
            ghostNowPos.append(manhattanDistance(newPos,y))

        #"Initialisation" 
        score = 0
        FoodCurrentLeft = len(currentGameState.getFood().asList())
        FoodLeft = len(listefood)
        nbrgumgum = len(successorGameState.getCapsules())
        newtime = sum(newScaredTimes)
        
        score += successorGameState.getScore() - currentGameState.getScore()
        if action == Directions.STOP:
            score -= 10
        if newPos in currentGameState.getCapsules():
            score += 150 * nbrgumgum
        if FoodLeft < FoodCurrentLeft:
            score += 200
        score -= FoodLeft * 10
        if newtime > 0 :
            if min(ghostNow) < min(GhostX):
                score += 200
            else:
                score += 200
        else:
            if min(ghostNow) < min(GhostX):
                score -=100
            else:
                score += 200

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
        ##################################################
        action = gameState.getLegalActions(0)
        scored = -999999
        returned = ''
        ##################################################
        
        def MinState(gameState,depth,agentIndex):
            mini = 99999999
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            actionLegal = gameState.getLegalActions(agentIndex)
            for i in actionLegal:
                nexter = gameState.generateSuccessor(agentIndex, i)
                if (gameState.getNumAgents() - 1) == agentIndex:
                    mini = min(mini,MaxState(nexter,depth))
                else:
                    mini = min(mini,MinState(nexter,depth,agentIndex+1))
            return mini

        def MaxState(gameState,depth):
            actdepth = depth + 1
            if gameState.isWin() or gameState.isLose() or actdepth==self.depth:
                return self.evaluationFunction(gameState)
            maxi = -9999999
            actionLegal = gameState.getLegalActions(0)
            for i in actionLegal:
                nexter = gameState.generateSuccessor(0,i)
                maxi = max(maxi,MinState(nexter,actdepth,1))
            return maxi

        for i in action:
            nextState = gameState.generateSuccessor(0,i)
            score = MinState(nextState,0,1)
            if score > scored:
                returned = i
                scored = score
        return returned
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ##################################################
        actions = gameState.getLegalActions(0)
        actScore = -99999999
        returnAction = ''
        alpha = -9999999
        beta = 999999999
        ##################################################
        
        def MinState(gameState,depth,agentIndex,alpha,beta):
            ##################################################
            mini = 9999999999
            actions = gameState.getLegalActions(agentIndex)
            beta1 = beta
            ##################################################
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            for i in actions:
                successor= gameState.generateSuccessor(agentIndex,i)
                if agentIndex == (gameState.getNumAgents()-1):
                    mini = min (mini,MaxState(successor,depth,alpha,beta1))
                    if mini < alpha:
                        return mini
                    beta1 = min(beta1,mini)
                else:
                    mini = min(mini,MinState(successor,depth,agentIndex+1,alpha,beta1))
                    if mini < alpha:
                        return mini
                    beta1 = min(beta1,mini)
            return mini
        
        def MaxState(gameState,depth,alpha, beta):
            ##################################################
            actDepth = depth + 1
            maxi = -99999999999
            actions = gameState.getLegalActions(0)
            alpha1 = alpha
            ##################################################
            
            if gameState.isWin() or gameState.isLose() or actDepth==self.depth:
                return self.evaluationFunction(gameState)
            for i in actions:
                successor= gameState.generateSuccessor(0,i)
                maxi = max (maxi,MinState(successor,actDepth,1,alpha1,beta))
                if maxi > beta:
                    return maxi
                alpha1 = max(alpha1,maxi)
            return maxi

        for i in actions:
            nextState = gameState.generateSuccessor(0,i)
            score = MinState(nextState,0,1,alpha,beta)
            if score > actScore:
                returnAction = i
                actScore = score  
            if score > beta:
                return returnAction
            alpha = max(alpha,score)
        return returnAction

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
        ##################################################
        action = gameState.getLegalActions(0)
        scored = -999999
        returned = ''
        ##################################################
        
        def Expected(gameState,depth,agentIndex):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            action = gameState.getLegalActions(agentIndex)
            nbr = len(action)
            val = 0
            for i in action:
                nexted = gameState.generateSuccessor(agentIndex,i)
                if (gameState.getNumAgents() - 1) == agentIndex:
                    temp = MaxState(nexted,depth)
                else:
                    temp = Expected(nexted,depth,agentIndex+1)
                val += temp
            if nbr == 0:
                return 0
            final = float(val)/float(nbr)
            return final

        def MaxState(gameState,depth):
            ##################################################
            actDepth = depth + 1
            maxi = -999999
            action = gameState.getLegalActions(0)
            totalmaxvalue = 0
            numberofactions = len(action)
            ##################################################
            if gameState.isWin() or gameState.isLose() or actDepth==self.depth:
                return self.evaluationFunction(gameState)
            for i in action:
                nexted = gameState.generateSuccessor(0,i)
                maxi = max(maxi,Expected(nexted,actDepth,1))
            return maxi

        for i in action:
            nextState = gameState.generateSuccessor(0,i)
            score = Expected(nextState,0,1)
            if score > scored:
                returned = i
                scored = score
        return returned

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    from util import manhattanDistance
    ##################################################
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ##################################################

    listefood = newFood.asList()
    foodDist = [0]
    ghostX = []
    nbrgumgum = len(currentGameState.getCapsules())
    score = 0
    temp = 0
    Pasdebraspasdechocolat = len(newFood.asList(False)) 
    for y in ghostX:
        ghostDist.append(manhattanDistance(newPos,y))
    for i in newGhostStates:
        ghostX.append(i.getPosition())
    ghostDist = [0]
    for y in ghostX:
        ghostDist.append(manhattanDistance(newPos,y))
    scaredTime = sum(newScaredTimes)
    scaredDist = sum(ghostDist)

    if sum(foodDist) > 0 :
        temp = (1.0/sum(foodDist))
    
    score += currentGameState.getScore() + temp + Pasdebraspasdechocolat


    if (scaredTime > 0):
        score += scaredTime + (-1 * nbrgumgum) + (-1 * scaredDist)
    else :
        score += scaredDist + nbrgumgum
    return score
    
# Abbreviation
better = betterEvaluationFunction
