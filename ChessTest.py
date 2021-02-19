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

class MiniMaxPlayer(object):
    def __init__(self, board, colour, depth=2):
        self.current_board = board
        self.colour = colour
        self.depth = depth
        self.legal_moves = []

        self.pieceValues = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 3.5}

    def getMove(self, board):
        self.current_board = board
        chosen_board, eval = self.miniMax(self.current_board, self.depth, True)
        print('max eval found: ', eval)
        # for _ in range(self.depth-1):
        #     move = chosen_board.pop()
        return chosen_board.pop()

    def miniMax(self, board, depth, maxPlayer):
        if board.is_game_over():
            result = board.result().split('-')
            print(result)

            if self.colour == chess.WHITE and result[0] == '1':
                return board, float('inf')
            elif self.colour == chess.BLACK and result[1] == '1':
                return board, float('inf')
            else:
                return board, -100.0
        elif depth == 0:
            eval = self.evaluateBoardState(board)
            if maxPlayer:
                if self.colour == chess.WHITE:
                    eval = eval[0] - eval[1]
                elif self.colour == chess.BLACK:
                    eval = eval[1] - eval[0]
                else:
                    print('max player zero depth eval error')
                    eval = 0
                return board, eval
            elif not maxPlayer:
                if self.colour != chess.WHITE:
                    eval = eval[0] - eval[1]
                elif self.colour != chess.BLACK:
                    eval = eval[1] - eval[0]
                else:
                    print('min player zero depth eval error')

                return board, eval

        # if depth == 0 or board.is_game_over():
        #     board.result()
        #     eval = self.evaluateBoardState(board)
        #     if maxPlayer:
        #         if self.colour == chess.WHITE:
        #             eval = eval[0] - eval[1]
        #         elif self.colour == chess.BLACK:
        #             eval = eval[1] - eval[0]
        #         else:
        #             print('max player zero depth eval error')
        #             eval = 0
        #         return board, eval
        #     elif not maxPlayer:
        #         if self.colour != chess.WHITE:
        #             eval = eval[0] - eval[1]
        #         elif self.colour != chess.BLACK:
        #             eval = eval[1] - eval[0]
        #         else:
        #             print('min player zero depth eval error')
        #
        #         return board, eval
        if maxPlayer:
            maxEval = float('-inf')
            for legalmove in board.legal_moves:
                child_board = board.__copy__()
                child_board.push(legalmove)
                # eval = self.evaluateBoardState(child_board)
                # print(eval)

                return_board, eval = self.miniMax(child_board, depth-1, not maxPlayer)

                # if self.colour == chess.WHITE:
                #     eval = eval[0] - eval[1]
                # elif self.colour == chess.BLACK:
                #     eval = eval[1] - eval[0]
                # else:
                #     print('max player eval error')
                #     eval = 0

                if eval > maxEval:
                    maxEval = eval
                    best_board = child_board
                    print(best_board, maxEval)
            return best_board, maxEval
        elif not maxPlayer:
            minEval = float('inf')
            for legalmove in board.legal_moves:
                # print(legalmove)
                # print(legalmove in board.legal_moves)
                child_board = board.__copy__()
                child_board.push(legalmove)
                # eval = self.evaluateBoardState(child_board)

                return_board, eval = self.miniMax(child_board, depth-1, not maxPlayer)
                # if self.colour != chess.WHITE:
                #     eval = eval[0] - eval[1]
                # elif self.colour != chess.BLACK:
                #     eval = eval[1] - eval[0]
                # else:
                #     print('min player eval error')
                if eval < minEval:
                    minEval = eval
                    best_board = return_board
            return best_board, minEval

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

if __name__ == "__main__":

    realtimeboard = chess.Board()

    white = BasicEvalPlayer(realtimeboard, chess.WHITE)
    black = MiniMaxPlayer(realtimeboard, chess.BLACK)

    blk_total_score = 0
    wht_total_score = 0
    num_games = 20

    start = datetime.now()
    for game in range(num_games):
        realtimeboard.reset()
        while not realtimeboard.is_game_over():
            print(len(realtimeboard.move_stack))
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
