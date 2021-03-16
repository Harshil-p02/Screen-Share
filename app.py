import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QPushButton, QLineEdit, QLabel

from server import Server
from client import Client


# will probably need a User class to differentiate b/w users

# Menu:  HOW??
#   - Enter Username
#   - Join a server
#       ~ Server IP
#           = Share screen
#           = Receive screen
#   - Create a server
#       ~ Server IP
#       new window with created server having share and receive options
#       ~ Invite friends???


class Window(QWidget):

    WIDTH, HEIGHT = 1080, 720

    def __init__(self):
        super(Window, self).__init__()
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Python Screen Share")
        self.center()

        uname_label = QLabel("Username:", parent=self)
        uname_label.move(int(self.WIDTH/2)-200, 100)
        uname_input = QLineEdit(parent=self)
        uname_input.move(int(self.WIDTH/2)-100, 100)
        join_server_btn = self.add_btn(x=int(self.WIDTH/2)-300, y=200, label='Join an existing Server')
        create_server_btn = self.add_btn(x=int(self.WIDTH/2)+100, y=200, label='Create a new Server')
        join_server_btn.clicked.connect(self.join_server_menu)      # change screen
        create_server_btn.clicked.connect(self.create_server_menu)  # change screen

        self.show()

    def center(self):
        win = self.frameGeometry()
        center_pt = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pt)

    def add_btn(self, x, y, label):
        btn = QPushButton(text=label, parent=self)
        btn.move(x, y)
        btn.show()
        return btn

    def join_server_menu(self):
        print("Joined!")

    def create_server_menu(self):
        print("Created!")

    def join_server(self, server_ip, port):
        self.client = Client(server_ip, port)
        # change the screen

    def share_screen(self):
        self.client.share_screen()

    def receive_screen(self):
        self.client.receive_screen()

    def create_server(self, server_ip, port):
        server = Server(server_ip, port)
        # change screen


def main():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()