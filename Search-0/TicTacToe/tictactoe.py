"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    else:
        xcounter = 0
        ocounter = 0
        for x in board:
            xcounter += x.count(X)
            ocounter += x.count(O)
        counter = xcounter - ocounter
    return X if counter == 0 else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('Invalid Action')
    playerTurn = player(board)
    boardCopy = deepcopy(board)
    boardCopy[action[0]][action[1]] = playerTurn
    return boardCopy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    xwinner = ['X', 'X', 'X']
    owinner = ['O', 'O', 'O']
    # Horizontal Winner
    for x in board:
        if xwinner == x:
            return X
        elif owinner == x:
            return O

    # Diagonal Winner
    diagBoard = []
    for i in range(3): 
        diagBoard.append(board[i][i])
    if xwinner == diagBoard:
        return X
    elif owinner == diagBoard:
        return O

    # Second Diagonal Winner
    diagBoard = []
    j = 2
    for i in range(3):
        diagBoard.append(board[i][j])
        j -= 1
    if xwinner == diagBoard:
        return X
    elif owinner == diagBoard:
        return O
        
    # Vertical Winner
    for j in range(3):
        verBoard = []
        for i in range(3):
            verBoard.append(board[i][j])
        if xwinner == verBoard:
            return X
        elif owinner == verBoard:
            return O

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winnerPlayer = winner(board)
    if winnerPlayer:
        return True
    elif not([x for x in board if not(all(x))]):
        return True
    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winnerPlayer = winner(board)
    if winnerPlayer == "X":
        return 1
    elif winnerPlayer == "O":
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    playerTurn = player(board)
    if playerTurn == "X":
        # Max Player
        optimalAction = maxValue(board, -math.inf, math.inf)
    if playerTurn == "O":
        # Min Player
        optimalAction = minValue(board, -math.inf, math.inf)

    return optimalAction[1]

def maxValue(board, alpha, beta):
    if terminal(board):
        return utility(board)

    possibleActions = actions(board)
    v = (-math.inf, None)
    for action in possibleActions:
        minPlyrUtil = minValue(result(board, action), alpha, beta)
        if type(minPlyrUtil) == tuple:
            minPlyrUtil = minPlyrUtil[0] 
        if v[0] < minPlyrUtil:
            v = (minPlyrUtil, action)
        alpha = max(alpha, minPlyrUtil)
        if beta <= alpha: 
            break
    return v

def minValue(board, alpha, beta):
    if terminal(board):
        return utility(board)

    possibleActions = actions(board)
    v = (math.inf, None)
    for action in possibleActions:
        maxPlyrUtil = maxValue(result(board, action), alpha, beta)
        if type(maxPlyrUtil) == tuple:
            maxPlyrUtil = maxPlyrUtil[0] 
        if v[0] > maxPlyrUtil:
            v = (maxPlyrUtil, action)
        beta = min(beta, maxPlyrUtil)
        if beta <= alpha:
            break
    return v