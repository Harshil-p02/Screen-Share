import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QLineEdit, QLabel

from server import Server
from client import Client


class Window(QWidget):

    HEIGHT, WIDTH = 1080, 720

    def __init__(self):
        super(Window, self).__init__()
        self.resize(self.HEIGHT, self.WIDTH)
        self.center()

        self.show()

    def center(self):
        win = self.frameGeometry()
        center_pt = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pt)


def main():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()