# coding=utf-8

"""PyPKM: Easy PKM file manipulation.

This utility serves as a friendly way to create, edit, encrypt, decrypt, and
convert PKM files. Its goal is to faciliate the creation of more end-user
tools and allow developers to work with PKM files.

Example usage:
    >>> import pypkm
    >>> pkm = pypkm.load(gen=4, path='gengar.pkm')
    >>> pkm.move1
    95
    >>> pkm.exp = 10000
    >>> pkm.save()
    gengar_new.pkm
    >>> pkm.toparty()
    >>> pkm.save('gengar_party.pkm')
    gengar_party.pkm

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

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'
__version__ = '0.1'

import os
import sqlite3
import struct
from pypkm.binary import PkmBinaryFile
from pypkm.attr import PkmAttrMapper
from pypkm.crypt import encrypt, encrypt_gts, decrypt, decrypt_gts

class BasePkm(object):
    "Base class for the Pkm class."

    # Instance of PkmBinaryFile
    bin = None

    # Instance of PkmAttrMapper
    attr = None

    def __getattr__(self, name):
        # Try to avoid infinite recursion by calling __getattribute__ and
        # catching the attribute
        try:
            func_name = '{}{}'.format('attr__', name)
            return object.__getattribute__(self.attr, func_name)()
        except AttributeError:
            # catch exception to raise a more helpful one
            error = "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)
            raise AttributeError(error)
    
    def __setattr__(self, name, value):
        try:
            getattr(self.attr, 'attr__' + name)(value)
        except AttributeError:
            self.__dict__[name] = value
    
    def new(self, gen):
        """Hook for creating a Pkm instance with blank data.

        Keyword arguments:
        gen (int) -- the file's game generation
        """
        
        self.bin = PkmBinaryFile().new(gen=gen)
        self.attr = PkmAttrMapper(bin_=self.bin)

        return self
    
    def load(self, gen, path=None, data=None):
        """Hook for loading data into a new Pkm instance.

        Keyword arguments:
        path (string) -- path to the file to load
        data (string) -- string of byte data
        """

        self.bin = PkmBinaryFile().load(gen=gen, path=path, data=data)
        self.attr = PkmAttrMapper(bin_=self.bin)

        return self
    
    def toparty(self):
        "Add battle data to the PKM file."

        data = self.bin.get_boxdata()

        # first four bytes don't need to be set by us
        battle_data = '\x00' * 4

        level = self.bin.get_level(pokemon_id=self.id, exp=self.exp)
        battle_data += struct.pack('<B', level)
        
        # we don't set the capsule index
        battle_data += '\x00'

        # the nature is used to calculate battle stats (except hp)
        nature = self.bin.get_nature(self.pv % 25)

        base_stats = self.bin.get_basestats(pokemon_id=self.id)

        curhp_stat = self.bin.calcstat(iv=self.hp_iv, ev=self.hp_ev, base=base_stats[0], level=level, nature_stat=None)
        maxhp_stat = curhp_stat
        atk_stat = self.bin.calcstat(iv=self.atk_iv, ev=self.atk_ev, base=base_stats[1], level=level, nature_stat=nature[2])
        def_stat = self.bin.calcstat(iv=self.def_iv, ev=self.def_ev, base=base_stats[2], level=level, nature_stat=nature[3])
        spe_stat = self.bin.calcstat(iv=self.spe_iv, ev=self.spe_ev, base=base_stats[3], level=level, nature_stat=nature[4])
        spa_stat = self.bin.calcstat(iv=self.spa_iv, ev=self.spa_ev, base=base_stats[4], level=level, nature_stat=nature[5])
        spd_stat = self.bin.calcstat(iv=self.spd_iv, ev=self.spd_ev, base=base_stats[5], level=level, nature_stat=nature[6])

        battle_data += struct.pack('<HHHHHHH', curhp_stat, maxhp_stat, atk_stat, def_stat, spe_stat, spa_stat, spd_stat)

        # trash data and capsule seal coords
        if self.is_gen(5):
            battle_data += '\x00' * 64
        elif self.is_gen(4):
            battle_data += '\x00' * 80
        
        new_data = data + battle_data
        self.bin.add_data(new_data)

        return new_data
    
    def togts(self):
        "Create PKM data to be transferred via the GTS."
        pass
    
    def encrypt(self):
        "Encrypt PKM data."
        
        encrypted_data = encrypt(self.get_data())
        self.bin.add_data(encrypted_data)
        
        return encrypted_data
    
    def decrypt(self):
        "Decrypt PKM data."
        
        decrypted_data = decrypt(self.get_boxdata())
        self.bin.add_data(decrypted_data)

        return decrypted_data
    
    def encrypt_gts(self):
        "Encrypt PKM data for use in the GTS."
        pass
    
    def decrypt_gts(self):
        "Decrypt PKM data sent over the GTS."
        pass

class Pkm(BasePkm):
    "Wrapper class for all PKM file manipulation."
    pass

def new(gen):
    "Create a PKM file from scratch and return a Pkm instance."
    
    return Pkm().new(gen=gen)

def load(gen, path=None, data=None):
    "Load a PKM file and return a Pkm instance."
    
    return Pkm().load(gen=gen, path=path, data=data)