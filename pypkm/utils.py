# coding=utf-8

"""General utilities."""

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

def calcstat(self, iv, ev, base, level, nature_stat):
    """Calculate the battle stat of a Pokémon.

    Note that some stats may be off by one compared to the
    "official" PKM data. I've only found this to be true on a
    specific FAL2010 Mew file, but it's worth mentioning. If you
    would like to be safe, deposit the Pokémon in the Day Care and
    take it back out to recreate the party data.

    Keyword arguments:
    iv (int) -- IV stat
    ev (int) -- EV stat
    base (int) -- base stat (from lookup table)
    level (int) -- level (1-100)
    nature_stat (float) -- the stat's nature multiplier (set to
        None if HP)
    """

    # if hp
    if nature_stat is None:
        num = (iv + (2 * base) + (ev / 4.0) + 100) * level
        denom = 100
        stat = (num / denom) + 10

        return int(floor(stat))
    else:
        num = (iv + (2 * base) + (ev / 4.0)) * level
        denom = 100
        stat = (num / denom) + 5

        return int(floor(floor(stat) * nature_stat))