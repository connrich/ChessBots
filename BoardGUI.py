from PyQt5 import QtWidgets, QtGui, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.board = Board()
        self.setCentralWidget(self.board)
        self.setFixedSize(QtCore.QSize(self.width(), self.height()))
        self.show()

class Board(QtWidgets.QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.board_layout = QtWidgets.QGridLayout()

        blk_bishop = QtGui.QPixmap('blk_bishop.png')
        piece = QtWidgets.QLabel()
        piece.setPixmap(blk_bishop)
        piece.setStyleSheet('background-color: rgb(255, 255, 255);')

        white_square = True
        for i in range(8):
            for j in range(8):
                blk_bishop = QtGui.QPixmap('blk_bishop.png')
                piece = QtWidgets.QLabel()
                piece.setPixmap(blk_bishop)

                square = QtWidgets.QFrame()
                if white_square:
                    square.setStyleSheet("background-color: rgb(255, 255, 255);")
                else:
                    square.setStyleSheet("background-color: rgb(47, 47, 47);")
                white_square = not white_square
                #piece.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored))
                self.board_layout.addWidget(square, i, j)
                self.board_layout.addWidget(piece, i, j)

            white_square = not white_square

        self.setLayout(self.board_layout)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        # QtGui.QResizeEvent(self)
        # super(MainWindow, self).resizeEvent()
        if self.width() < self.height():
            self.setGeometry(QtCore.QRect(0, 0, self.width(), self.width()))
        elif self.height() > self.width():
            self.setGeometry(QtCore.QRect(0, 0, self.height(), self.height()))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()

    sys.exit(app.exec_())