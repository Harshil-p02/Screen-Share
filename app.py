import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QApplication, QPushButton, QLineEdit, QLabel

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

    WIDTH, HEIGHT = 1080, 720                                       # change size

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Python Screen Share")
        self.center()

        uname_label = QLabel("Username:", parent=self)
        uname_label.move(int(self.WIDTH/2)-200, 100)
        self.uname_input = QLineEdit(parent=self)
        self.uname_input.move(int(self.WIDTH/2)-100, 100)

        ip_label = QLabel("Server IP:", parent=self)
        ip_label.move(int(self.WIDTH/2)-200, 150)
        port_label = QLabel("Server Port:", parent=self)
        port_label.move(int(self.WIDTH/2)-200, 200)
        self.ip_input = QLineEdit(parent=self)
        self.ip_input.move(int(self.WIDTH/2)-100, 150)
        self.port_input = QLineEdit(parent=self)
        self.port_input.move(int(self.WIDTH/2)-100, 200)

        self.join_server_btn = self.add_btn(x=int(self.WIDTH/2)-300, y=250, label='Join an existing Server')
        self.create_server_btn = self.add_btn(x=int(self.WIDTH/2)+100, y=250, label='Create a new Server')
        # join_server_btn.clicked.connect(self.join_server_menu)      # change screen
        # create_server_btn.clicked.connect(self.create_server_menu)  # change screen

        # self.show()

    def center(self):
        win = self.frameGeometry()
        center_pt = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pt)

    def add_btn(self, x, y, label):
        btn = QPushButton(text=label, parent=self)
        btn.move(x, y)
        # btn.show()
        return btn

    # def join_server_menu(self):
    #     print("Joined!")

    # def create_server_menu(self):
    #     print("Created!")

class JoinServerMenu(QWidget):

    WIDTH, HEIGHT = 1080, 720

    def __init__(self, ip, port, username, parent=None):
        super(JoinServerMenu, self).__init__(parent)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Python Screen Share")
        self.center()

        # Call join_server
        # Display additional info.. num of members, etc..
        self.client = self.join_server(ip, port, username)



        self.share_btn = QPushButton(text="Share screen", parent=self)
        self.receive_btn = QPushButton(text="Receive screen", parent=self)
        self.share_btn.move(int(self.WIDTH/2)-300, 200)
        self.receive_btn.move(int(self.WIDTH/2)+100, 200)
        self.share_btn.clicked.connect(self.share_screen)
        self.receive_btn.clicked.connect(self.receive_screen)
        self.back = QPushButton(text="Back", parent=self)
        self.back.move(10, 10)

    def center(self):
        win = self.frameGeometry()
        center_pt = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pt)

    def join_server(self, server_ip, port, username):

        client = Client(server_ip, port, username)    # Fetch username from gui
        print(client)
        return client
        # change the screen

    def share_screen(self):
        self.client.share_screen()

    def receive_screen(self):
        self.client.receive_screen()


class CreateServerMenu(QWidget):

    WIDTH, HEIGHT = 1080, 720

    def __init__(self, ip, port, username, parent=None):
        super(CreateServerMenu, self).__init__(parent)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Python Screen Share")
        self.center()

        # Add options
        # Share, invite friends
        self.server = self.create_server(ip, port, username)

        # server_label = QLabel("Enter server IP:", parent=self)
        # server_label.move(int(self.WIDTH / 2) - 227, 100)
        # server_input = QLineEdit(parent=self)
        # server_input.move(int(self.WIDTH / 2) - 100, 100)
        self.back = QPushButton(text="Back", parent=self)
        self.back.move(10, 10)

    def center(self):
        win = self.frameGeometry()
        center_pt = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pt)

    def create_server(self, server_ip, port, username):
        server = Server(server_ip, port, username)
        print(server_ip, port)
        print(server)
        return server
        # change screen

class WindowHandler(QMainWindow):

    WIDTH, HEIGHT = 1080, 720

    def __init__(self, parent=None):
        super(WindowHandler, self).__init__(parent)
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Python Screen Share")

        self.start_window()

    def start_window(self):
        self.window = Window(self)
        self.setCentralWidget(self.window)
        self.window.join_server_btn.clicked.connect(self.start_join_screen)
        self.window.create_server_btn.clicked.connect(self.start_create_screen)
        self.show()

    def start_join_screen(self):
        print("Joined!")
        self.username = self.window.uname_input.text()
        self.ip = self.window.ip_input.text()
        self.port = self.window.port_input.text()
        print(self.username)
        self.join_menu = JoinServerMenu(self.ip, self.port, self.username, parent=self)
        self.setCentralWidget(self.join_menu)
        self.join_menu.back.clicked.connect(self.start_window)
        self.show()

    def start_create_screen(self):
        print("Created!")
        self.username = self.window.uname_input.text()
        self.ip = self.window.ip_input.text()
        self.port = self.window.port_input.text()
        print(self.username)
        self.create_menu = CreateServerMenu(self.ip, self.port, self.username, parent=self)
        self.setCentralWidget(self.create_menu)
        self.create_menu.back.clicked.connect(self.start_window)
        self.show()



def main():
    app = QApplication(sys.argv)
    w = WindowHandler()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()