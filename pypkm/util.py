from construct import Buffered

# http://construct.wikispaces.com/bitfields
# used for IVs (and maybe ribbon sets) since they span two bytes
def Swapped(subcon):
    """swaps the bytes of the stream, prior to parsing"""
    return Buffered(subcon,
        encoder = lambda buf: buf[::-1],
        decoder = lambda buf: buf[::-1],
        resizer = lambda length: length
    )

# http://code.activestate.com/recipes/466341-guaranteed-conversion-to-unicode-or-byte-string/
def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

def calcstat(self, iv, ev, base, level, nature_stat):
    """Calculate the battle stat of a Pokémon.

    Note that some stats may be off by one compared to the
    "official" PKM data. I've only found this to be true on a
    specific FAL2010 Mew file, but it's worth mentioning. If you
    would like to be safe, deposit the Pokémon in the Day Care and
    take it back out to recreate the party data.

    Keyword arguments:
    iv (int) -- IV stat
    ev (int) -- EV stat
    base (int) -- base stat (from lookup table)
    level (int) -- level (1-100)
    nature_stat (float) -- the stat's nature multiplier (set to
        None if HP)
    """

    # if hp
    if nature_stat is None:
        num = (iv + (2 * base) + (ev / 4.0) + 100) * level
        denom = 100
        stat = (num / denom) + 10

        return int(floor(stat))
    else:
        num = (iv + (2 * base) + (ev / 4.0)) * level
        denom = 100
        stat = (num / denom) + 5

        return int(floor(floor(stat) * nature_stat))