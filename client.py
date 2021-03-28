import socket
import numpy as np
import cv2
import mss


class Client:

    def __init__(self, server, port, username):
        '''
        creates client-side socket

        :param server: IP of server (Join server)
        :param port: Port of server
        '''
        self.SERVER = server
        self.PORT = int(port)
        self.FORMAT = 'utf-8'
        self.HEADER = 64
        self.username = username

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("here1")
        self.client.connect((self.SERVER, self.PORT))
        print("here2")

        self.send_msg(username)

        num_users = self.recv_msg()
        print(num_users)

    def send_msg(self, msg):
        msg_len = len(msg)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len += b' ' * (self.HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(msg.encode(self.FORMAT))

    def recv_msg(self):
        msg_len = self.client.recv(self.HEADER).decode(self.FORMAT)
        msg = self.client.recv(int(msg_len)).decode(self.FORMAT)
        return msg

    def share_screen(self):
        # Send participant's name first
        self.send_msg(self.username)

        n = 1

        with mss.mss() as sct:
            sct.compression_level = 9
            monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

            while True:
                img = sct.grab(monitor)
                img_arr = np.array(img)

                resized = cv2.resize(img_arr, (0,0), fx=0.5, fy=0.5)
                img_arr = np.array(resized)

                img_bytes = cv2.imencode('.png', img_arr)[1].tobytes()
                self.client.send(img_bytes)
                print(f"Sent image {n}")
                n += 1

    def get_image(self):
        img_bytes = self.client.recv(8000000)
        img_arr = np.frombuffer(img_bytes, np.uint8)

        return cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

    def receive_screen(self):
        # get name of the screen showing participant
        name = self.recv_msg()                                      # Truncate the name... 10 chars?
        cv2.namedWindow(f"Viewing {name[:10]}'s screen - Screen Share")

        while True:
            img = self.get_image()
            cv2.imshow(f"Viewing {name[:10]}'s screen", img)
            cv2.waitKey(delay=10)
