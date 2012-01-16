# coding=utf-8

"""Retrieve Pokémon information from a PKM file.


"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

from pypkm.structs import g4pkm, g5pkm
from pypkm.crypto import encrypt, decrypt

class BasePkm(object):

    # Constructor Struct object
    _strc = None

    # Construct Container object
    _ctnr = None

    def __getattr__(self, attr):
        return getattr(self._ctnr, attr)
    
    def __setattr__(self, attr, value):
        if hasattr(self._ctnr, attr):
            setattr(self._ctnr, attr, value)
        else:
            self.__dict__[attr] = value
    
    def _load(self, strc, data):
        self._strc = strc
        self._ctnr = self._strc.parse(data)
    
    def tostring(self):
        return self._strc.build(self._ctnr)

class Gen4Pkm(BasePkm):

    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 136
        
        if len(data) == 136:
            strc = g4pkm.pkm_struct
        elif len(data) == 236:
            strc = g4pkm.pkm_party_struct
        else:
            raise ValueError('Unsupported PKM file length: expected 136 or 236, received {}'.format(len(data)))
        
        self._load(strc, data)

class Gen5Pkm(BasePkm):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 136
        
        if len(data) == 136:
            strc = g5pkm.pkm_struct
        elif len(data) == 220:
            strc = g5pkm.pkm_party_struct
        else:
            raise ValueError('Unsupported PKM file length: expected 136 or 220, received {}'.format(len(data)))
        
        self._load(strc, data)