"""
Hamming and Manchester Encoding example
Author: Joel Addison
Date: March 2013
Functions to do (7,4) hamming encoding and decoding, including error detection
and correction.
Manchester encoding and decoding is also included, and by default will use
least bit ordering for the byte that is to be included in the array.
"""
from math import *
#import logging
#import sys
#import logger_format

# List of syndrome positions. SYNDROME_CHECK[pos] will give the
# bit in the provided encoded byte that needs to be fixed
# Note: bit order used is 7 6 5 4 3 2 1 0
SYNDROME_CHECK = [-1, 6, 5, 0, 4, 1, 2, 3]

#logger = daiquiri.getLogger(__name__)

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#handler = logger_format.RainbowLoggingHandler(sys.stdout)
#handler.setFormatter(formatter)
#logger.addHandler(handler)

def extract_bit(byte, pos):
    """
    Extract a bit from a given byte using MS ordering.
    ie. B7 B6 B5 B4 B3 B2 B1 B0
    """
    return ((byte >> pos) & 0b1)


def hamming_encode_nibble(data):
    """
    Encode a nibble using Hamming encoding.
    Nibble is provided in form 0b0000DDDD == 0 0 0 0 D3 D2 D1 D0
    Encoded byte is in form P H2 H1 H0 D3 D2 D1 D0
    """

    # Get data bits
    d = [0, 0, 0, 0]
    d[0] = extract_bit(data, 0)
    d[1] = extract_bit(data, 1)
    d[2] = extract_bit(data, 2)
    d[3] = extract_bit(data, 3)

    # Calculate hamming bits
    h = [0, 0, 0]
    h[0] = (d[0] + d[1] + d[3]) % 2
    h[1] = (d[0] + d[2] + d[3]) % 2
    h[2] = (d[1] + d[2] + d[3]) % 2

    # Calculate parity bit, using even parity
    p = 0 ^ d[0] ^ d[1] ^ d[2] ^ d[3] ^ h[0] ^ h[1] ^ h[2]

    # Encode byte
    encoded = (data & 0x0f)
    encoded |= (p << 7) | (h[2] << 6) | (h[1] << 5) | (h[0] << 4)

    return encoded

def get_parity(n): 
    parity = 0
    while n: 
        parity = ~parity 
        n = n & (n - 1) 
    return parity 

def hamming_encode_nbit(data, data_width):
    """
    Encode data of data_width suing Hamming encoding.
    only the encoded parity bits are returned
    Eg. for data_width = 4
    Nibble is provided in form 0bDDDD ==  D3 D2 D1 D0
    Encoded byte is in form  D2 D2 D1 H2 D0 H1 H0
    Returned value: H2 H1 H0 
    """
    #logger.debug('Data for encoding: {}'.format(data))
    bit_pos = {}
    #logger.debug('# data width : {}'.format(data_width))
    num_encode_bits = int(log2(data_width)) + 1
    #logger.debug('# encode bits: {}'.format(num_encode_bits))
    total_bits = data_width + num_encode_bits
    #logger.debug('# total_bits: {}'.format(total_bits))

    data_index = 0
    for index in range(1,(total_bits+1)):
        binary_key = bin(index)[2:]
        binary_key = binary_key.zfill(num_encode_bits)
        #logger.debug('binary_key: {}'.format(binary_key))
        if(ceil(log2(index)) == floor(log2(index))):
            bit_pos[index] = 'H'
        else:
            bit_pos[index] = extract_bit(data, data_index)
            data_index = data_index + 1
    
    data_indexed = ''
    for key in sorted(bit_pos.keys()):
        data_indexed =  str(bit_pos[key]) + ' ' + data_indexed
    
    #logger.debug('Data positioned: {}'.format(data_indexed))

    for key in sorted(bit_pos.keys()):
        if bit_pos[key] == 'H':
            check_key = key
            n = ''
            for key1 in sorted(bit_pos.keys()):
                if (((check_key & key1) == check_key)): 
                    bit_pos[check_key] = bit_pos[check_key] + ':' + str(key1)
            parity_index = bit_pos[check_key].split(':')[2:]
            #logger.debug(parity_index)
            for i in range(len(parity_index)):
                n = n + str(bit_pos[int(parity_index[i])])
            if(get_parity(int(n,2)) == -1):
                bit_pos[check_key] = 1
            else:
                bit_pos[check_key] = 0


    data_indexed = ''
    for key in sorted(bit_pos.keys()):
        data_indexed =  str(bit_pos[key]) + ' ' + data_indexed
    
    #logger.debug('Encd positioned: {}'.format(data_indexed))

    ecc_encode = ''
    data_encoded = ''
    for index in range(1,(total_bits+1)):
        data_encoded = str(bit_pos[index]) + data_encoded
        if(ceil(log2(index)) == floor(log2(index))):
            ecc_encode = str(bit_pos[index]) + ecc_encode
    if(get_parity(int(data_encoded,2)) == -1):
        ded = 1
    else:
        ded = 0

    ecc_encode = str(ded) + str(ecc_encode)
    return bin(int(ecc_encode, 2))[2:].zfill((num_encode_bits+1))

