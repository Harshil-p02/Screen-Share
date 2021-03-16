import socket
import numpy as np
import cv2
import mss


class Client:

    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.SERVER, self.PORT))

    # def take_image(self):
    #     pass

    def share_screen(self):
        # Send participant's name first

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
        name = self.client.recv(80000).decode('utf-8')
        cv2.namedWindow(f"Viewing {name}'s screen")

        while True:
            img = self.get_image()
            cv2.imshow(f"Viewing {name}'s screen", img)
            cv2.waitKey(delay=10)