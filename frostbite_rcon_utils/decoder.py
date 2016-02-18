from struct import unpack

from .helpers import DEFAULT_HEADER_SIZE


def decode_int32(buf):
    return unpack('<I', buf)[0]


def decode_words(buf):
    size = decode_int32(buf[4:8])
    words = []
    offset = DEFAULT_HEADER_SIZE

    while offset < size:
        word_length = decode_int32(buf[offset:offset + 4])
        word = buf[offset + 4:offset + 4 + word_length]
        words.append(int(word) if word.isdigit() else (
            word == 'true' if word == 'true' or word == 'false' else word))
        offset += word_length + 5
    return words


def decode_header(buf):
    header = decode_int32(buf[0:4])
    return {
        'sequence': header & 0x3fffffff,
        'is_response': header & 0x40000000 > 0,
        'is_from_server': header & 0x80000000 > 0,
        'size': decode_int32(buf[4:8]),
        'total_words_length': decode_int32(buf[8:12])
    }


def decode_packet(buf):
    header = decode_header(buf)
    words = decode_words(buf)
    packet = dict(header)
    packet.update(dict(words=words))
    return packet
