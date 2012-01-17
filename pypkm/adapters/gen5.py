# coding=utf-8

"""Generation 5 Struct Adapters"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

from construct import Adapter

class PkmStringAdapter(Adapter):
    def _encode(self, obj, ctx):
        """Converts a unicode string to a list of ords."""

        # enforce unicode
        if not isinstance(obj, unicode):
            obj = obj.decode('utf8')
        
        ordlist = []

        for chr_ in obj:
            ord_ = ord(chr_)
            if ord_ == 0xFFFF:
                break
            ordlist.append(ord_)

        if len(ordlist) < self.bytes:
            ordlist.append(0xFFFF)
            while len(ordlist) < (self.bytes - 1):
                ordlist.append(0x0000)
        
        ordlist = ordlist[:(self.bytes - 1)]
        ordlist.append(0xFFFF) # enforce term byte

        return ordlist
    
    def _decode(self, obj, ctx):
        """Converts a list of ords to a unicode string."""

        chrlist = []

        for ord_ in obj:
            if ord_ == 0xFFFF:
                break
            chrlist.append(unichr(ord_))
        
        return ''.join(chrlist)

class NicknameAdapter(PkmStringAdapter):
    bytes = 11

class OTNameAdapter(PkmStringAdapter):
    bytes = 8