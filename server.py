import socket
import threading


# function for: receiving data, sending data
# Ask for username, can be done via gui application

class Server:

    def __init__(self, ip, port, username):
        '''
        creates the server socket; only executed when create server is called

        :param server: IP where server socket resides (Create Server)
        :param port: port where server is to be established
        '''
        self.IP = ip
        self.PORT = int(port)
        self.FORMAT = 'utf-8'
        self.HEADER = 64

        self.users = {}
        self.owner = username

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("here1")
        print(self.IP, self.PORT)
        print(self.soc)
        self.soc.bind((self.IP, self.PORT))
        print(f"server bound to {self.IP} ip and {self.PORT} port")
        while True:
            self.start()
            print(username)

        # Add upto 5 clients; start a thread, maintain user profile (username)
        # Will need to store client info as [(conn, addr), ...]

    def start(self):
        print("here2, listening...")
        self.soc.listen()                       # maybe new func for accepting connections? threading or multiprocessing
        conn, addr = self.soc.accept()
        print("connected with", addr)
        print(conn)

        msg_len = conn.recv(self.HEADER).decode(self.FORMAT)

        # ADD CHECK IN GUI THAT EMPTY USERNAME IS NOT ALLOWED
        username = conn.recv(int(msg_len)).decode(self.FORMAT)
        if username in self.users.keys():
            # send alert for new username
            pass
        self.users[username] = conn
        print(self.users)


        # create a handle_client instance for each user (multiprocessing/ threading??)
        thread = threading.Thread(target=self.handle_clients, args=(conn, addr, username))
        thread.start()

    def handle_clients(self, conn, addr, username):
        # ADD A DISCONNECT SIGNAL ONCE GUI IS CLOSED
        # Send an alert when a client leaves
        self.send_msg(str(len(self.users)), conn)

        while True:
            msg = conn.recv(8000000)
            for user in self.users.keys():
                if user != username:
                    self.users[username].send(msg)

    def send_msg(self, msg, soc):
        msg = msg.encode(self.FORMAT)
        msg_len = str(len(msg)).encode(self.FORMAT)
        msg_len += b' ' * (self.HEADER - len(msg_len))
        soc.send(msg_len)
        soc.send(msg)

