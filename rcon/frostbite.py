from struct import *
import socket
import select
import hashlib

import exceptions

class Frostbite(object):
    client_sequence_nr = 0

    @staticmethod
    def encode_header(is_from_server, is_response, sequence):
        header = sequence & 0x3fffffff
        if is_from_server:
            header += 0x80000000
        if is_response:
            header += 0x40000000
        return pack('<I', header)

    @staticmethod
    def decode_header(data):
        [header] = unpack('<I', data[0 : 4])
        return [header & 0x80000000, header & 0x40000000, header & 0x3fffffff]

    @staticmethod
    def encode_int32(size):
        return pack('<I', size)

    @staticmethod
    def decode_int32(data):
        return unpack('<I', data[0 : 4])[0]
    
    @classmethod
    def encode_words(cls, words):
        size = 0
        encoded_words = ''
        for word in words:
            str_word = str(word)
            encoded_words += cls.encode_int32(len(str_word))
            encoded_words += str_word
            encoded_words += '\x00'
            size += len(str_word) + 5
        
        return size, encoded_words

    @classmethod
    def decode_words(cls, size, data):
        words = []
        offset = 0
        while offset < size:
            word_len = cls.decode_int32(data[offset : offset + 4])      
            word = data[offset + 4 : offset + 4 + word_len]
            words.append(int(word) if word.isdigit() else word)
            offset += word_len + 5

        return words

    @classmethod
    def encode_packet(cls, is_from_server, is_response, sequence, words):
        encoded_header = cls.encode_header(is_from_server, is_response, sequence)
        encoded_num_words = cls.encode_int32(len(words))
        [words_size, encoded_words] = cls.encode_words(words)
        encoded_size = cls.encode_int32(words_size + 12)
        return encoded_header + encoded_size + encoded_num_words + encoded_words

    @classmethod    
    def decode_packet(cls, data):
        [is_from_server, is_response, sequence] = cls.decode_header(data)
        words_size = cls.decode_int32(data[4:8]) - 12
        words = cls.decode_words(words_size, data[12:])
        return [is_from_server, is_response, sequence, words]



    # Encode a request packet
    @classmethod
    def encode_client_request(cls, words):
        #global client_sequence_nr
        packet = cls.encode_packet(False, False, cls.client_sequence_nr, words)
        cls.client_sequence_nr = (cls.client_sequence_nr + 1) & 0x3fffffff
        return packet

    # Encode a response packet
    @classmethod
    def encode_client_response(cls, sequence, words):
        return cls.encode_packet(True, True, sequence, words)

    @classmethod
    def contains_complete_packet(cls, data):
        if len(data) < 8:
            return False
        if len(data) < cls.decode_int32(data[4:8]):
            return False
        return True

    @classmethod
    def receive_packet(cls, _socket):
        receive_buffer = ""
        while not cls.contains_complete_packet(receive_buffer):
            try:
                data = _socket.recv(4096)
                receive_buffer += data
                if data == "":
                    raise exceptions.NoDataReceived('socket returned empty string ""')
            except socket.timeout:
                raise exceptions.ServerTimeout('')
            
            
            
        packet_size = cls.decode_int32(receive_buffer[4:8])

        packet = receive_buffer[0:packet_size]
        receive_buffer = receive_buffer[packet_size:len(receive_buffer)]

        return packet

    @classmethod
    def receive_event(cls, _socket):
        response = cls.receive_packet(_socket)

        [is_from_server, is_response, sequence, words] = cls.decode_packet(response)
        return words

    def send_command(self, _socket, data):
        request = self.encode_client_request(data)
        _socket.send(request)

        response = self.receive_packet(_socket)
        [is_from_server, is_response, sequence, words] = self.decode_packet(response)
        return words

    @staticmethod
    def make_password_hash(salt, password):
        """
        Hash and salt password
        """
        password_hash = hashlib.md5()
        password_hash.update(salt)
        password_hash.update(password)
        return password_hash.digest()
