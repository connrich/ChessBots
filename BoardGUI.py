from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import chess
from ChessTest import RandomPlayer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.board = Board()
        self.board.boardFromFEN(chess.STARTING_BOARD_FEN)
        self.setCentralWidget(self.board)
        self.setFixedSize(QtCore.QSize(500, 480))
        self.show()

class Board(QtWidgets.QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.board_layout = QtWidgets.QGridLayout()
        self.board_layout.setHorizontalSpacing(0)
        self.board_layout.setVerticalSpacing(0)

        self.loadPiecePixmaps()

        white_square = True
        for i in range(8):
            for j in range(8):
                square = QtWidgets.QFrame()
                square.setFixedSize(QtCore.QSize(60, 60))
                if white_square:
                    square.setStyleSheet("background-color: rgb(240, 240, 230);")
                else:
                    square.setStyleSheet("background-color: rgb(118, 150, 86);")
                white_square = not white_square
                self.board_layout.addWidget(square, i, j)
            white_square = not white_square
        self.setLayout(self.board_layout)

    def playGame(self):
        self.Referee = Referee()
        for i in range(4):
            board = self.Referee.takeTurn()
            print(board)


    def boardFromFEN(self, fen):
        # TODO construct visual board from fen
        ranks = fen.split('/')
        for rank_index, rank in enumerate(ranks):
            file_index = 0
            for char in rank:
                if char.isalpha():
                    piece = QtWidgets.QLabel()
                    piece.setPixmap(self.getPiecePixmap(char))
                    self.board_layout.addWidget(piece, rank_index, file_index)
                    file_index += 1
                elif char.isdigit():
                    file_index += int(char)

    def getPiecePixmap(self, piece):
        try:
            pixmap = self.pixmapDict[piece]  # = self.blk_bishop
        except:
            pixmap = QtGui.QPixmap()
            pixmap.fill(QtGui.QColor(QtCore.Qt.transparent))
        return pixmap

    def loadPiecePixmaps(self):
        self.pixmapDict = {}
        self.pixmapDict['b'] = QtGui.QPixmap('Piece Images/blk_bishop.png')
        self.pixmapDict['B'] = QtGui.QPixmap('Piece Images/wht_bishop.png')
        self.pixmapDict['k'] = QtGui.QPixmap('Piece Images/blk_king.png')
        self.pixmapDict['K']  = QtGui.QPixmap('Piece Images/wht_king.png')
        self.pixmapDict['n']  = QtGui.QPixmap('Piece Images/blk_knight.png')
        self.pixmapDict['N']  = QtGui.QPixmap('Piece Images/wht_knight.png')
        self.pixmapDict['p']  = QtGui.QPixmap('Piece Images/blk_pawn.png')
        self.pixmapDict['P'] = QtGui.QPixmap('Piece Images/wht_pawn.png')
        self.pixmapDict['q']  = QtGui.QPixmap('Piece Images/blk_queen.png')
        self.pixmapDict['Q']  = QtGui.QPixmap('Piece Images/wht_queen.png')
        self.pixmapDict['r']  = QtGui.QPixmap('Piece Images/blk_rook.png')
        self.pixmapDict['R'] = QtGui.QPixmap('Piece Images/wht_rook.png')

class Referee(object):
    # TODO create 2 player instances and check legal rules
    def __init__(self):
        self.realtimeboard = chess.Board()
        self.white = RandomPlayer(self.realtimeboard, chess.WHITE)
        self.black = RandomPlayer(self.realtimeboard, chess.BLACK)

    def takeTurn(self):
        print(self.realtimeboard.turn)
        if self.realtimeboard.turn == chess.WHITE:
            move = self.white.getMove(self.realtimeboard)
        elif self.realtimeboard.turn == chess.BLACK:
            move = self.black.getMove(self.realtimeboard)
        else:
            print('error in takeTurn')

        if move in self.realtimeboard.legal_moves:
            self.realtimeboard.push(move)
            print(move)
            print(self.realtimeboard)
            return self.realtimeboard
        else:
            print('Illegal Move:')
            print(self.realtimeboard)
            print(move)
            print(self.realtimeboard.legal_moves)
            return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()

    MainWindow.board.playGame()

    sys.exit(app.exec_())