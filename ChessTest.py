import chess
from random import randint
import time

class RandomPlayer(object):
    def __init__(self, board):
        self.game_board = board
        self.legal_moves = []

    # Pass in the current board state
    def getRandomMove(self, board):
        self.game_board = board
        self.legal_moves.clear()
        for legal_move in self.game_board.legal_moves:
            self.legal_moves.append(legal_move)

        random = randint(0, len(self.legal_moves)-1)
        random_move = self.legal_moves[random]

        return random_move

realtimeboard = chess.Board()

white = RandomPlayer(realtimeboard)
black = RandomPlayer(realtimeboard)

if __name__ == "__main__":
    while not realtimeboard.is_game_over():
        colour_to_move = realtimeboard.turn
        if colour_to_move == chess.WHITE:
            move = white.getRandomMove(realtimeboard)
        elif colour_to_move == chess.BLACK:
            move = black.getRandomMove(realtimeboard)

        legal_moves = realtimeboard.legal_moves
        if move in legal_moves:
            realtimeboard.push(move)
            print()
            print(realtimeboard)
        else:
            print('Illegal Move:')
            print(realtimeboard)
            print(move)
            print(legal_moves)
            break
        # time.sleep(5)

    print(realtimeboard.result())
