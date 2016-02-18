import unittest
from frostbite_rcon_utils.encoder import encode_packet
from frostbite_rcon_utils.decoder import decode_int32
from frostbite_rcon_utils.helpers import create_packet


class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.packet = create_packet(1, False, False, ['hej'])
        self.encoded_packet = encode_packet(self.packet)

    def test_encode_packet_output_type(self):
        self.assertEqual(type(self.encoded_packet), bytes,
                         'encode_packet doesn\'t return a string')

    def test_encode_packet_output_size(self):
        self.assertEqual(len(self.encoded_packet), self.packet['size'],
                         'encode_packet output length is wrong')

    def test_encode_packet_output_encodes_size(self):
        self.assertEqual(decode_int32(self.encoded_packet[4:8]), self.packet['size'],
                         'encode_packet doesn\'t encode size')

    def test_encode_packet_output_encodes_total_words_length(self):
        self.assertEqual(decode_int32(self.encoded_packet[8:12]), self.packet['total_words_length'],
                         'encode_packet doesn\'t encode total_words_length')

    def test_encode_packet_output_encodes_sequence(self):
        self.assertEqual(decode_int32(self.encoded_packet[0:4]) & 0x3fffffff, self.packet['sequence'],
                         'encode_packet doesn\'t encode the sequence')

    def test_encode_packet_output_encodes_is_from_server(self):
        self.assertEqual(decode_int32(self.encoded_packet[0:4]) & 0x80000000 > 0, self.packet['is_from_server'],
                         'encode_packet doesn\'t encode the is_from_server flag')

    def test_encode_packet_output_encodes_is_response(self):
        self.assertEqual(decode_int32(self.encoded_packet[0:4]) & 0x40000000 > 0, self.packet['is_response'],
                         'encode_packet doesn\'t encode the is_response flag')