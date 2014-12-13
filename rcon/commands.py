from exceptions import *
from decorators import ChainResponse

class Commands(object):

    def __init__(self):
        self.response = ResponseProxy(self)
        super(Commands, self).__init__()

    def command(self, command, args=[]):
        if not type(args) == list:
            raise TypeError('args must be of type list')

        data = [command] + args
        return self.protocol.send_command(self.socket, data)

    def login(self, password):
        salt = self.command('login.hashed')[1].decode("hex")

        hashed_password = self.protocol.make_password_hash(salt, password)\
        .encode("hex").upper()

        if not self.command('login.hashed', [hashed_password])[0] == "OK":
            raise InvalidPassword('The supplied password is incorrect')

        return self 

    @ChainResponse
    def server_info(self):
        return self.command('serverInfo')

    @ChainResponse
    def server_name(self):
        return self.command('serverInfo')[1]

    @ChainResponse
    def active_players(self):
        return self.command('serverInfo')[2]

    @ChainResponse
    def max_players(self):
        return self.command('serverInfo')[3]

    @ChainResponse
    def current_level(self):
        return self.command('currentLevel')

    @ChainResponse
    def list_players(self, player_subset):
        return self.command('listPlayers', [player_subset])

    @ChainResponse
    def admin_list_players(self, player_subset):
        return self.command('admin.listPlayers', [player_subset])

    @ChainResponse
    def enable_events(self, state=True):
        #BC2 support
        command = 'eventsEnabled' if self.game in ['bc2'] else 'admin.eventsEnabled'
        return self.command(command, [state])

    @ChainResponse
    def ping(self):
        return self.command('ping')

class ResponseProxy(object):

    def __init__(self, instance):
        self.__data = {}
        self.instance = instance
        super(ResponseProxy, self).__init__()

    def addResponse(self, key, val):
        self.__data[key] = val

    def data(self):
        return self.__data

    def clear(self):
        self.__data = {}
        return self

    def __getattr__(self, name):
        if hasattr(self.instance, name):
            return getattr(self.instance, name)
        else:
            raise AttributeError('{0} does not have attribute {1}'.format(self.instance.__name__, name))