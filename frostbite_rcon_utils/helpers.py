DEFAULT_HEADER_SIZE = 12


def calculate_packet_size(words):
    return DEFAULT_HEADER_SIZE + sum([len(str(word)) + 5 for word in words])


def contains_complete_packet(buf):
    from .decoder import decode_int32
    return not (len(buf) < 8 or len(buf) < decode_int32(buf[4:8]))


def create_packet(sequence, is_from_server, is_response, words):
    packet = {
        'sequence': sequence,
        'is_from_server': is_from_server,
        'is_response': is_response,
        'total_words_length': len(words),
        'size': calculate_packet_size(words),
        'words': words
    }
    return packet
