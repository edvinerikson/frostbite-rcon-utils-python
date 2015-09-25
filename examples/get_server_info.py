import socket

from frostbite_rcon_utils import create_packet, encode_packet, decode_packet, contains_complete_packet


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.settimeout(1)
connection.connect(('188.126.64.4', 47215))
connection.setblocking(1)

packet_to_send = encode_packet(create_packet(0, False, False, ['serverInfo']))
connection.send(packet_to_send)
data_buffer = ""
while not contains_complete_packet(data_buffer):
    data_buffer += connection.recv(2048)

packet = decode_packet(data_buffer)
print(packet)