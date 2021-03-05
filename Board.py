from PyQt5 import QtWidgets, QtGui, QtCore
import math
import chess

class Board(QtWidgets.QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.setFixedSize(QtCore.QSize(480, 480))

        self.board_layout = QtWidgets.QGridLayout()
        self.board_layout.setHorizontalSpacing(0)
        self.board_layout.setVerticalSpacing(0)

        self.pieces = []
        self.selected_piece = None
        self.moves = []

        self.loadPiecePixmaps()

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

    def show_moves(self):
        self.selected_piece = self
        print('show_moves')

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
                print('excpet')
                pass
            parent.selected_piece = self
            self.setStyleSheet('border: 2px solid #ff0000;')
            print(math.floor(self.square/8), self.square%8)
            Board.show_moves(self)

    class Square(QtWidgets.QFrame):
        def __init__(self):
            super(Board.Square, self).__init__()
            self.square = 0

        def mousePressEvent(self, event):
            parent = self.parent()
            parent.selected_piece.clearSelection()
            print(math.floor(self.square/8), self.square%8)