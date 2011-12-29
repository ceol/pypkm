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
    >>> pkm.exp = 5000
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

import os
import sqlite3
import struct
from pypkm.attr import PkmAttrMapper

class PkmBase(PkmAttrMapper):
    "Base class for the Pkm class."
    
    def toparty(self):
        "Add battle data to the PKM file."

        data = self.get_boxdata()

        # first four bytes don't need to be set by us
        battle_data = '\x00' * 4

        level = self.get_level(pokemon_id=self.id, exp=self.exp)
        battle_data += struct.pack('<B', level)
        
        # we don't set the capsule index
        battle_data += '\x00'

        # the nature is used to calculate battle stats (except hp)
        nature = self.get_nature(self.pv % 25)

        base_stats = self.get_basestats(pokemon_id=self.id)

        curhp_stat = self.calcstat(iv=self.hp_iv, ev=self.hp_ev, base=base_stats[0], level=level, nature_stat=None)
        maxhp_stat = curhp_stat
        atk_stat = self.calcstat(iv=self.atk_iv, ev=self.atk_ev, base=base_stats[1], level=level, nature_stat=nature[2])
        def_stat = self.calcstat(iv=self.def_iv, ev=self.def_ev, base=base_stats[2], level=level, nature_stat=nature[3])
        spe_stat = self.calcstat(iv=self.spe_iv, ev=self.spe_ev, base=base_stats[3], level=level, nature_stat=nature[4])
        spa_stat = self.calcstat(iv=self.spa_iv, ev=self.spa_ev, base=base_stats[4], level=level, nature_stat=nature[5])
        spd_stat = self.calcstat(iv=self.spd_iv, ev=self.spd_ev, base=base_stats[5], level=level, nature_stat=nature[6])

        battle_data += struct.pack('<HHHHHHH', curhp_stat, maxhp_stat, atk_stat, def_stat, spe_stat, spa_stat, spd_stat)

        # trash data and capsule seal coords
        if self.is_gen(5):
            battle_data += '\x00' * 64
        elif self.is_gen(4):
            battle_data += '\x00' * 80
        
        new_data = data + battle_data
        self.add_data(new_data)

        return new_data

class Pkm(PkmBase):
    "Wrapper class for all PKM file manipulation."
    pass

def new(gen):
    "Create a PKM file from scratch and return a Pkm instance."
    
    return Pkm().new(gen=gen)

def load(gen, path=None, data=None):
    "Load a PKM file and return a Pkm instance."
    
    return Pkm().load(gen=gen, path=path, data=data)