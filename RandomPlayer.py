import chess
from random import randint

class RandomPlayer(object):
    def __init__(self, board, colour):
        self.current_board = board
        self.legal_moves = []

    # Pass in the current board state
    def getMove(self, board):
        self.current_board = board
        self.legal_moves.clear()
        for legal_move in self.current_board.legal_moves:
            self.legal_moves.append(legal_move)

        random = randint(0, len(self.legal_moves)-1)
        random_move = self.legal_moves[random]

        return random_move