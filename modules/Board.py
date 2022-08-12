from .Constants import *


class BoardState:
    def __init__(self):
        self.w = 0
        self.h = 0
        self.row_spaces = [0]*DEFAULT_BOARD_SIZE[1]
        self.flattencies = []
        self.binary = []

    def Save_from_board(board):
        bs = BoardState()
        bs.w = len(board[0])
        bs.h = len(board)
        for i in range(bs.h):
            bs.binary.append([])
            col_flattency = []
            for j in range(bs.w):
                col_space = 0
                if not board[i][j]: bs.row_spaces[i] += 1
                bs.binary[-1].append( 1 if board[i][j] else 0 )
                for k in range(i, bs.h):
                    if board[k][j]: break 
                    col_space += 1
                col_flattency.append(col_space)
            bs.flattencies.append(col_flattency)
        return bs



def Board():
    b = []
    for i in range(DEFAULT_BOARD_SIZE[1]):
        b.append([])
        for j in range(DEFAULT_BOARD_SIZE[0]):
            b[-1].append(0)
    return b, DEFAULT_BOARD_SIZE[0], DEFAULT_BOARD_SIZE[1]