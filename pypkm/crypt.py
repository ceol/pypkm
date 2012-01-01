# coding=utf-8

"Encrypt and decrypt Pokémon data."

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import struct
from pypkm.rng import Prng, Grng

def _checksum(data, size='H'):
    """Calculate the checksum of data using the size as the word-length.
    
    This defaults to 'H' (a two-byte word) because it's what the Pokémon
    games use.
    """
    
    data = array(size, data)
    chksum = 0
    
    for word in data:
        chksum += word
    
    chksum &= 0xFFFF
    
    return chksum

def _shuffle(pv, data):
    """Shuffle the data according to a shift value derived from the PV.
    
    Data stored in .pkm files is split into five blocks: one unencrypted
    block the PV and checksum, and four encrypted blocks containing all other
    information. In order to encrypt (for saving) or decrypt (for reading)
    .pkm files, the four encrypted blocks must be shuffled based on the
    supplied PV.
    
    The data must be a multiple of 4 or it will be padded to fit. Most of the
    time, the supplied data will be 128 bytes (the length of Pokémon data).
    
    The blocks are shifted in an ascending permutation.  To wit:
        00 = ABCD   01 = ABDC   02 = ACBD   03 = ACDB
        04 = ADBC   05 = ADCB   06 = BACD   07 = BADC
        08 = BCAD   09 = BCDA   10 = BDAC   11 = BDCA
        12 = CABD   13 = CADB   14 = CBAD   15 = CBDA
        16 = CDAB   17 = CDBA   18 = DABC   19 = DACB
        20 = DBAC   21 = DBCA   22 = DCAB   23 = DCBA
    
    Given a list [ 'A', 'B', 'C', 'D' ], we can calculate which elements
    to pop out to yield the correct order, e.g.:
        pop #1 (shiftVal / 6):
            0 = A (BCD)
            1 = B (ACD)
            2 = C (ABD)
            3 = D (ABC)
    
        pop #2 ((shiftVal % 6) / 2):
            0 = first
            1 = second
            2 = third
    
        pop #3 ((shiftVal % 6) % 2)):
            0 = first
            1 = second
    
        pop #4 is always the remaining element.
     
    The previous comment section (along with basically this entire function)
    was stolen directly from tsanth's code because it's great.

    Keyword arguments:
    pv (longint) -- personality value
    data (string) -- 128 byte length of Pokémon data
    """
        
    # Pad the data to fit into a multiple of 4.
    if len(data) % 4 != 0:
        data += '\x00' * (4 - (len(data) % 4))
    
    # Create the blocks of data using its length.
    blocksize = len(data) / 4
    blocks = [
        data[:(blocksize * 1)],
        data[(blocksize * 1):(blocksize * 2)],
        data[(blocksize * 2):(blocksize * 3)],
        data[(blocksize * 3):],
    ]
    
    # The shift value is derived from the PV
    shiftval = ((pv >> 0xD) & 0x1F) % 24
    
    blockorder = [
        shiftval / 6,
        (shiftval % 6) / 2,
        (shiftval % 6) % 2,
        0,
    ]
    
    shuffledblocks = []
    
    # Grab the correct block according to the block order.
    for block in blockorder:
        shuffledblocks.append(blocks.pop(block))
    
    shuffledblocks = ''.join(shuffledblocks)
    
    return shuffledblocks

def _pack(pv, chksum, data):
    """Pack Pokémon data into a PKM file.

    Keyword arguments:
    pv (longint) -- the Pokémon's personality value
    chksum (int) -- the data's checksum
    data (string) -- the Pokémon data
    """

    chunks = [
        struct.pack('L', pv),
        '\x00\x00',
        struct.pack('H', chksum),
        data
    ]
    return ''.join(chunks)

def _crypt(seed, data):
    """Encrypts/decrypts data with the given seed.

    Logic taken from tsanth's _crypt() function.

    Keyword arguments:
    seed (int) -- the seed to use in the LC RNG
    data (string) -- the Pokémon data to process
    """

    data = array('H', data)
    lc = Prng(seed)

    for word in data:
        data.append(word ^ lc.advance())
    
    return data.tostring()

def encrypt(pv, blocks):
    """Encrypt PKM data.

    Keyword arguments:
    pv (longint) -- the Pokémon's personality value
    blocks (string) -- the Pokémon blocks to encrypt
    """
    
    shuffled = _shuffle(pv, blocks)
    chksum = _checksum(shuffled)
    encrypted = _crypt(chksum, shuffled)

    return _pack(pv, chksum, encrypted)

def decrypt(pv, chksum, blocks):
    """Decrypt PKM data.

    Keyword arguments:
    pv (longint) -- the Pokémon's personality value
    chksum (int) -- checksum of the decrypted blocks
    blocks (string) -- the Pokémon blocks to decrypt
    """
    
    decrypted = _crypt(chksum, blocks)
    shuffled = _shuffle(pv, decrypted)

    return _pack(pv, chksum, shuffled)

def encrypt_gts(data):
    """Encrypt PKM data for use in the GTS.

    Keyword arguments:
    data (string) -- the Pokémon data to encrypt
    """
    pass

def decrypt_gts(data):
    """Decrypt PKM data sent over the GTS.

    Keyword arguments:
    data (string) -- the Pokémon data to decrypt
    """
    pass