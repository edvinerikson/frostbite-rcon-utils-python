from struct import pack


def encode_int32(num):
    return pack('<I', num)


def encode_header(packet):
    header = packet['sequence'] & 0x3fffffff
    if packet['is_from_server']:
        header += 0x80000000
    if packet['is_response']:
        header += 0x40000000
    return (encode_int32(header) +
            encode_int32(packet['size']) +
            encode_int32(packet['total_words_length']))


def encode_words(packet):
    words = packet['words']
    encoded_words = b''
    for word in words:
        word = str(word)
        encoded_words += encode_int32(len(word))
        encoded_words += str.encode(word)
        encoded_words += b'\x00'
    return encoded_words


def encode_packet(packet):
    encoded_header = encode_header(packet)
    encoded_words = encode_words(packet)
    return encoded_header + encoded_words
