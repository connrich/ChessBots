from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import importlib
import math
import chess
from Board import Board
from Bots import RandomPlayer, BasicEvalPlayer, MiniMaxPlayer
from ChessTest import OrderedMiniMax
from datetime import datetime
import time
import ChessBots

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.setFixedSize(QtCore.QSize(500, 480))

        self.initBoard()
        self.initControlDock()
        self.show()

        self.move_timer = QtCore.QTimer()
        self.move_timer.setInterval(200)
        self.move_timer.timeout.connect(self.takeTurn)

    def loadPlayers(self, combobox):
        self.Bots = {}
        # Iterates through ChessBots folder and extracts Player classes
        for filename in os.listdir('ChessBots'):
            if filename.endswith('.py') and filename[0] != '_':
                filename = filename[:-3]
                mymodule = importlib.import_module('ChessBots.' + filename)
                self.Bots[filename] = mymodule.Player
                combobox.addItem(filename)

    def initBoard(self):
        self.board = Board()
        self.setCentralWidget(self.board)

    def initControlDock(self):
        self.DockWidget = QtWidgets.QDockWidget()
        self.DockWidget.setWindowTitle('Game Controls')
        self.DockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock_widget = QtWidgets.QWidget()
        self.DockWidget.setWidget(self.dock_widget)
        self.dock_layout = QtWidgets.QVBoxLayout()
        self.dock_widget.setLayout(self.dock_layout)

        white_label = QLabel('White:')
        white_label.setMaximumHeight(10)
        self.dock_layout.addWidget(white_label)
        self.WhiteComboBox = QComboBox()
        self.loadPlayers(self.WhiteComboBox)
        self.dock_layout.addWidget(self.WhiteComboBox)

        black_label = QLabel('Black:')
        black_label.setMaximumHeight(10)
        self.dock_layout.addWidget(black_label)
        self.BlackComboBox = QComboBox()
        self.loadPlayers(self.BlackComboBox)
        self.dock_layout.addWidget(self.BlackComboBox)

        self.startGameButton = QPushButton('Start Game')
        self.dock_layout.addWidget(self.startGameButton)

        self.play_button = QtWidgets.QPushButton()
        self.play_button.setIcon(QtGui.QIcon('Assets/play_icon.png'))
        self.dock_layout.addWidget(self.play_button)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.DockWidget)
        self.play_button.clicked.connect(self.play_pause)

        self.direction_layout = QtWidgets.QHBoxLayout()
        self.back = QPushButton()
        self.back.setIcon(QIcon('Assets/back_arrow'))
        self.direction_layout.addWidget(self.back)
        self.back.clicked.connect(self.board.previousMove)
        self.forward = QPushButton()
        self.forward.setIcon(QIcon('Assets/forward_arrow'))
        self.direction_layout.addWidget(self.forward)
        self.forward.clicked.connect(self.board.nextTurn)

        self.direction_widget = QWidget()
        self.direction_widget.setLayout(self.direction_layout)
        self.dock_layout.addWidget(self.direction_widget)

    def flipBoard(self):
        pass

    def play_pause(self):
        if self.move_timer.isActive():
            self.move_timer.stop()
            self.play_button.setIcon(QtGui.QIcon('Assets/play_icon.png'))
        else:
            self.move_timer.start()
            self.play_button.setIcon(QtGui.QIcon('Assets/pause_icon.png'))

    def playGame(self):
        self.Referee = Referee()

    def takeTurn(self):
        board = self.Referee.takeTurn()
        self.board.boardFromFEN(board.fen())
        if board.is_game_over():
            print(board.result())
            self.move_timer.stop()


class Referee(object):
    def __init__(self):
        self.realtimeboard = chess.Board()
        self.white = MiniMaxPlayer(self.realtimeboard, chess.WHITE, depth=3)
        self.black = OrderedMiniMax(self.realtimeboard, chess.BLACK)

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