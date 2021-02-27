from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import chess
from Bots import BasicEvalPlayer, MiniMaxPlayer
from datetime import datetime
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.board = Board()
        self.board.boardFromFEN(chess.STARTING_BOARD_FEN)
        self.setCentralWidget(self.board)
        # self.setFixedSize(QtCore.QSize(500, 480))

        self.turnThread = turnThread(self.playGame)

        self.move_timer = QtCore.QTimer()
        self.move_timer.setInterval(200)
        self.move_timer.timeout.connect(self.takeTurn)

        self.DockWidget = QtWidgets.QDockWidget()
        self.dock_widget = QtWidgets.QWidget()

        self.play_button = QtWidgets.QPushButton()
        self.play_button.setIcon(QtGui.QIcon('Assets/play_icon.png'))
        self.dock_layout = QtWidgets.QVBoxLayout()
        self.dock_layout.addWidget(self.play_button)
        self.dock_widget.setLayout(self.dock_layout)
        self.DockWidget.setWidget(self.dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.DockWidget)
        self.play_button.clicked.connect(self.play_pause)

        self.direction_layout = QtWidgets.QHBoxLayout()
        self.back = QPushButton()
        self.back.setIcon(QIcon('Assets/back_arrow'))
        self.direction_layout.addWidget(self.back)
        self.forward = QPushButton()
        self.forward.setIcon(QIcon('Assets/forward_arrow'))
        self.direction_layout.addWidget(self.forward)

        self.direction_widget = QWidget()
        self.direction_widget.setLayout(self.direction_layout)
        self.dock_layout.addWidget(self.direction_widget)

        self.show()
        self.playGame()

    def play_pause(self):
        if self.move_timer.isActive():
            self.move_timer.stop()
            self.play_button.setIcon(QtGui.QIcon('Assets/play_icon.png'))
        else:
            self.move_timer.start()
            self.play_button.setIcon(QtGui.QIcon('Assets/pause_icon.png'))
        pass

    def playGame(self):
        self.board.boardFromFEN(chess.STARTING_BOARD_FEN)
        self.Referee = Referee()
        # self.move_timer.start()

    def takeTurn(self):
        board = self.Referee.takeTurn()
        self.board.boardFromFEN(board.fen())
        if board.is_game_over():
            print(board.result())
            self.move_timer.stop()



class Board(QtWidgets.QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.setFixedSize(QtCore.QSize(480, 480))

        self.board_layout = QtWidgets.QGridLayout()
        self.board_layout.setHorizontalSpacing(0)
        self.board_layout.setVerticalSpacing(0)

        self.pieces = []

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
                    piece = QtWidgets.QLabel()
                    self.pieces.append(piece)
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
        self.pixmapDict['K'] = QtGui.QPixmap('Piece Images/wht_king.png')
        self.pixmapDict['n'] = QtGui.QPixmap('Piece Images/blk_knight.png')
        self.pixmapDict['N'] = QtGui.QPixmap('Piece Images/wht_knight.png')
        self.pixmapDict['p'] = QtGui.QPixmap('Piece Images/blk_pawn.png')
        self.pixmapDict['P'] = QtGui.QPixmap('Piece Images/wht_pawn.png')
        self.pixmapDict['q'] = QtGui.QPixmap('Piece Images/blk_queen.png')
        self.pixmapDict['Q'] = QtGui.QPixmap('Piece Images/wht_queen.png')
        self.pixmapDict['r'] = QtGui.QPixmap('Piece Images/blk_rook.png')
        self.pixmapDict['R'] = QtGui.QPixmap('Piece Images/wht_rook.png')

class Referee(object):
    # TODO create 2 player instances and check legal rules
    def __init__(self):
        self.realtimeboard = chess.Board()
        self.white = BasicEvalPlayer(self.realtimeboard, chess.WHITE)
        self.black = MiniMaxPlayer(self.realtimeboard, chess.BLACK)

    def takeTurn(self):
        if self.realtimeboard.turn == chess.WHITE:
            move = self.white.getMove(self.realtimeboard)
            print('white move: ', move)
        elif self.realtimeboard.turn == chess.BLACK:
            move = self.black.getMove(self.realtimeboard)
            print('black move: ', move)
        else:
            print('error in takeTurn')

        if move in self.realtimeboard.legal_moves:
            self.realtimeboard.push(move)
            # print(move)
            # print(self.realtimeboard)
            return self.realtimeboard
        else:
            print('Illegal Move:')
            print(self.realtimeboard)
            print(move)
            print(self.realtimeboard.legal_moves)
            return

class turnThread(QtCore.QThread):

    def __init__(self, turn_method):
        QtCore.QThread.__init__(self)
        self.turn_method = turn_method

    def run(self):
        self.turn_method()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()

    games = 1
    for game in range(games):
        print('play game ', game)
        MainWindow.playGame()

    sys.exit(app.exec_())