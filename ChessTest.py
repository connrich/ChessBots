import chess
from random import randint
import time

class RandomPlayer(object):
    def __init__(self, board, colour):
        self.game_board = board
        self.legal_moves = []

    # Pass in the current board state
    def getMove(self, board):
        self.game_board = board
        self.legal_moves.clear()
        for legal_move in self.game_board.legal_moves:
            self.legal_moves.append(legal_move)

        random = randint(0, len(self.legal_moves)-1)
        random_move = self.legal_moves[random]

        return random_move

class BasicEvalPlayer(object):
    def __init__(self, board, colour):
        self.colour = colour
        self.game_board = board
        self.legal_moves = []

        self.pieceValues = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 3.5}

    def evaluateBoardState(self, board):
        # TODO
        ranks = board.fen().split('/')
        ranks[-1] = ranks[-1].split(' ')[0]  # Strips extraneous information
        wht_eval = 0
        blk_eval = 0
        for rank in ranks:
            for char in rank:
                if char.isdigit():
                    pass
                elif char.isupper():
                    wht_eval += self.pieceValues[char.lower()]
                elif char.islower():
                    blk_eval += self.pieceValues[char]
                else:
                    pass
        print('white eval: ', wht_eval, ', black eval: ', blk_eval)

    def evalLegalMoves(self, board):
        self.legal_moves.clear()
        for legal_move in board.legal_moves:
            self.legal_moves.append(legal_move)



    def getMove(self, board):
        self.game_board = board
        print(self.evaluateBoardState(board))
        self.legal_moves.clear()
        for legal_move in self.game_board.legal_moves:
            self.legal_moves.append(legal_move)
        move = self.legal_moves[0]
        return move

if __name__ == "__main__":

    realtimeboard = chess.Board()

    white = RandomPlayer(realtimeboard, chess.WHITE)
    black = BasicEvalPlayer(realtimeboard, chess.BLACK)

    while not realtimeboard.is_game_over():
        colour_to_move = realtimeboard.turn
        if colour_to_move == chess.WHITE:
            move = white.getMove(realtimeboard)
        elif colour_to_move == chess.BLACK:
            move = black.getMove(realtimeboard)

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
