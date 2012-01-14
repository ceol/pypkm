# coding=utf-8

"""PyPKM: Easy PKM file manipulation.

This utility serves as a friendly way to create, edit, encrypt,
decrypt, and convert PKM files. Its goal is to faciliate the creation
of more end-user tools and allow developers to work with PKM files.

Example usage:
    >>> import pypkm
    >>> pkm = pypkm.load(gen=4, path='gengar.pkm')
    >>> pkm.move1
    95
    >>> pkm.exp = 10000
    >>> data = pkm.tostring() # save this somewhere
    >>> pkm.toparty()
    >>> data = pkm.tostring() # save this somewhere

For instructions on how to set a specific attribute, refer to that
attribute's function in the Pkm class.

The encryption and decryption functions (including checksum and
shuffle) are taken from the pycrypto/crypto module created by Stephen
Anthony Uy <tsanth@iname.com>. Somehow, somewhere I came across this
module, and it's been an extremely valuable tool for encrypting and
decrypting PKM files to send over the GTS.

Knowledge of the PKM file structure comes from the awesome people at
ProjectPokemon <http://projectpokemon.org/>, both on the forums and in
their IRC channel.
"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'
__version__ = '0.3.1'

from pypkm.pkm import Pkm

def new(gen):
    "Create a PKM file from scratch and return a Pkm instance."
    
    return Pkm().new(gen=gen)

def load(gen, data):
    "Load a PKM file and return a Pkm instance."
    
    return Pkm().load(gen=gen, data=data)