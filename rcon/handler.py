import socket
from time import sleep
import logging
logger = logging.getLogger(__name__)


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

    def reconnect(self, max_seconds=20):
        reconnect = 1
        while True:
            if reconnect >= max_seconds:
                raise exceptions.ServerUnReachable(
                'Server did not respond within the max_seconds interval: {0} seconds'.format(max_seconds)
                )
            try:
                self.connect()
            except exceptions.ServerTimeout:
                reconnect *= 2
                logger.info("reconnect failed, retrying after {0} seconds".format(reconnect))
            else:
                return self
            sleep(reconnect)

    def process_event(self):
        return self.protocol.receive_event(self.socket)
