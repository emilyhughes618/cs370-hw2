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
        print("Successor Game State:", successorGameState)
        print("New Position:", newPos)
        print("New Food:", newFood)
        print("New Ghost States", str(newGhostStates))
        print("New Scared Times:", newScaredTimes)

        score = 0
        newFoodList = newFood.asList()
        foodDistanceDict = {}
        # if food is close, reward that
        for food in newFoodList:
            if len(newFoodList) == 0:
                break
            foodDistanceDict[food] = manhattanDistance(newPos, food)
        if len(newFoodList) != 0:
            minDistance = min(foodDistanceDict.values())
            score += 1/minDistance
        #if ghost is on you, avoid at all costs
        print("Ghost:", newGhostStates[0].getPosition())
        for ghost in newGhostStates:
            if manhattanDistance(newPos, ghost.getPosition()) == 0:
                score -= 100
        # more important to go away from ghosts:
        ghostDistanceList = []
        ghostCount = 0
        for ghost in newGhostStates:
            ghostDistanceList.append(manhattanDistance(newPos, ghost.getPosition()))
            ghostCount += 1
        closestGhostDistance = min(ghostDistanceList)
        if closestGhostDistance != 0:
            score -= 2 * 1/closestGhostDistance
        #focus on food when power pellet works
        if sum(newScaredTimes) > 0:
            score += 4 * 1/closestGhostDistance
        return score + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
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
        #print(gameState.getLegalActions(0))
        #print("depth:", self.depth)
        numOfGhosts = gameState.getNumAgents() 
        retAction = []

        counter = 0
        def minimax(state, index, counter):
            if (state.isWin() or state.isLose() or (counter // state.getNumAgents()) == self.depth ):
                print(" should be at leaf node, My counter is:", counter)
                print("I am at a leaf node! My value is:", self.evaluationFunction(state))
                return self.evaluationFunction(state), ""
            maxVal = float("-inf")
            minVal = float("inf")
            bestAction = ""
            if index == 0:
                for action in state.getLegalActions(0):
                    print("line 184 My counter is:", counter)
                    print("line 184 My index is:", index)
                    print("line 185Action:", action)
                    currentVal = minimax(state.generateSuccessor(0, action), 1, counter + 1)[0]
                    if currentVal > maxVal:
                        maxVal = currentVal
                        print("line 189 Max Val:", maxVal)
                        bestAction = action
                return maxVal, bestAction
            if index != 0:
                #print("I'm at a min")
                for action in state.getLegalActions(index):
                    print("line 195 My counter is:", counter)
                    print("line 196 My index is:", index)
                    print("line 196 Action:", action)
                    if index <= state.getNumAgents() - 2:
                        currentVal = minimax(state.generateSuccessor(index, action), index + 1, counter + 1)[0]
                    else:
                        currentVal = minimax(state.generateSuccessor(index, action), 0, counter + 1)[0]
                    if currentVal < minVal:
                        minVal = currentVal
                        print("linw 203 My index is:", index)
                        print("line 204 Min Val:", minVal)
                        bestAction = action
                    print("line 206 my min val is:", minVal)
                return minVal, bestAction
            
                        



            
        def get_max(currentGameState, currentDepth):
            if (currentGameState.isWin() or currentGameState.isLose() or currentDepth == self.depth ):
                return self.evaluationFunction(currentGameState)
            
            
            bestAction = ""
            maxVal = float("-inf")
            for action in gameState.getLegalActions(0):
                moveVal = get_min(gameState.generateSuccessor(0, action), currentDepth)
                if(moveVal > maxVal):
                    maxVal = moveVal
                    bestAction = action
                
            retAction.append(bestAction)
            return maxVal
        
        def get_min(currentGameState, currentDepth):
            if (currentGameState.isWin() or currentGameState.isLose() or currentDepth == self.depth):
                return self.evaluationFunction(currentGameState)
            
            
            minVal = float("inf")
            for i in range(1, gameState.getNumAgents()):
                for action in gameState.getLegalActions(i): #only ghost will minimize   
                    #if(currentDepth == self.depth - 1):
                       # moveVal =  self.evaluationFunction(gameState.generateSuccessor(i, action))
                    
                    moveVal = get_max(gameState.generateSuccessor(i, action), currentDepth + 1)
                    
                    if moveVal < minVal:
                        minVal = moveVal
                
            return minVal
        
        #get_max(gameState, 0)
        ans = minimax(gameState, 0, 0)
        return ans[1]
        #return retAction[0]

            


        def is_terminal_node(currentGameState, searchedDepth):
            if (currentGameState.isWin() or currentGameState.isLose()) or searchedDepth == self.depth:
                return True
            return False

        def max_value(currentGameState, currentDepth):
            if is_terminal_node(currentGameState, currentDepth):
                return self.evaluationFunction, ""
            action = ""
            value = float("-inf")
            for action in gameState.getLegalActions(0): #only pacman will maximize max
                value2 = min_value(gameState.generateSuccessor(0, action), currentDepth)
                print("this is action")
                print(action)
                if value2 > value:
                    value = value2
            return value


        def min_value(currentGameState, currentDepth):
            if is_terminal_node(currentGameState, currentDepth):
                return self.evaluationFunction, ""
            action = ""
            value = float("inf")
            for i in range(1, numOfGhosts + 1):
                for action in gameState.getLegalActions(i): #only ghost will minimize 
                    
                    value2 = max_value(gameState.generateSuccessor(i, action), currentDepth)
                    if value2 > value:
                        value = value2
                if i == numOfGhosts + 1:
                    currentDepth += 1
            return value
        
        def main():
            # need to cut off minimax at a given depth
            depth = self.depth

        highest_value, optimal_action = max_value(gameState, 0)
        return optimal_action

        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        '''
        root = gameState
        def min_value(state, alpha, beta):
            if (state.isWin() or state.isLose() or (counter // state.getNumAgents()) == self.depth ):
                return self.evaluationFunction(state), ""
            minVal = float("inf")
            alpha = max(alpha, v)
            return 0
        
        def max_value(state, alpha, beta):
            if (state.isWin() or state.isLose() or (counter // state.getNumAgents()) == self.depth ):
                return self.evaluationFunction(state), ""
            maxVal = float("-inf")
            beta = min(beta, v)
            return 0
        

        max_value(root, float("-inf"), float("inf"))
        '''

        def minimax(state, index, counter, alpha, beta):
            if (state.isWin() or state.isLose() or (counter // state.getNumAgents()) == self.depth ):
                return self.evaluationFunction(state), ""
            maxVal = float("-inf")
            minVal = float("inf")
            bestAction = ""
            if index == 0:
                for action in state.getLegalActions(0):
                    currentVal = minimax(state.generateSuccessor(0, action), 1, counter + 1, alpha, beta)[0]
                    if currentVal > maxVal:
                        maxVal = currentVal
                        bestAction = action
                    alpha = max(alpha, maxVal)
                    if alpha > beta:
                        break
                return maxVal, bestAction
            if index != 0:
                for action in state.getLegalActions(index):
                    if index <= state.getNumAgents() - 2:
                        currentVal = minimax(state.generateSuccessor(index, action), index + 1, counter + 1, alpha, beta)[0]
                    else:
                        currentVal = minimax(state.generateSuccessor(index, action), 0, counter + 1, alpha, beta)[0]
                    if currentVal < minVal:
                        minVal = currentVal
                        bestAction = action
                    beta = min(beta, minVal)
                    if alpha > beta:
                        break
                return minVal, bestAction
        
        ans = minimax(gameState, 0, 0, float("-inf"), float("inf"))
        return ans[1]


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
        
        def minimax(state, index, counter):
            if (state.isWin() or state.isLose() or (counter // state.getNumAgents()) == self.depth ):
                #print(" should be at leaf node, My counter is:", counter)
                #print("I am at a leaf node! My value is:", self.evaluationFunction(state))
                return self.evaluationFunction(state), ""
            maxVal = float("-inf")
            minVal = float("inf")
            bestAction = ""
            if index == 0:
                for action in state.getLegalActions(0):
                    #print("line 184 My counter is:", counter)
                    #print("line 184 My index is:", index)
                    #print("line 185Action:", action)
                    currentVal = minimax(state.generateSuccessor(0, action), 1, counter + 1)[0]
                    if currentVal > maxVal:
                        maxVal = currentVal
                        #print("line 189 Max Val:", maxVal)
                        bestAction = action
                return maxVal, bestAction
            if index != 0:
                #print("I'm at a min")
                minVal = 0
                for action in state.getLegalActions(index):
                    #print("line 195 My counter is:", counter)
                    #print("line 196 My index is:", index)
                    #print("line 196 Action:", action)
                    if index <= state.getNumAgents() - 2:
                        currentVal = minimax(state.generateSuccessor(index, action), index + 1, counter + 1)[0]
                    else:
                        currentVal = minimax(state.generateSuccessor(index, action), 0, counter + 1)[0]
                    minVal += currentVal
                    #print("line 206 my min val is:", minVal)
                return minVal, bestAction
            
        #get_max(gameState, 0)
        ans = minimax(gameState, 0, 0)
        return ans[1]
        #return retAction[0]
            




        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    '''
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
    
        "*** YOUR CODE HERE ***"
    '''
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

     

    score = 0
    newFoodList = newFood.asList()
    foodDistanceDict = {}
    # if food is close, reward that
    for food in newFoodList:
        if len(newFoodList) == 0:
            break
        foodDistanceDict[food] = manhattanDistance(newPos, food)
    if len(newFoodList) != 0:
        minDistance = min(foodDistanceDict.values())
        score += 1/minDistance
    #if ghost is on you, avoid at all costs
    print("Ghost:", newGhostStates[0].configuration.pos)
    for ghost in newGhostStates:
        if manhattanDistance(newPos, ghost.configuration.pos) == 0:
            score -= 100
    # more important to go away from ghosts:
    ghostDistanceList = []
    ghostCount = 0
    for ghost in newGhostStates:
        ghostDistanceList.append(manhattanDistance(newPos, ghost.configuration.pos))
        ghostCount += 1
    closestGhostDistance = min(ghostDistanceList)
    if closestGhostDistance != 0:
        score -= 2 * 1/closestGhostDistance
    #focus on food when power pellet works
    if sum(newScaredTimes) > 0:
        score += 4 * 1/closestGhostDistance
    return score + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction