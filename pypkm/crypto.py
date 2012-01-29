# coding=utf-8

"""Encrypt and decrypt Pokémon data.

Pokémon data is encrypted using a linear congruential random number
generator (LC RNG). The game encrypts the data when sending data over
the GTS or when storing the Pokémon in its save file.

If we break a traditional 136-byte Pokémon file up, bytes 0x00 to 0x07
would be unencrypted, and the following 128 bytes would account for
the data to be encrypted/decrypted.

To encrypt, shuffle the blocks using the PV to calculate a shift value,
then apply a XOR transformation to each two-byte word of the data using
an instance of the PRNG seeded by the checksum. To decrypt, apply the
XOR transformation and then unshuffle the blocks.

If the data includes party information, a second shuffling and
transformation is applied but with the PRNG seeded by the PV, not the
checksum.

@see http://projectpokemon.org/wiki/Pokemon_NDS_Structure
@see http://projectpokemon.org/wiki/Pokemon_Black/White_NDS_Structure
"""

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import struct
from array import array
from pypkm.rng import Prng, Grng

def checksum(data, size='H'):
    """Calculate the checksum of data using size as word-length.
    
    This defaults to 'H' (a two-byte word) because it's what the
    Pokémon games use.
    """
    
    data = array(size, data)
    chksum = 0
    
    for word in data:
        chksum += word
    
    chksum &= 0xFFFF
    
    return chksum

def _unshuffle(pv, data):
    """Unshuffle PKM binary data according to a shift value.

    Unshuffling data has different permuations than shuffling data.
    Until I figure out a way to convey this pattern mathematically,
    I'll have to resort to hardcoding the stray permutations in a
    dict.

    Keyword arguments:
    pv (int) -- the Pokémon's personality value
    data (int) -- the PKM data to unshuffle
    """
    stray_perms = {
        8: 12,
        9: 18,
        10: 13,
        11: 19,
        12: 8,
        13: 10,
        15: 20,
        17: 22,
        18: 9,
        19: 11,
        20: 15,
        22: 17,
    }

    shiftval = ((pv >> 0xD) & 0x1F) % 24

    if stray_perms.get(shiftval) is None:
        return _shuffle(pv, data)
    
    return _shuffle(pv, data, shiftval=stray_perms.get(shiftval))

def _shuffle(pv, data, shiftval=None):
    """Shuffle the data according to a shift value derived from the PV.
    
    Data stored in .pkm files is split into five blocks: one
    unencrypted block the PV and checksum, and four encrypted blocks
    containing all other information. In order to encrypt (for saving)
    or decrypt (for reading) .pkm files, the four encrypted blocks must
    be shuffled based on the supplied PV.
    
    The data must be a multiple of 4 or it will be padded to fit. Most
    of the time, the supplied data will be 128 bytes (the length of
    Pokémon data).
    
    The blocks are shifted in an ascending permutation.  To wit:
        00 = ABCD   01 = ABDC   02 = ACBD   03 = ACDB
        04 = ADBC   05 = ADCB   06 = BACD   07 = BADC
        08 = BCAD   09 = BCDA   10 = BDAC   11 = BDCA
        12 = CABD   13 = CADB   14 = CBAD   15 = CBDA
        16 = CDAB   17 = CDBA   18 = DABC   19 = DACB
        20 = DBAC   21 = DBCA   22 = DCAB   23 = DCBA
    
    Given a list [ 'A', 'B', 'C', 'D' ], we can calculate which
    elements to pop out to yield the correct order, e.g.:
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
     
    The previous comment section (along with basically this entire
    function) was stolen directly from tsanth's code because it's
    great.

    Keyword arguments:
    pv (int) -- personality value
    data (string) -- 128 byte length of Pokémon data
    shiftval (int) -- optional forced shift value
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
    if shiftval is None:
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

def _unpack(data):
    """Unpack a PKM file into Pokémon data.

    Keyword arguments:
    data (string) -- the PKM file data
    """

    pv = struct.unpack('<L', data[:4])[0]
    chksum = struct.unpack('<H', data[6:8])[0]

    return (pv, chksum, data[8:136], data[136:])

def _pack(pv, chksum, box_data, party_data):
    """Pack Pokémon data into a PKM file.

    Keyword arguments:
    pv (int) -- the Pokémon's personality value
    chksum (int) -- the data's checksum
    data (string) -- the Pokémon data
    """

    chunks = [
        struct.pack('<L', pv),
        '\x00\x00',
        struct.pack('<H', chksum),
        box_data,
        party_data,
    ]
    return ''.join(chunks)

def _crypt(seed, data):
    """Encrypts/decrypts data with the given seed.

    Keyword arguments:
    seed (int) -- the seed to use in the LC RNG
    data (string) -- the Pokémon data to process
    """

    data = array('H', data)
    lc = Prng(seed)

    new_data = array('H')
    for word in data:
        new_data.append(word ^ lc.advance())
    
    return new_data.tostring()

def encrypt(data):
    """Encrypt PKM data.

    Keyword arguments:
    data (string) -- Pokémon data to encrypt
    """
    
    (pv, chksum, box_data, party_data) = _unpack(data)

    box_data = _shuffle(pv, box_data)
    chksum = _checksum(box_data)
    box_data = _crypt(chksum, box_data)

    party_data = _shuffle(pv, party_data)
    party_data = _crypt(pv, party_data)

    return _pack(pv, chksum, box_data, party_data)

def decrypt(data):
    """Decrypt a PKM binary.

    Keyword arguments:
    data (string) -- PKM binary to decrypt
    """

    (pv, chksum, box_data, party_data) = _unpack(data)
    
    box_data = _crypt(chksum, box_data)
    box_data = _unshuffle(pv, box_data)

    party_data = _crypt(pv, party_data)
    party_data = _unshuffle(pv, party_data)

    return _pack(pv, chksum, box_data, party_data)

def encrypt_gts(data):
    """Encrypt PKM data for use in the GTS.

    Keyword arguments:
    data (string) -- the Pokémon data to encrypt
    """
    pass

def decrypt_gts(data):
    """Decrypt PKM bin sent over the GTS.

    Keyword arguments:
    data (string) -- the Pokémon binary to decrypt
    """
    pass