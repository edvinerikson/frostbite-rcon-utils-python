frostbite-rcon-utils
====================

lightweight library for connecting to an frostbite based game (bf3, bf4, bfh, mohw, bc2)

## Example


`````python

from socket import timeout
from rcon import ConnectionHandler, InvalidPassword

server = ConnectionHandler('127.0.0.1', 47200, 'bf4')

try:
    info = server.connect().login('password').server_info().active_players().data()
except timeout, e:
    print('Unable to connect to server')
except InvalidPassword, e:
    print('Invalid password!')
else:
    print('We got all info, disconnect')
    server.disconnect()
    print(info['server_info'], info['active_players'])

`````
