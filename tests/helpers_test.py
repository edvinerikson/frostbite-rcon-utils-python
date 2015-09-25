import unittest
from frostbite_rcon_utils.helpers import create_packet, calculate_packet_size


class TestHelpers(unittest.TestCase):
    def test_create_packet_output(self):
        generated_packet = create_packet(1, False, False, ['hej'])

        self.assertEqual(generated_packet, dict(sequence=1,
                                                is_from_server=False,
                                                is_response=False,
                                                size=20,
                                                total_words_length=1,
                                                words=['hej']))

    def test_calculate_packet_size_output(self):
        self.assertEqual(calculate_packet_size(['hej']), 20, 'calculate_packet_size is not returning the correct size')
