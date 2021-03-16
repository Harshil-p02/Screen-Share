import socket
import numpy as np
import cv2
import mss


# function for: receiving data, sending data

class Server:

    def __init__(self, server, port):
        self.SERVER = server
        self.PORT = port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.SERVER, self.PORT))

        # Add upto 5 clients
        # Will need to store client info as [(conn, addr), ...]

        s.listen()                  # maybe new func for accepting connections?
        conn, addr = s.accept()
        print("connected with", addr)

    def handle_clients(self):
        pass