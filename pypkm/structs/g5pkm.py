# coding=utf-8

"""PKM file structure for Generation 5.

All PKM Struct modules should declare a `pkm_struct` variable that is
an instance of construct.Struct.

Note about BitStructs: it appears Construct has some odd formatting, so
the bit order is reversed when declaring BitStructs. This should be
noticeable for ribbons.

Note about nickname and ot_name: even though they're encoded as Unicode
this generation, we still have to do some additional logic because
Construct (understandably) doesn't handle Game Freak's insane string
formatting. I may want to use the Const construct for the term byte,
but as of right now I'd rather keep that logic separate.
"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

# I hate doing this, but apparently it's Construct convention
from construct import *
from pypkm.util import Swapped
from pypkm.sqlite import get_chr, get_ord

class PkmStringAdapter(Adapter):
    def _encode(self, obj, ctx):
        s = []
        for chr_ in obj:
            s.append(ord(chr_))
        
        return s
    
    def _decode(self, obj, ctx):
        s = []
        for ord_ in obj:
            s.append(unichr(ord_))
        
        return ''.join(s)

_block0 = Struct('_block0',
    ULInt32('pv'),
    Padding(2),
    ULInt16('checksum'),
)

_blockA = Struct('_blockA',
    ULInt16('dex'),
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
        ULInt8('atk'),
        ULInt8('def'),
        ULInt8('spe'),
        ULInt8('spa'),
        ULInt8('spd'),
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
            BitField('spd', 5),
            BitField('spa', 5),
            BitField('spe', 5),
            BitField('def', 5),
            BitField('atk', 5),
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
    StrictRepeater(11, ULInt16('nickname')),
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
    StrictRepeater(8, ULInt16('ot_name')), # needs additional logic
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
        ULInt16('atk'),
        ULInt16('def'),
        ULInt16('spe'),
        ULInt16('spa'),
        ULInt16('spd'),
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