import chess

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
                eval = evals[0] - evals[1]
                if child_board.is_checkmate():
                    move = legal_move
                    break
                elif eval > 0:
                    move = legal_move
            elif self.colour == chess.BLACK:
                eval = evals[0] - evals[1]
                if child_board.is_checkmate():
                    move = legal_move
                    break
                elif eval > 0:
                    move = legal_move

        if move == None:
            move = self.legal_moves[0]
        return move