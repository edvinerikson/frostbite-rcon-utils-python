frostbite-rcon-utils
====================

lightweight library for connecting to an frostbite based game (bf3, bf4, bfh, mohw, bc2)

## Example


`````python

from rcon import exceptions
from rcon import ConnectionHandler

server = ConnectionHandler('127.0.0.1', 47200, 'bf4')

try:
    info = server.connect().login('password').server_info().active_players().data()
except exceptions.ServerTimeout, e:
    print('Unable to connect to server')
except exceptions.InvalidPassword, e:
    print('Invalid password!')
else:
    print('We got all info, disconnect')
    server.disconnect()
    print(info['server_info'], info['active_players'])

`````


##Example #2
`````python

from rcon import exceptions
from rcon import ConnectionHandler

password = 'hej123'
def main(server):
    server.login(password).enable_events()
    while True:
        try:
            event = server.process_event()
        except (exceptions.ServerTimeout, exceptions.NoDataReceived), e:
            print('Server timeout or no data recevied, in event loop excepetion')
            server.reconnect().login(password).enable_events()
            print('Reconnected!')
        else:
            print(event)

if __name__ == "__main__":
    server = ConnectionHandler('127.0.0.1', 47200, 'bf4')
    try:
        server.connect()
    except exceptions.ServerTimeout, e:
        print('Server timeout.')
        server.reconnect()
        print('Reconnected')
        main(server)

    except exceptions.InvalidPassword, e:
        print('Wrong password')
    else:
        print('Seems to work here!')
        main(server)

`````