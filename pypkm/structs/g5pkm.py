# coding=utf-8

"""PKM file structure for Generation 5.

All PKM Struct modules should declare a `pkm_struct` variable that is
an instance of construct.Struct.

Note about nickname and ot_name: even though they're encoded as Unicode
this generation, we still have to do some additional logic because
Construct (understandably) doesn't handle Game Freak's insane string
formatting. I may want to use the Const construct for the term byte,
but as of right now I'd rather keep that logic separate.
"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

# I hate doing this, but apparently it's Construct convention
from construct import *

# http://construct.wikispaces.com/bitfields
# used for IVs since they span two bytes
def Swapped(subcon):
    """swaps the bytes of the stream, prior to parsing"""
    return Buffered(subcon,
        encoder = lambda buf: buf[::-1],
        decoder = lambda buf: buf[::-1],
        resizer = lambda length: length
    )

def _check_gender(ctx):
    """Return the appropriate gender.

    Since 'male' is when neither bits are set, we check the others
    first.
    """
    if ctx['is_female']:
        return 'f'
    elif ctx['is_genderless']:
        return 'n'
    
    return 'm'

def _check_date(ctx):
    """Return a formatted date.

    This function just adds 2000 to the year and puts everything in a
    tuple.
    """

    return (ctx['year'] + 2000, ctx['month'], ctx['day'])

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
    ULInt16('exp'),
    ULInt8('happiness'),
    ULInt8('ability'),
    BitStruct('markings',
        Flag('circle'),
        Flag('triangle'),
        Flag('square'),
        Flag('heart'),
        Flag('star'),
        Flag('diamond'),
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
        Flag('sinnoh_champ'),
        Flag('ability'),
        Flag('great_ability'),
        Flag('double_ability'),
        Flag('multi_ability'),
        Flag('pair_ability'),
        Flag('world_ability'),
        Flag('alert'),
    ),
    BitStruct('sinnoh_ribbons_set12',
        Flag('shock'),
        Flag('downcast'),
        Flag('careless'),
        Flag('relax'),
        Flag('snooze'),
        Flag('smile'),
        Flag('gorgeous'),
        Flag('royal'),
    ),
    BitStruct('sinnoh_ribbons_set21',
        Flag('gorgeous_royal'),
        Flag('footprint'),
        Flag('record'),
        Flag('history'),
        Flag('legend'),
        Flag('red'),
        Flag('green'),
        Flag('blue'),
    ),
    BitStruct('sinnoh_ribbons_set22',
        Flag('festival'),
        Flag('carnival'),
        Flag('classic'),
        Flag('premiere'),
        Padding(4)
    ),
)

_blockB = Struct('_blockB',
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
    Swapped(BitStruct('ivs',
        BitField('hp', 5),
        BitField('atk', 5),
        BitField('def', 5),
        BitField('spe', 5),
        BitField('spa', 5),
        BitField('spd', 5),
        Flag('is_egg'),
        Flag('is_nicknamed'),
    )),
    BitStruct('hoenn_ribbons_set11',
        Flag('cool'),
        Flag('cool_super'),
        Flag('cool_hyper'),
        Flag('cool_master'),
        Flag('beauty'),
        Flag('beauty_super'),
        Flag('beauty_hyper'),
        Flag('beauty_master'),
    ),
    BitStruct('hoenn_ribbons_set12',
        Flag('cute'),
        Flag('cute_super'),
        Flag('cute_hyper'),
        Flag('cute_master'),
        Flag('smart'),
        Flag('smart_super'),
        Flag('smart_hyper'),
        Flag('smart_master'),
    ),
    BitStruct('hoenn_ribbons_set21',
        Flag('tough'),
        Flag('tough_super'),
        Flag('tough_hyper'),
        Flag('tough_master'),
        Flag('champion'),
        Flag('winning'),
        Flag('victory'),
        Flag('artist'),
    ),
    BitStruct('hoenn_ribbons_set22',
        Flag('effort'),
        Flag('marine'),
        Flag('land'),
        Flag('sky'),
        Flag('country'),
        Flag('national'),
        Flag('earth'),
        Flag('world'),
    ),
    BitStruct('x40',
        Flag('is_fateful'),
        Flag('is_female'),
        Flag('is_genderless'), # if both False, then it's male
        BitField('alt_form_unshifted', 5), # leftshift 3
    ),
    ULInt8('nature'),
    Flag('has_dwability'),
    Padding(5),
)

_blockC = Struct('_blockC',
    StrictRepeater(11, ULInt16('nickname')),
    Padding(1),
    ULInt8('hometown'),
    BitStruct('sinnoh_ribbons_set31',
        Flag('cool'),
        Flag('cool_great'),
        Flag('cool_ultra'),
        Flag('cool_master'),
        Flag('beauty'),
        Flag('beauty_great'),
        Flag('beauty_ultra'),
        Flag('beauty_master'),
    ),
    BitStruct('sinnoh_ribbons_set32',
        Flag('cute'),
        Flag('cute_great'),
        Flag('cute_ultra'),
        Flag('cute_master'),
        Flag('smart'),
        Flag('smart_great'),
        Flag('smart_ultra'),
        Flag('smart_master'),
    ),
    BitStruct('sinnoh_ribbons_set41',
        Flag('tough'),
        Flag('tough_great'),
        Flag('tough_ultra'),
        Flag('tough_master'),
        Padding(4),
    ),
    Padding(1),
)

_blockD = Struct('_blockD',
    StrictRepeater(8, ULInt16('ot_name')),
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
    BitStruct('x84',
        BitField('met_level', 7),
        Flag('ot_is_female'),
    ),
    ULInt8('encounter_type'),
    Padding(2),
)

# Battle data
_blockE = Struct('_blockE',
    BitStruct('status',
        BitField('asleep_rounds', 3),
        Flag('poisoned'),
        Flag('burned'),
        Flag('frozen'),
        Flag('paralyzed'),
        Flag('toxic'),
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

pkm_struct = Struct(
    Embed(_block0),
    Embed(_blockA),
    Embed(_blockB),
    Embed(_blockC),
    Embed(_blockD),
)

pkm_party_struct = Struct(
    Embed(pkm_struct),
    Embed(_blockE),
)