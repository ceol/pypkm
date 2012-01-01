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