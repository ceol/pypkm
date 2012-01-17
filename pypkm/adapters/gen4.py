# coding=utf-8

"""Generation 4 Struct Adapters."""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

from construct import Adapter
from pypkm.sqlite import get_chr, get_ord

class PkmStringAdapter(Adapter):
    def _encode(self, obj, ctx):
        """Converts a unicode string to a list of Gen 4 ords."""

        # enforce unicode
        if not isinstance(obj, unicode):
            obj = obj.decode('utf8')

        ordlist = []

        for chr_ in obj:
            ord_ = get_ord(chr_)
            if ord_ == 0xFFFF:
                break
            ordlist.append(ord_)
        
        while len(ordlist) < (self.bytes - 1):
            ordlist.append(0xFFFF)
        
        ordlist = ordlist[:(self.bytes - 1)]
        ordlist.append(0xFFFF) # enforce term byte

        return ordlist
    
    def _decode(self, obj, ctx):
        """Converts a list of Gen 4 ords to a unicode string."""

        chrlist = []

        for ord_ in obj:
            if ord_ == 0xFFFF:
                break
            chrlist.append(get_chr(ord_))
        
        return ''.join(chrlist)

class NicknameAdapter(PkmStringAdapter):
    bytes = 11

class OTNameAdapter(PkmStringAdapter):
    bytes = 8