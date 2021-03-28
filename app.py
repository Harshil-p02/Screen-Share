import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget, QApplication, QPushButton, QLineEdit, QLabel

from server import Server
from client import Client

# will probably need a User class to differentiate b/w users            (just save the users as dict in server)
# Make menus responsive to size changes; fixed size menu?

# Menu:
#   - Enter Username; ip, port
#   - Join a server
#           = Share screen
#           = Receive screen
#   - Create a server
#           Invite friends???
#           display info.. who joined; their ip..
#           new window with created server having share and receive options

# CAN WE REMOVE PARENT FROM INIT??      Nooo; it helps :)
class Window(QWidget):

    def __init__(self, parent):
        '''
        Home screen of the gui app
        Gets the username, IP and port number to either join or create a server
        :param parent: sets the parent of the current instance
        '''
        super(Window, self).__init__(parent)

        self.WIDTH, self.HEIGHT = parent.WIDTH, parent.HEIGHT                   # change these values to change the size of a single menu
        parent.resize(self.WIDTH, self.HEIGHT)
        parent.setWindowTitle("Screen Share")

        uname_label = QLabel("Username:", parent=self)
        uname_label.move(int(self.WIDTH/2)-200, 100)
        self.uname_input = QLineEdit(parent=self)
        self.uname_input.move(int(self.WIDTH/2)-100, 100)

        ip_label = QLabel("Server IP:", parent=self)
        ip_label.move(int(self.WIDTH/2)-200, 150)
        self.ip_input = QLineEdit(parent=self)
        self.ip_input.move(int(self.WIDTH/2)-100, 150)

        port_label = QLabel("Server Port:", parent=self)
        port_label.move(int(self.WIDTH/2)-200, 200)
        self.port_input = QLineEdit(parent=self)
        self.port_input.move(int(self.WIDTH/2)-100, 200)

        self.join_server_btn = parent.add_btn(x=int(self.WIDTH/2)-300, y=250, label='Join an existing Server', parent=self)
        self.create_server_btn = parent.add_btn(x=int(self.WIDTH/2)+100, y=250, label='Create a new Server', parent=self)
    #     Button presses handled in calling function (WindowHandler)


class JoinServerMenu(QWidget):

    def __init__(self, ip, port, username, parent):
        super(JoinServerMenu, self).__init__(parent)

        self.WIDTH, self.HEIGHT = parent.WIDTH, parent.HEIGHT
        parent.resize(self.WIDTH, self.HEIGHT)
        parent.setWindowTitle("Join server - Screen Share")

        # Display additional info.. num of members, etc..
        self.client = self.join_server(ip, port, username)

        self.share_btn = parent.add_btn(x=int(self.WIDTH/2)-300, y=200, label="Share screen", parent=self)
        self.receive_btn = parent.add_btn(x=int(self.WIDTH/2)+100, y=200, label="Receive screen", parent=self)
        self.back = parent.add_btn(x=10, y=10, label="Back", parent=self)

        self.share_btn.clicked.connect(self.share_screen)
        self.receive_btn.clicked.connect(self.receive_screen)

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

    def __init__(self, ip, port, username, parent=None):
        super(CreateServerMenu, self).__init__(parent)

        self.WIDTH, self.HEIGHT = parent.WIDTH, parent.HEIGHT
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Create Server - Screen Share")

        # Add options
        # Share, invite friends
        self.back = parent.add_btn(x=10, y=10, label="Back", parent=self)
        # time.sleep(2)
        self.server = self.create_server(ip, port, username)
        print(self.server)

    def create_server(self, server_ip, port, username):
        return Server(server_ip, port, username)
        # change screen


class WindowHandler(QMainWindow):

    WIDTH, HEIGHT = 1080, 720

    def __init__(self):
        super(WindowHandler, self).__init__()
        self.resize(self.WIDTH, self.HEIGHT)
        self.center()
        # Window title is set by the individual window classes

        self.start_window()

    def start_window(self):
        self.window = Window(self)
        self.setCentralWidget(self.window)
        self.window.join_server_btn.clicked.connect(self.start_join_screen)
        self.window.create_server_btn.clicked.connect(self.start_create_screen)
        self.show()

    def start_join_screen(self):
        self.username = self.window.uname_input.text()
        self.ip = self.window.ip_input.text()
        self.port = self.window.port_input.text()
        print(self.username)

        self.join_menu = JoinServerMenu(self.ip, self.port, self.username, parent=self)
        self.setCentralWidget(self.join_menu)
        self.join_menu.back.clicked.connect(self.start_window)
        self.show()

    def start_create_screen(self):
        self.username = self.window.uname_input.text()
        self.ip = self.window.ip_input.text()
        self.port = self.window.port_input.text()
        print(self.username)

        self.create_menu = CreateServerMenu(self.ip, self.port, self.username, parent=self)
        self.setCentralWidget(self.create_menu)
        self.create_menu.back.clicked.connect(self.start_window)
        self.show()

    def center(self):
        win = self.frameGeometry()
        center_pt = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pt)

    def add_btn(self, x, y, label, parent):
        btn = QPushButton(text=label, parent=parent)
        btn.move(x, y)
        return btn


def main():
    app = QApplication(sys.argv)
    w = WindowHandler()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()