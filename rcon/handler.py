import socket
from time import sleep

import frostbite
import exceptions
from commands import Commands as CommandExtension

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
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1)
            self.socket.connect((self.ip, self.port))
            self.socket.setblocking(1)
            #self.socket.settimeout(5)
        except socket.timeout:
            raise exceptions.ServerTimeout()

        return self

    def disconnect(self):
        self.socket.close()
        return self

    def reconnect(self):
        reconnect = 1
        while True:         
            try:
                self.connect()
            except exceptions.ServerTimeout:
                reconnect *= 2
                print("reconnect failed, retrying after {0} seconds".format(reconnect))
            else:
                print('Successfully reconnected')
                #server.login('H4xxPass').enable_events()
                return self
            sleep(reconnect)

    def process_event(self):
        return self.protocol.receive_event(self.socket)
