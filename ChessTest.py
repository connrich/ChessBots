import chess
from random import randint
import time

class Player(object):
    def __init__(self, board):
        self.game_board = board
        self.legal_moves = []

    # Pass in the current board state
    def getRandomMove(self, board):
        self.game_board = board
        for legal_move in self.game_board.legal_moves:
            self.legal_moves.append(legal_move)
        random_move = self.legal_moves[randint(0, len(self.legal_moves)-1)]
        return random_move

realtimeboard = chess.Board()

white = Player(realtimeboard)
black = Player(realtimeboard)

if __name__ == "__main__":
    while not realtimeboard.is_game_over():
        colour_to_move = realtimeboard.turn
        print(colour_to_move)
        if colour_to_move == chess.WHITE:
            print('white to move')
            move = white.getRandomMove(realtimeboard)
        elif colour_to_move == chess.BLACK:
            print('black to move')
            move = black.getRandomMove(realtimeboard)

        if move in realtimeboard.legal_moves:
            realtimeboard.push(move)
            print(realtimeboard)
        else:
            print('error')
        # time.sleep(5)

    print(realtimeboard.result())

# legal_moves = []
# for legal_move in realtimeboard.legal_moves:
#     legal_moves.append(legal_move)
# random_move = legal_moves[randint(0, len(legal_moves))]
# move = random_move
# print(legal_moves)
#
# test_board = realtimeboard
# print(test_board)
#
# if move in realtimeboard.legal_moves:
#     test_board.push(move)