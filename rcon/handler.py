import socket

import frostbite
from commandextension import CommandExtension
import exceptions

class ConnectionHandler(CommandExtension):

    def __init__(self, ip, port, game):
        self.ip = ip
        self.port = port
        self.game = game

        self.protocol = frostbite.Frostbite()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        super(ConnectionHandler, self).__init__()

    def connect(self):
        try:
            self.socket.settimeout(1)
            self.socket.connect((self.server_ip, self.server_port))
            self.socket.setblocking(1)
            self.socket.settimeout(None)
        except socket.timeout:
            raise exceptions.ServerTimeout()

        return self

    def disconnect(self):
        self.socket.close()
        return self

    def process_event(self):
        return self.protocol.recive_packet(self.socket)
