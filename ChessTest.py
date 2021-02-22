import chess
from datetime import datetime
from BasicEvalPlayer import BasicEvalPlayer as BasicEvalPlayer

class MiniMaxPlayer(object):
    def __init__(self, board, colour, depth=2):
        self.current_board = board
        self.colour = colour
        self.depth = depth
        self.legal_moves = []

        self.pieceValues = {'p': 1, 'b': 3, 'n': 3, 'r': 5, 'q': 9, 'k': 3.5}

    def getMove(self, board):
        self.current_board = board
        self.current_eval = self.evaluateBoardState(self.current_board)
        if self.colour == chess.WHITE:
            eval_diff = self.current_eval[0] - self.current_eval[1]
            opponent_eval = self.current_eval[1]
        elif self.colour == chess.BLACK:
            eval_diff = self.current_eval[1] - self.current_eval[0]
            opponent_eval = self.current_eval[0]

        if  opponent_eval < 12:
            depth = 4
        else:
            depth = 3
        chosen_board, eval = self.miniMax(self.current_board, True, depth=depth)
        print(depth)
        return chosen_board.pop()

    def miniMax(self, board, maxPlayer, depth=2):
        if board.is_game_over():
            result = board.result().split('-')

            if self.colour == chess.WHITE and result[0] == '1':
                return board, 999999
            elif self.colour == chess.BLACK and result[1] == '1':
                return board, 999999
            if self.colour == chess.WHITE and result[1] == '1':
                return board, -999999
            elif self.colour == chess.BLACK and result[0] == '1':
                return board, -999999
            else:
                return board, -100.0
        elif depth == 0:
            evals = self.evaluateBoardState(board)
            if self.colour == chess.WHITE:
                eval = evals[0] - evals[1]
            elif self.colour == chess.BLACK:
                eval = evals[1] - evals[0]
            return board, eval

        if maxPlayer:
            maxEval = float('-inf')
            for legalmove in board.legal_moves:
                child_board = board.__copy__()
                child_board.push(legalmove)

                # eval = self.evaluateBoardState(child_board)
                # print(eval)

                return_board, eval = self.miniMax(child_board, not maxPlayer, depth=depth-1)

                if self.colour == chess.WHITE:
                    if child_board.is_check():
                        eval += 0.55
                elif self.colour == chess.BLACK:
                    if child_board.is_check():
                        eval += 0.55
                else:
                    print('max player eval error')
                    eval = 0

                if eval > maxEval:
                    maxEval = eval
                    best_board = child_board
            return best_board, maxEval

        elif not maxPlayer:
            minEval = float('inf')
            for legalmove in board.legal_moves:
                # print(legalmove)
                # print(legalmove in board.legal_moves)
                child_board = board.__copy__()
                child_board.push(legalmove)
                # eval = self.evaluateBoardState(child_board)

                return_board, eval = self.miniMax(child_board, not maxPlayer, depth=depth-1)
                if self.colour != chess.WHITE:
                    pass
                elif self.colour != chess.BLACK:
                    pass
                else:
                    print('min player eval error')
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

    white = MiniMaxPlayer(realtimeboard, chess.WHITE)
    black = BasicEvalPlayer(realtimeboard, chess.BLACK)

    blk_total_score = 0
    wht_total_score = 0
    num_games = 1

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
