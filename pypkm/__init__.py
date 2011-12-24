# coding=utf-8

"""PyPKM: Easy PKM file manipulation.

This utility serves as a friendly way to create, edit, encrypt, decrypt, and
convert PKM files. Its goal is to faciliate the creation of more end-user
tools and allow developers to work with PKM files.

Example usage:
    >>> from pypkm import Pkm
    >>> pkm = Pkm().load(gen=4, path='gengar.pkm')
    >>> pkm.move1
    95
    >>> pkm.level = 100
    >>> pkm.save()
    gengar_new.pkm
    >>> pkm.level = 50
    >>> pkm.save('gengar_50.pkm')
    gengar_50.pkm

For instructions on how to set a specific attribute, refer to that
attribute's function in the Pkm class.

The encryption and decryption functions (including checksum and shuffle) are
taken from the pycrypto/crypto module created by Stephen Anthony Uy
<tsanth@iname.com>. Somehow, somewhere I came across this module, and it's
been an extremely valuable tool for encrypting and decrypting PKM files to
send over the GTS.

Knowledge of the PKM file structure comes from the awesome people at
ProjectPokemon <http://projectpokemon.org/>, both on the forums and in their
IRC channel.
"""

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

from pypkm.attr import PkmAttrMapper

class PkmBase(PkmAttrMapper):
    "Base class for the Pkm class."
    pass

class Pkm(PkmBase):
    "Wrapper class for all PKM file manipulation."
    pass

def new(gen):
    "Create a PKM file from scratch and return a Pkm instance."
    
    return Pkm().new(gen=gen)

def load(gen, path=None, data=None):
    "Load a PKM file and return a Pkm instance."
    
    return Pkm().load(gen=gen, path=path, data=data)