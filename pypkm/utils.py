# coding=utf-8

"""General utilities for working with file byte data.

These functions could potentially be used to manipulate byte data in general,
so I want to keep them separate for sanity. The *bit functions are really
just so I don't have a bunch of bit shifting thrown in my code and not know
immediately what it's doing.
"""

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

from array import array

def setbit(i, bit):
    "Set a specific bit for an int i."
        
    return (1 << bit) | i

def clearbit(i, bit):
    "Clear a specific bit from an int i."
    
    return i & ~(1 << bit)

def getbit (i, bit):
    "Retrieve a bit from an int i."
    
    return (i >> bit) & 1

def checksum(data, size='H'):
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