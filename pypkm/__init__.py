# coding=utf-8

"""PyPKM - Easy PKM File Manipulation

"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'
__version__ = '0.4'

from pypkm.pkm import Gen4Pkm, Gen5Pkm

def load(gen, data):
    """Load PKM data.

    Keyword arguments:
    gen (int) -- the file's game generation
    data (str) -- the file's binary data
    """
    if gen == 5:
        return Gen5Pkm(data)
    elif gen == 4:
        return Gen4Pkm(data)

def new(gen):
    """Create a new PKM file.

    Keyword arguments:
    gen (int) -- the file's game generation
    """
    if gen == 5:
        return Gen5Pkm()
    elif gen == 4:
        return Gen4Pkm()