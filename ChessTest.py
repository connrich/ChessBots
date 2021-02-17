import chess
from random import randint
from datetime import datetime

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

class BasicEvalPlayer(object):
    def __init__(self, board, colour):
        self.colour = colour
        self.current_board = board
        self.legal_moves = []

        self.pieceValues = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 3.5}

    def evaluateBoardState(self, board):
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
        return (wht_eval, blk_eval)

    def evalLegalMoves(self, board):
        self.legal_moves.clear()
        for legal_move in board.legal_moves:
            self.legal_moves.append(legal_move)

    def getMove(self, board):
        self.current_board = board
        self.legal_moves.clear()
        move = None
        for legal_move in self.current_board.legal_moves:
            self.legal_moves.append(legal_move)
            child_board = self.current_board.__copy__()
            child_board.push(legal_move)
            evals = self.evaluateBoardState(child_board)
            if self.colour == chess.WHITE:
                if child_board.is_checkmate():
                    move = legal_move
                    break
                elif evals[0] > evals[1]:
                    move = legal_move
            elif self.colour == chess.BLACK:
                if child_board.is_checkmate():
                    move = legal_move
                    break
                elif evals[0] < evals[1]:
                    move = legal_move

        if move == None:
            move = self.legal_moves[0]
        return move

if __name__ == "__main__":

    realtimeboard = chess.Board()

    white = RandomPlayer(realtimeboard, chess.WHITE)
    black = BasicEvalPlayer(realtimeboard, chess.BLACK)

    blk_total_score = 0
    wht_total_score = 0
    num_games = 10

    start = datetime.now()
    for game in range(num_games):
        realtimeboard.reset()
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
        result = realtimeboard.result().split('-')
        if result[0] == '1/2' or result[1] == '1/2':
            result[0] = 0.5
            result[1] = 0.5

        wht_total_score += float(result[0])
        blk_total_score += float(result[1])


    finish = datetime.now()
    print('White: ', wht_total_score, ' Black: ', blk_total_score)
    print(num_games, ' game(s) completed in ', finish-start,)