def hamming_decode_byte(byte):
    """
    Decode a single hamming encoded byte, and return a decoded nibble.
    Input is in form P H2 H1 H0 D3 D2 D1 D0
    Decoded nibble is in form 0b0000DDDD == 0 0 0 0 D3 D2 D1 D0
    """
    error = 0
    corrected = 0

    # Calculate syndrome
    s = [0, 0, 0]

    # D1 + D2 + D3 + H0
    s[0] = (extract_bit(byte, 1) + extract_bit(byte, 2) +
            extract_bit(byte, 3) + extract_bit(byte, 4)) % 2

    # D0 + D2 + D3 + H1
    s[1] = (extract_bit(byte, 0) + extract_bit(byte, 2) +
            extract_bit(byte, 3) + extract_bit(byte, 5)) % 2

    # D0 + D1 + D3 + H2
    s[2] = (extract_bit(byte, 0) + extract_bit(byte, 1) +
            extract_bit(byte, 3) + extract_bit(byte, 6)) % 2

    syndrome = (s[0] << 2) | (s[1] << 1) | s[2]

    if syndrome:
        # Syndrome is not 0, so correct and log the error
        error += 1
        byte ^= (1 << SYNDROME_CHECK[syndrome])
        corrected += 1

    # Check parity
    p = 0
    for i in range(0, 7):
        p ^= extract_bit(byte, i)

    if p != extract_bit(byte, 7):
        # Parity bit is wrong, so log error
        if syndrome:
            # Parity is wrong and syndrome was also bad, so error is not corrected
            corrected -= 1
        else:
            # Parity is wrong and syndrome is fine, so corrected parity bit
            error += 1
            corrected += 1

    return ((byte & 0x0f), error, corrected)


def manchester_encode(byte):
    """
    Encode a byte using Manchester encoding. Returns an array of bits.
    Adds two start bits (1, 1) and one stop bit (0) to the array.
    """
    # Add start bits (encoded 1, 1)
    manchester_encoded = [0, 1, 0, 1]

    # Encode byte
    for i in range(7, -1, -1):
        if extract_bit(byte, i):
            manchester_encoded.append(0)
            manchester_encoded.append(1)
        else:
            manchester_encoded.append(1)
            manchester_encoded.append(0)

    # Add stop bit (encoded 0)
    manchester_encoded.append(1)
    manchester_encoded.append(0)

    return manchester_encoded


def manchester_decode(manchester_array):
    """
    Decode a Manchester array to a single data byte.
    """
    decoded = 0
    for i in range(0, 8):
        bit = 7 - i
        # Use the second value of each encoded bit, as that is the bit value
        # eg. 1 is encoded to [0, 1], so retrieve the second bit (1)
        decoded |= manchester_array[4 + (i * 2) + 1] << (bit)

    return decoded


def reorder_byte(byte):
    """
    Changes a byte in most significant bit ordering into least significant
    bit ordering, or vice versa.
    """
    new_byte = 0

    for i in range(0, 8, 1):
        new_byte |= extract_bit(byte, i) << (7 - i)

    return new_byte


def encode_byte(byte, ls_order=True):
    """
    Encodes the given byte using Hamming encoding, followed by Manchester
    encoding.
    Uses least bit ordering for the Manchester encoding by default.
    """
    ls_nibble = byte & 0x0f
    ms_nibble = (byte & 0xf0) >> 4

    ls_hamming = hamming_encode_nibble(ls_nibble)
    ms_hamming = hamming_encode_nibble(ms_nibble)

    if ls_order:
        ls_hamming = reorder_byte(ls_hamming)
        ms_hamming = reorder_byte(ms_hamming)

    ls_manchester = manchester_encode(ls_hamming)
    ms_manchester = manchester_encode(ms_hamming)

    return ls_manchester, ms_manchester


def decode_byte(ls_manchester, ms_manchester, ls_order=True):
    """
    Decodes two manchester arrays containing hamming encoded nibbles
    of a single byte. The arrays are first decoded to a hamming byte, then
    decoded from the hamming byte to a single nibble. The nibbles are joined
    to get the final byte.
    By default, it is assumed the manchester array contains a byte using
    least bit ordering.
    """
    ls_hamming = manchester_decode(ls_manchester)
    ms_hamming = manchester_decode(ms_manchester)

    if ls_order:
        ls_hamming = reorder_byte(ls_hamming)
        ms_hamming = reorder_byte(ms_hamming)

    ls_nibble, ls_error, ls_corrected = hamming_decode_byte(ls_hamming)
    ms_nibble, ms_error, ms_corrected = hamming_decode_byte(ms_hamming)

    return ls_nibble | (ms_nibble << 4)
