def ChainResponse(f):
    """
    Use this when you want to be able to chain rcon commands,
    use method name as the key when you want to access the data from .data() method
    example: data = server.server_info().active_players().data()
    info = data['server_info']
    active_players = data['active_players']

    clear the response cache
    data.clear()

    @ChainResponse
    def server_info(self):
        return self.command('serverInfo')
    """
    def wrapper(*args):
        instance = args[0]
        instance.response.addResponse(f.__name__, f(*args))
        return instance.response
    return wrapper