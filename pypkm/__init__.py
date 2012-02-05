# coding=utf-8

"""PyPKM - Easy PKM File Manipulation

This utility serves as a friendly way to create, edit, encrypt,
decrypt, and convert PKM files. Its goal is to faciliate the creation
of more end-user tools and allow developers to work with PKM files.

Example usage:
    >>> import pypkm
    >>> data = open('/path/to/pokemon.pkm', 'r').read()
    >>> pkm = pypkm.load(gen=4, data=data)
    >>> pkm.moves.move1
    95
    >>> pkm.exp = 10000
    >>> data = pkm.tostring() # save this somewhere
    >>> new_pkm = pkm.toparty()
    >>> data = new_pkm.tostring() # save this somewhere


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
__version__ = '0.5'

from pypkm.pkm import get_pkmobj

def load(gen, data):
    """Load PKM data.

    Keyword arguments:
    gen (int) -- the file's game generation
    data (str) -- the file's binary data
    """
    return get_pkmobj(gen, data)

def new(gen):
    """Create a new PKM file.

    Keyword arguments:
    gen (int) -- the file's game generation
    """
    return get_pkmobj(gen, '\x00' * 136)