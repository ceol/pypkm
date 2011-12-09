# coding=utf-8

"""PKM file structure and data.

This is mostly here as a reference to the file structure and if I ever need
to unpack the entire file, the struct format string is already available.

Because there is no official documentation for PKM files, some bytes are
still unknown, so they are kept as-is instead of being replaced with NUL.
These bytes are denoted by a backslash or question mark immediately after the
line's comment delimiter and labeled as 'unused' or 'unknown', respectively.

@see http://docs.python.org/library/struct.html
@see http://projectpokemon.org/wiki/Pokemon_NDS_Structure
@see http://projectpokemon.org/wiki/Pokemon_Black/White_NDS_Structure
"""

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

GEN5 = [
    # Block 0
    [
        'L',   # [0x00-0x03] personality value
        '2B',  #\[0x04-0x05] unused
        'H',   # [0x06-0x07] checksum
    ],
    
    # Block A
    [
        'H',   # [0x08-0x09] national pokédex ID
        'H',   # [0x0A-0x0B] held item ID
        'H',   # [0x0C-0x0D] original trainer ID
        'H',   # [0x0E-0x0F] original trainer secret ID
        'L',   # [0x10-0x13] experience points total
        'B',   # [0x14] friendship total (or steps to hatch if egg)
        'B',   # [0x15] ability ID
        'B',   # [0x16] markings ID
        'B',   # [0x17] language ID
        'B',   # [0x18] hit points EV
        'B',   # [0x19] attack EV
        'B',   # [0x1A] defense EV
        'B',   # [0x1B] speed EV
        'B',   # [0x1C] special attack EV
        'B',   # [0x1D] special defense EV
        'B',   # [0x1E] cool CV
        'B',   # [0x1F] beauty CV
        'B',   # [0x20] cute CV
        'B',   # [0x21] smart CV
        'B',   # [0x22] tough CV
        'B',   # [0x23] sheen CV
        'B',   # [0x24] sinnoh ribbon set 1-1
        'B',   # [0x25] sinnoh ribbon set 1-2
        'B',   # [0x26] sinnoh ribbon set 2-1
        'B',   # [0x27] sinnoh ribbon set 2-2
    ],
    
    # Block B
    [
        'H',   # [0x28-0x29] move 1 ID
        'H',   # [0x2A-0x2B] move 2 ID
        'H',   # [0x2C-0x2D] move 3 ID
        'H',   # [0x2E-0x2F] move 4 ID
        'B',   # [0x30] move 1 current PP
        'B',   # [0x31] move 2 current PP
        'B',   # [0x32] move 3 current PP
        'B',   # [0x33] move 4 current PP
        'B',   # [0x34] move 1 PP-Up total
        'B',   # [0x35] move 2 PP-Up total
        'B',   # [0x36] move 3 PP-Up total
        'B',   # [0x37] move 4 PP-Up total
        'L',   # [0x38-0x3B] IV bits
        'B',   # [0x3C] hoenn ribbon set 1-1
        'B',   # [0x3D] hoenn ribbon set 1-2
        'B',   # [0x3E] hoenn ribbon set 2-1
        'B',   # [0x3F] hoenn ribbon set 2-2
        'B',   # [0x40] fateful encounter, gender, and alternate forms bits
        'B',   # [0x41] nature
        'B',   # [0x42] dream world ability flag
        '5B',  #\[0x43-0x47] unused 
    ],
    
    # Block C
    [
        '11H', # [0x48-0x5D] nickname (unicode bytes)
        'B',   #\[0x5E] unused
        'B',   # [0x5F] hometown ID
        'B',   # [0x60] sinnoh ribbon set 3-1
        'B',   # [0x61] sinnoh ribbon set 3-2
        'B',   # [0x62] sinnoh ribbon set 4-1
        'B',   # [0x63] sinnoh ribbon set 4-2
        '4B',  #\[0x64-0x67] unused
    ],
    
    # Block D
    [
        '8H',  # [0x68-0x77] original trainer name (unicode bytes)
        'B',   # [0x78] year egg received (-2000)
        'B',   # [0x79] month egg received
        'B',   # [0x7A] day egg received
        'B',   # [0x7B] year met (-2000)
        'B',   # [0x7C] month met
        'B',   # [0x7D] day met
        'H',   # [0x7E-0x7F] egg received location ID
        'H',   # [0x80-0x81] met at location ID
        'B',   # [0x82] pokérus flag
        'B',   # [0x83] poké ball ID
        'B',   # [0x84] met at level and original trainer gender
        'B',   # [0x85] encounter type ID
        '2B',  #\[0x86-0x87] unused
    ],
    
    # Battle Data
    [
        'B',   # [0x88] status effect bits
        'B',   #?[0x89] unknown flag (maximum value 0x0F)
        '2B',  #?[0x8A-0x8B] unknown
        'B',   # [0x8C] level
        'B',   # [0x8D] capsule index for seals
        'H',   # [0x8E-0x8F] current hit points
        'H',   # [0x90-0x91] maximum hit points
        'H',   # [0x92-0x93] attack
        'H',   # [0x94-0x95] defense
        'H',   # [0x96-0x97] speed
        'H',   # [0x98-0x99] special attack
        'H',   # [0x9A-0x9B] special defense
        '56B', #?[0x9C-0xD3] unknown trash data
        '8B',  #?[0xD4-0xDB] unknown (all 0s)
    ],
]

GEN4 = [
    # Block 0
    [
        
    ],
    
    # Block A
    [
        
    ],
    
    # Block B
    [
        
    ],
    
    # Block C
    [
        
    ],
    
    # Block D
    [
        
    ],
    
    # Battle Data
    [
        
    ],
]