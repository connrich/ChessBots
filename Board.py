from PyQt5 import QtWidgets, QtGui, QtCore
import math
import chess
from Bots import MiniMaxPlayer, RandomPlayer

# TODO
#   Save PGN
#   Load board state from fen
#   Human player class
#       - Show available moves for highlighted piece
#   Player selection for white and black
#       - Iterate through 'ChessBots' folder to get bot names
#       - Each bot is invoked by the 'Player' class

class Board(QtWidgets.QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.setFixedSize(QtCore.QSize(480, 480))

        self.files = 'abcdefgh'

        self.loadPiecePixmaps()
        self.pieces = []
        self.selected_piece = None
        self.moves = []
        self.shown_moves = []
        self.prevMoves = []
        self.initBoard()

        self.Referee = Referee()
        self.game_over = False

    def initBoard(self):
        self.board_layout = QtWidgets.QGridLayout()
        self.board_layout.setHorizontalSpacing(0)
        self.board_layout.setVerticalSpacing(0)
        white_square = True
        for i in range(8):
            for j in range(8):
                square = self.Square()
                square.square = i*8 + j
                square.setFixedSize(QtCore.QSize(60, 60))
                if white_square:
                    square.setStyleSheet("background-color: rgb(240, 240, 230);")
                else:
                    square.setStyleSheet("background-color: rgb(118, 150, 86);")
                white_square = not white_square
                self.board_layout.addWidget(square, i, j)
            white_square = not white_square
        self.setLayout(self.board_layout)

        self.boardFromFEN(chess.STARTING_BOARD_FEN)


    def boardFromFEN(self, fen):
        for piece in self.pieces:
            self.board_layout.removeWidget(piece)
            piece.close()
        self.pieces.clear()
        ranks = fen.split('/')
        ranks[-1] = ranks[-1].split(' ')[0]
        for rank_index, rank in enumerate(ranks):
            file_index = 0
            for char in rank:
                if char.isalpha():
                    piece = self.Piece()

                    piece.square = chess.square(file_index, rank_index)
                    self.pieces.append(piece)
                    piece.setPixmap(self.getPiecePixmap(char))
                    piece.setAlignment(QtCore.Qt.AlignCenter)
                    self.board_layout.addWidget(piece, rank_index, file_index)
                    file_index += 1
                elif char.isdigit():
                    file_index += int(char)

    def getPiecePixmap(self, piece):
        try:
            pixmap = self.pixmapDict[piece]
        except:
            pixmap = QtGui.QPixmap()
            pixmap.fill(QtGui.QColor(QtCore.Qt.transparent))
        return pixmap

    def loadPiecePixmaps(self):
        self.pixmapDict = {}
        self.pixmapDict['b'] = QtGui.QPixmap('Piece Images/blk_bishop.png')
        self.pixmapDict['B'] = QtGui.QPixmap('Piece Images/wht_bishop.png')
        self.pixmapDict['k'] = QtGui.QPixmap('Piece Images/blk_king.png')
        self.pixmapDict['K'] = QtGui.QPixmap('Piece Images/wht_king.png')
        self.pixmapDict['n'] = QtGui.QPixmap('Piece Images/blk_knight.png')
        self.pixmapDict['N'] = QtGui.QPixmap('Piece Images/wht_knight.png')
        self.pixmapDict['p'] = QtGui.QPixmap('Piece Images/blk_pawn.png')
        self.pixmapDict['P'] = QtGui.QPixmap('Piece Images/wht_pawn.png')
        self.pixmapDict['q'] = QtGui.QPixmap('Piece Images/blk_queen.png')
        self.pixmapDict['Q'] = QtGui.QPixmap('Piece Images/wht_queen.png')
        self.pixmapDict['r'] = QtGui.QPixmap('Piece Images/blk_rook.png')
        self.pixmapDict['R'] = QtGui.QPixmap('Piece Images/wht_rook.png')

    def nextTurn(self):
        if not self.game_over:
            if self.prevMoves:
                self.oldBoard.push(self.prevMoves.pop())
                board = self.oldBoard
            else:
                board = self.Referee.takeTurn()
                if board.is_game_over():
                    self.game_over = True
            self.boardFromFEN(board.fen())

    def previousMove(self):
        self.oldBoard = self.Referee.realtimeboard
        if self.oldBoard.ply() != 0:
            self.prevMoves.append(self.oldBoard.pop())
            self.boardFromFEN(self.oldBoard.fen())

    def show_legal_moves(self, rank, file):
        for square in self.shown_moves:
            square.setStyleSheet(square.styleSheet() + 'border: 0px;')
        self.shown_moves = []
        # rank = str(8 - rank)
        # file = self.files[file]
        shown_moves = []
        for move in self.Referee.realtimeboard.legal_moves:
            move_str = move.uci()
            if move_str[0] == self.files[file]:
                if move_str[1] == str(8 - rank):
                    square = self.map_to_layout(move_str[2] + move_str[3])
                    square.setStyleSheet(square.styleSheet() + 'border: 3px solid #0000ff;')
                    self.shown_moves.append(square)
                    print(move)

    def map_to_layout(self, square):
        column = 0
        for file in self.files:
            if square[0] == file:
                break
            else:
                column += 1
        row = 8 - int(square[1])
        layout_square = self.board_layout.itemAtPosition(row, column).widget()
        return layout_square

    class Piece(QtWidgets.QLabel):
        piece_selected = QtCore.pyqtSignal()
        def __init__(self):
            super(Board.Piece, self).__init__()
            self.square = 0

        def clearSelection(self):
            self.setStyleSheet('border: 0px;')

        def mousePressEvent(self, event):
            # print('piece at: ', self.parent().layout())
            # self.setStyleSheet('background-color: rgb(69,69,69);')
            parent = self.parent()
            # self.piece_selected.emit()
            try:
                parent.selected_piece.clearSelection()
            except:
                pass
            parent.selected_piece = self
            self.setStyleSheet('border: 2px solid #ff0000;')
            print(math.floor(self.square/8), self.square%8)
            parent.show_legal_moves(math.floor(self.square/8), self.square%8)

    class Square(QtWidgets.QFrame):
        def __init__(self):
            super(Board.Square, self).__init__()
            self.square = 0

        def mousePressEvent(self, event):
            parent = self.parent()
            parent.selected_piece.clearSelection()
            print(math.floor(self.square/8), self.square%8)

class Referee(object):
    def __init__(self):
        self.realtimeboard = chess.Board()
        self.white = MiniMaxPlayer(self.realtimeboard, chess.WHITE, depth=3)
        self.black = RandomPlayer(self.realtimeboard, chess.BLACK)

    def takeTurn(self):
        if self.realtimeboard.turn == chess.WHITE:
            move = self.white.getMove(self.realtimeboard)
            print('white move: ', move)
        elif self.realtimeboard.turn == chess.BLACK:
            move = self.black.getMove(self.realtimeboard)
            print('black move: ', move)
        else:
            print('error in Referee.takeTurn')

        if move in self.realtimeboard.legal_moves:
            self.realtimeboard.push(move)
            return self.realtimeboard
        else:
            print('Illegal Move:')
            print(self.realtimeboard)
            print(move)
            print(self.realtimeboard.legal_moves)
            return