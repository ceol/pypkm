# coding=utf-8

"Encrypt and decrypt Pokémon data."

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

from pypkm.rng import Prng, Grng
from pypkm.utils import checksum

def _shuffle(pv, data):
    """Shuffle the data according to a shift value derived from the PV.
    
    Data stored in .pkm files is split into five blocks: one unencrypted
    block the PV and checksum, and four encrypted blocks containing all other
    information. In order to encrypt (for saving) or decrypt (for reading)
    .pkm files, the four encrypted blocks must be shuffled based on the
    supplied PV.
    
    The data must be a multiple of 4 or it will be padded to fit. Most of the
    time, the supplied data will be 128 bytes (the length of Pokémon data).
    Party data does NOT need to be encrypted, decrypted, or shuffled.
    
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

def _crypt(seed, data):
    "Encrypts data with the given seed."
    pass

def encrypt(data):
    "Encrypt PKM data."
    pass

def decrypt(data):
    "Decrypt PKM data."
    pass

def encrypt_gts(data):
    "Encrypt PKM data for use in the GTS."
    pass

def decrypt_gts(data):
    "Decrypt PKM data sent over the GTS."
    pass