# coding=utf-8

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import os
import datetime
import sqlite3
import struct
from pypkm.handlers import load_handler
from pypkm.mappers import load_mapper
from pypkm.crypto import encrypt, encrypt_gts, decrypt, decrypt_gts
from pypkm.sqlite import (get_growthrate, get_level, get_exp, get_nature,
                          get_basestats)
from pypkm.utils import calcstat

class BasePkm(object):
    "Base class for the Pkm class."

    # Instance of PkmBinaryFile
    bin = None

    # Instance of attribute mapper class
    attr = None

    def __getattr__(self, name):
        # Try to avoid infinite recursion by calling __getattribute__
        # and catching the attribute
        try:
            return object.__getattribute__(self.attr, name)()
        except AttributeError:
            # catch exception to raise a more helpful one
            cls = self.__class__.__name__
            error = "'{}' object has no attribute '{}'".format(cls, name)
            raise AttributeError(error)
    
    def __setattr__(self, name, value):
        try:
            getattr(self.attr, name)(value)
        except AttributeError:
            self.__dict__[name] = value
    
    def new(self, gen):
        """Hook for creating a Pkm instance with blank data.

        Keyword arguments:
        gen (int) -- the file's game generation
        """
        
        self.bin = load_handler(gen).new(gen=gen)
        self.attr = load_mapper(bin_=self.bin)

        return self
    
    def load(self, gen, path=None, data=None):
        """Hook for loading data into a new Pkm instance.

        Keyword arguments:
        path (string) -- path to the file to load
        data (string) -- string of byte data
        """

        self.bin = load_handler(gen).load(path=path, data=data)
        self.attr = load_mapper(bin_=self.bin)

        return self
    
    def save(self, path=None, data=None):
        """Hook for saving data.

        Keyword arguments:
        path (string) -- optional path to save
        data (string) -- optional data to save
        """

        return self.bin.save(path=path, data=data)
    
    def toparty(self):
        "Add party data to the PKM file."

        data = self.bin.get_boxdata()
        party_data = []

        # first four bytes don't need to be set by us
        party_data.append('\x00' * 4)

        level = get_level(pokemon_id=self.id, exp=self.exp)
        party_data.append(struct.pack('<B', level))
        
        # we don't set the capsule index
        party_data.append('\x00')

        # the nature is used to calculate battle stats (except hp)
        nature = get_nature(self.pv % 25)

        base_stats = get_basestats(pokemon_id=self.id)

        curhp_stat = calcstat(iv=self.hp_iv, ev=self.hp_ev, base=base_stats[0],
                              level=level, nature_stat=None)
        maxhp_stat = curhp_stat
        atk_stat = calcstat(iv=self.atk_iv, ev=self.atk_ev, base=base_stats[1],
                            level=level, nature_stat=nature[2])
        def_stat = calcstat(iv=self.def_iv, ev=self.def_ev, base=base_stats[2],
                            level=level, nature_stat=nature[3])
        spe_stat = calcstat(iv=self.spe_iv, ev=self.spe_ev, base=base_stats[3],
                            level=level, nature_stat=nature[4])
        spa_stat = calcstat(iv=self.spa_iv, ev=self.spa_ev, base=base_stats[4],
                            level=level, nature_stat=nature[5])
        spd_stat = calcstat(iv=self.spd_iv, ev=self.spd_ev, base=base_stats[5],
                            level=level, nature_stat=nature[6])

        party_data.append(struct.pack('<HHHHHHH', curhp_stat, maxhp_stat,
                                      atk_stat, def_stat, spe_stat, spa_stat,
                                      spd_stat))

        # trash data and capsule seal coords
        if self.bin.is_gen(5):
            party_data.append('\x00' * 64)
        elif self.bin.is_gen(4):
            party_data.append('\x00' * 80)
        
        new_data = [
            data,
            ''.join(party_data),
        ]
        new_data = ''.join(new_data)
        self.bin.add_data(new_data)

        return new_data
    
    def togts(self):
        "Create PKM data to be sent from a fake GTS."
        
        data = self.bin.get_data()
        if len(data) != 136:
            data = self.toparty()
        
        def _gender(val):
            if val == 'm': # male
                return '\x01'
            elif val == 'f': # female
                return '\x02'
            elif val == 'n': # either/neither
                return '\x03'
        
        def _req_data():
            _data = [
                '\x01\x00', # requested dex ID (#001)
                '\x03', # requested gender (either/neither)
                '\x00', # requested min level (any)
                '\x00', # requested max level (any)
                '\x00', # unknown
                '\x01', # sending trainer's gender (female)
                '\x00', # unknown
            ]

            return ''.join(_data)
        
        def _timestamp():
            now = datetime.datetime.now()

            _data = [
                struct.pack('<H', now.year), # deposited year
                struct.pack('<B', now.month), # deposited month
                struct.pack('<B', now.day), # deposited day
                struct.pack('<B', now.hour), # deposited hour
                struct.pack('<B', now.minute), # deposited minute
                struct.pack('<B', now.second), # deposited second
                '\x00', # unknown
            ]

            return ''.join(_data)
        
        def _user_data():
            _data = [
                '\xDB', # country
                '\x02', # city
                '\x08', # trainer sprite (lass)
                '\x01', # is exchanged flag
                '\x08', # game version (soulsilver)
                data[0x17], # language
            ]

            return ''.join(_data)
        
        def _common():
            "Commonly-set GTS data."

            _data = [
                data[0x08:0x0A], # dex ID
                _gender(self.gender), # gender
                data[0x8C], # level
                _req_data(), # requested pokémon data            
                _timestamp(), # date deposited
                _timestamp(), # date traded (?)
                data[0x00:0x04], # pv
            ]

            return ''.join(_data)
        
        # it's easier to grab the raw bin data. don't hate me!
        if self.bin.is_gen(5):
            gts_data = [
                '\x00' * 16, # unused
                _common(), # common data
                data[0x0c:0x0e], # ot ID
                data[0x0e:0x10], # ot secret ID
                data[0x68:0x78], # ot name
                _user_data(), # user metadata
                '\x01\x00', # unknown
            ]
        elif self.bin.is_gen(4):
            gts_data = [
                _common(), # common data
                data[0x68:0x78], # ot name
                data[0x0c:0x0e], # ot ID
                _user_data(), # user metadata
            ]
        
        data = self.encrypt()
        # interpreter-safe concatenation using ''.join
        new_data = [
            data,
            ''.join(gts_data),
        ]
        new_data = ''.join(new_data)
        self.bin.add_data(new_data)

        return new_data
    
    def encrypt(self):
        "Encrypt PKM data."
        
        encrypted_data = encrypt(self.bin.get_data())
        self.bin.add_data(encrypted_data)
        
        return encrypted_data
    
    def decrypt(self):
        "Decrypt PKM data."
        
        decrypted_data = decrypt(self.bin.get_boxdata())
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