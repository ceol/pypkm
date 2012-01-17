# coding=utf-8

"""PKM file structure for Generation 5.

All PKM Struct modules should declare a `pkm_struct` variable that is
an instance of construct.Struct.

Note about BitStructs: it appears Construct has some odd formatting, so
the bit order is reversed when declaring BitStructs. This should be
noticeable for ribbons.

@see http://projectpokemon.org/wiki/Pokemon_Black/White_NDS_Structure
"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

# I hate doing this, but apparently it's Construct convention
from construct import *
from pypkm.util import Swapped

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

_block0 = Struct('_block0',
    ULInt32('pv'),
    Padding(2),
    ULInt16('checksum'),
)

_blockA = Struct('_blockA',
    ULInt16('id'),
    ULInt16('item'),
    ULInt16('ot_id'),
    ULInt16('ot_secret_id'),
    ULInt32('exp'),
    ULInt8('happiness'),
    ULInt8('ability'),
    BitStruct('markings',
        Padding(2),
        Flag('diamond'),
        Flag('star'),
        Flag('heart'),
        Flag('square'),
        Flag('triangle'),
        Flag('circle'),
    ),
    ULInt8('language'),
    Struct('evs',
        ULInt8('hp'),
        ULInt8('attack'),
        ULInt8('defense'),
        ULInt8('speed'),
        ULInt8('spattack'),
        ULInt8('spdefense'),
    ),
    Struct('cvs',
        ULInt8('cool'),
        ULInt8('beauty'),
        ULInt8('cute'),
        ULInt8('smart'),
        ULInt8('tough'),
        ULInt8('sheen'),
    ),
    BitStruct('sinnoh_ribbons_set11',
        Flag('alert'),
        Flag('world_ability'),
        Flag('pair_ability'),
        Flag('multi_ability'),
        Flag('double_ability'),
        Flag('great_ability'),
        Flag('ability'),
        Flag('sinnoh_champ'),
    ),
    BitStruct('sinnoh_ribbons_set12',
        Flag('royal'),
        Flag('gorgeous'),
        Flag('smile'),
        Flag('snooze'),
        Flag('relax'),
        Flag('careless'),
        Flag('downcast'),
        Flag('shock'),
    ),
    BitStruct('sinnoh_ribbons_set21',
        Flag('blue'),
        Flag('green'),
        Flag('red'),
        Flag('legend'),
        Flag('history'),
        Flag('record'),
        Flag('footprint'),
        Flag('gorgeous_royal'),
    ),
    BitStruct('sinnoh_ribbons_set22',
        Padding(4),
        Flag('premiere'),
        Flag('classic'),
        Flag('carnival'),
        Flag('festival'),
    ),
)

_blockB = Struct('_blockB',
    Struct('moves',
        ULInt16('move1'),
        ULInt16('move2'),
        ULInt16('move3'),
        ULInt16('move4'),
        ULInt8('move1_pp'),
        ULInt8('move2_pp'),
        ULInt8('move3_pp'),
        ULInt8('move4_pp'),
        ULInt8('move1_ppups'),
        ULInt8('move2_ppups'),
        ULInt8('move3_ppups'),
        ULInt8('move4_ppups'),
    ),
    Embed(Swapped(BitStruct('x38',
        Flag('is_nicknamed'),
        Flag('is_egg'),
        Struct('ivs',
            BitField('spdefense', 5),
            BitField('spattack', 5),
            BitField('speed', 5),
            BitField('defense', 5),
            BitField('attack', 5),
            BitField('hp', 5),
        ),
    ))),
    BitStruct('hoenn_ribbons_set11',
        Flag('beauty_master'),
        Flag('beauty_hyper'),
        Flag('beauty_super'),
        Flag('beauty'),
        Flag('cool_master'),
        Flag('cool_hyper'),
        Flag('cool_super'),
        Flag('cool'),
    ),
    BitStruct('hoenn_ribbons_set12',
        Flag('smart_master'),
        Flag('smart_hyper'),
        Flag('smart_super'),
        Flag('smart'),
        Flag('cute_master'),
        Flag('cute_hyper'),
        Flag('cute_super'),
        Flag('cute'),
    ),
    BitStruct('hoenn_ribbons_set21',
        Flag('artist'),
        Flag('victory'),
        Flag('winning'),
        Flag('champion'),
        Flag('tough_master'),
        Flag('tough_hyper'),
        Flag('tough_super'),
        Flag('tough'),
    ),
    BitStruct('hoenn_ribbons_set22',
        Flag('world'),
        Flag('earth'),
        Flag('national'),
        Flag('country'),
        Flag('sky'),
        Flag('land'),
        Flag('marine'),
        Flag('effort'),
    ),
    Embed(BitStruct('x40',
        BitField('alt_form_unshifted', 5), # leftshift 3
        Flag('is_genderless'), # if both False, then it's male
        Flag('is_female'),
        Flag('is_fateful'),
    )),
    ULInt8('nature'),
    Flag('has_dwability'),
    Padding(5),
)

_blockC = Struct('_blockC',
    NicknameAdapter(StrictRepeater(11, ULInt16('nickname'))),
    Padding(1),
    ULInt8('hometown'),
    BitStruct('sinnoh_ribbons_set31',
        Flag('beauty_master'),
        Flag('beauty_ultra'),
        Flag('beauty_great'),
        Flag('beauty'),
        Flag('cool_master'),
        Flag('cool_ultra'),
        Flag('cool_great'),
        Flag('cool'),
    ),
    BitStruct('sinnoh_ribbons_set32',
        Flag('smart_master'),
        Flag('smart_ultra'),
        Flag('smart_great'),
        Flag('smart'),
        Flag('cute_master'),
        Flag('cute_ultra'),
        Flag('cute_great'),
        Flag('cute'),
    ),
    BitStruct('sinnoh_ribbons_set41',
        Padding(4),
        Flag('tough_master'),
        Flag('tough_ultra'),
        Flag('tough_great'),
        Flag('tough'),
    ),
    Padding(5),
)

_blockD = Struct('_blockD',
    OTNameAdapter(StrictRepeater(8, ULInt16('ot_name'))),
    Struct('egg_date',
        ULInt8('year'), # minus 2000
        ULInt8('month'),
        ULInt8('day'),
    ),
    Struct('met_date',
        ULInt8('year'), # minus 2000
        ULInt8('month'),
        ULInt8('day'),
    ),
    ULInt16('egg_location'),
    ULInt16('met_location'),
    ULInt8('pokerus'), # needs additional calculations
    ULInt8('ball'),
    Embed(BitStruct('x84',
        Flag('ot_is_female'),
        BitField('met_level', 7),
    )),
    ULInt8('encounter_type'),
    Padding(2),
)

# Battle data
_blockE = Struct('_blockE',
    BitStruct('status',
        Flag('toxic'),
        Flag('paralyzed'),
        Flag('frozen'),
        Flag('burned'),
        Flag('poisoned'),
        BitField('asleep_rounds', 3),
    ),
    Byte('x89'),
    Padding(2),
    ULInt8('level'),
    ULInt8('capsule_index'),
    Struct('stats',
        ULInt16('current_hp'),
        ULInt16('max_hp'),
        ULInt16('attack'),
        ULInt16('defense'),
        ULInt16('speed'),
        ULInt16('spattack'),
        ULInt16('spdefense'),
    ),
    Bytes('trash_data', 56),
    Padding(8)
)

pkm_struct = Struct('pkm_struct',
    Embed(_block0),
    Embed(_blockA),
    Embed(_blockB),
    Embed(_blockC),
    Embed(_blockD),
)

pkm_party_struct = Struct('pkm_party_struct',
    Embed(pkm_struct),
    Embed(_blockE),
)