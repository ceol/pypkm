# coding=utf-8

"""PyPKM: Easy PKM file manipulation.

This utility serves as a friendly way to create, edit, encrypt, decrypt, and
convert PKM files. Its goal is to faciliate the creation of more end-user
tools and allow developers to work with PKM files.

Example usage:
    >>> from pypkm.pkm import Pkm
    >>> pkm = Pkm.load_from_path('gengar.pkm', generation=5)
    >>> pkm.moves
    [95, 138, 506, 171]
    >>> pkm.level = 100
    >>> pkm.save()
    gengar_new.pkm
    >>> pkm.level = 50
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

import os # filename functions
import struct  # getting/setting data
import sqlite3 # creating battle data and gen 4 text encoding
from pypkm.util import setbit, getbit, clearbit # setting/getting certain flags

# Encryption/decryption functions
#from array import array
#import pypkm.rng as rng
from pypkm.util import checksum#, shuffle

class PkmCore(object):
    """Core PKM file data manipulation functions.
    
    The plan for data manipulation is to unpack the part that needs to be
    edited, insert the new value, and pack the file back up each time. Since
    the files are extremely small, the overhead should not be much greater
    than unpacking the entire file, doing all the editing, and then packing
    it back up once finished. This also allows the user to edit files without
    loading them beforehand.
    """
    
    # File generation (4 or 5)
    _file_generation = None
    
    # Path to the loaded file.
    _file_load_path = ''
    
    # Path to the save file.
    _file_save_path = ''
    
    # Edit history list to undo/redo changes.
    # 
    # Note: I might not want to implement this completely due to a possible
    # memory issue if there are too many changes in a single session. If
    # that's the case, then just save the last revision in here.
    _file_edit_history = []
    
    def _getdata(self):
        "Retrieve the current working data."
        
        return self._file_edit_history[-1]
    
    def _adddata(self, data):
        """Add a node of current working data.
        
        Keyword arguments:
        data (string) -- the data to add to work history
        """
        
        self._file_edit_history.append(data)
    
    def _getgen(self):
        "Retrieve the current working generation."
        
        return self._file_generation
    
    def _setgen(self, generation):
        """Set the current working generation.
        
        Keyword arguments:
        generation (int) -- the file's game generation (4 or 5)
        """
        
        self._file_generation = generation
    
    def _pack(self):
        "Pack a specific section of PKM byte data."
        pass
    
    def _unpack(self):
        "Unpack a specific section of PKM byte data."
        pass
    
    def _get(self, fmt, offset, data=None):
        """Retrieve byte data located at offset.
        
        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        data (string) -- optional data to use instead of history
        """
        
        # Let them supply their own file data!
        if data is None:
            data = self._getdata()
        
        # Assert little-endian or the system might make longs eight bytes
        fmt = '<' + fmt
        
        size = struct.calcsize(fmt)
        unpacked = struct.unpack(fmt, data[offset:offset+size])
        
        return unpacked[0]
    
    def _set(self, fmt, offset, value, data=None):
        """Set a value located at offset.
        
        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        value (mixed) -- the value to inject at the specific offset
        data (string) -- optional data to use instead of history
        """
        
        # Let them supply their own file data!
        if data is None:
            data = self._getdata()
        
        # Assert little-endian or the system might make longs eight bytes
        fmt = '<' + fmt
        
        size = struct.calcsize(fmt)
        packed = struct.pack(fmt, value)
        
        # Inject our packed data (it's hacky, but seems to do the job!)
        # strings are immutable and I don't want to unpack the entire string
        # so this will have to do. KISS.
        split1 = data[:offset]
        split2 = data[offset+size:]
        new_data = split1+packed+split2
        
        self._adddata(new_data)
        
        return self._getdata()
    
    def _getset(self, attr, fmt, offset, value, data=None):
        """Common attribute get/set logic.

        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        value (mixed) -- the value to inject at the specific offset
        data (string) -- optional data to use instead of history
        """
        
        if value is not None:
            self._set(fmt, offset, value, data)
            
            return getattr(self, attr)
        
        return self._get(fmt, offset, data)
    
    def _getiv(self, mask, shift):
        "Returns an IV depending on the mask and shift."

        return (self._get('L', 0x38) & mask) >> shift
    
    def _setiv(self, mask, shift, value):
        "Sets an IV depending on the mask and shift."

        new_word = (self._get('L', 0x38) & ~mask) | (value << shift)

        return self._set('L', 0x38, new_word)
    
    def _getsetiv(self, attr, mask, shift, value):
        "Common logic for getting and setting an IV."

        if value is not None:
            self._setiv(mask=mask, shift=shift, value=value)

            return getattr(self, attr)
        
        return self._getiv(mask=mask, shift=shift)
    
    def _checksumdata(self, data=None):
        "Returns the appropriate slice for calculating the checksum."
        
        if data is None:
            data = self._getdata()
        
        return data[0x08:0x88]

class PkmAttr(PkmCore):
    """Functions used to map attribute calls."""
    
    def __getattr__(self, name):
        "Attempt to map any calls to missing attributes to functions."
        
        try:
            func_name = '{}{}'.format('attr__', name)
            return object.__getattribute__(self, func_name)()
        except AttributeError:
            error = "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)
            raise AttributeError(error)
    
    def __setattr__(self, name, value):
        "Attempt to map any calls to missing attributes to functions."
        
        try:
            getattr(self, 'attr__' + name)(value)
        except AttributeError:
            self.__dict__[name] = value
    
    def attr__pv(self, value=None):
        """Personality value.
        
        Note: Do NOT edit this unless you know what you are doing!
        """
        
        return self._getset('pv', fmt='L', offset=0x00, value=value)
            
    def attr__checksum(self, value=None):
        """Checksum.
        
        This should only be edited when the byte data is changed. Use the
        appropriate pypkm.util function to calculate.
        """
        
        return self._getset('checksum', fmt='H', offset=0x06, value=value)
    
    def attr__id(self, value=None):
        "National Pokédex ID."
        
        return self._getset('id', fmt='H', offset=0x08, value=value)
    
    def attr__item(self, value=None):
        "Held item ID."
        
        return self._getset('item', fmt='H', offset=0x0A, value=value)
    
    def attr__ot_id(self, value=None):
        "Original trainer ID."
        
        return self._getset('ot_id', fmt='H', offset=0x0C, value=value)
    
    def attr__ot_secret_id(self, value=None):
        "Original trainer secret ID."
        
        return self._getset('ot_secret_id', fmt='H', offset=0x0E, value=value)
    
    def attr__exp(self, value=None):
        "Experience points total."
        
        return self._getset('exp', fmt='L', offset=0x10, value=value)
    
    def attr__happiness(self, value=None):
        "Happiness (or steps to hatch if an egg)."
        
        return self._getset('happiness', fmt='B', offset=0x14, value=value)
    
    def attr__ability(self, value=None):
        "Ability ID."
        
        return self._getset('ability', fmt='B', offset=0x15, value=value)
    
    def attr__markings(self, value=None):
        "Pokédex markings. (I think?)"
        
        markings = {
            0x01: 'circle',
            0x02: 'triangle',
            0x04: 'square',
            0x08: 'heart',
            0x10: 'star',
            0x20: 'diamond',
        }
    
    def attr__language(self, value=None):
        "Language ID."
        
        # Currently not used in favor of returning the raw value
        #languages = {
        #    0x01: 'jp',
        #    0x02: 'en',
        #    0x03: 'fr',
        #    0x04: 'it',
        #    0x05: 'de',
        #    0x07: 'es',
        #    0x08: 'kr',
        #}
        
        return self._getset('language', fmt='B', offset=0x17, value=value)
    
    def attr__hp_ev(self, value=None):
        "Hit points effort value."
        
        return self._getset('hp_ev', fmt='B', offset=0x18, value=value)
    
    def attr__atk_ev(self, value=None):
        "Attack effort value."
        
        return self._getset('atk_ev', fmt='B', offset=0x19, value=value)
    
    def attr__def_ev(self, value=None):
        "Defense effort value."
        
        return self._getset('def_ev', fmt='B', offset=0x1A, value=value)
    
    def attr__spe_ev(self, value=None):
        "Speed effort value."
        
        return self._getset('spe_ev', fmt='B', offset=0x1B, value=value)
    
    def attr__spa_ev(self, value=None):
        "Special attack effort value."
        
        return self._getset('spa_ev', fmt='B', offset=0x1C, value=value)
    
    def attr__spd_ev(self, value=None):
        "Special defense effort value."
        
        return self._getset('spd_ev', fmt='B', offset=0x1D, value=value)
    
    def attr__cool_cv(self, value=None):
        "Cool contest value."
        
        return self._getset('cool_cv', fmt='B', offset=0x1E, value=value)
    
    def attr__beauty_cv(self, value=None):
        "Beauty contest value."
        
        return self._getset('beauty_cv', fmt='B', offset=0x1F, value=value)
    
    def attr__cute_cv(self, value=None):
        "Cute contest value."
        
        return self._getset('cute_cv', fmt='B', offset=0x20, value=value)
    
    def attr__smart_cv(self, value=None):
        "Smart contest value."
        
        return self._getset('smart_cv', fmt='B', offset=0x21, value=value)
    
    def attr__tough_cv(self, value=None):
        "Tough contest value."
        
        return self._getset('tough_cv', fmt='B', offset=0x22, value=value)
    
    def attr__sheen_cv(self, value=None):
        "Sheen contest value."
        
        return self._getset('sheen_cv', fmt='B', offset=0x23, value=value)
    
    def attr__ribbons(self, value=None):
        "Hoenn and Sinnoh ribbon sets."
        pass
    
    def attr__move1(self, value=None):
        "Move #1 ID."
        
        return self._getset('move1', fmt='H', offset=0x28, value=value)
    
    def attr__move2(self, value=None):
        "Move #2 ID."
        
        return self._getset('move2', fmt='H', offset=0x2A, value=value)
    
    def attr__move3(self, value=None):
        "Move #3 ID."
        
        return self._getset('move3', fmt='H', offset=0x2C, value=value)
    
    def attr__move4(self, value=None):
        "Move #4 ID."
        
        return self._getset('move4', fmt='H', offset=0x2E, value=value)
    
    def attr__move_pp(self, value=None):
        "Current move PP."
        pass
    
    def attr__move_ppup(self, value=None):
        "Move PP-Ups."
        pass
    
    def attr__hp_iv(self, value=None):
        "Hit point individual value."

        return self._getsetiv('hp_iv', mask=0x0000001f, shift=0, value=value)
    
    def attr__atk_iv(self, value=None):
        "Attack individual value."
        
        return self._getsetiv('atk_iv', mask=0x000003e0, shift=5, value=value)
    
    def attr__def_iv(self, value=None):
        "Defense individual value."
        
        return self._getsetiv('def_iv', mask=0x00007c00, shift=10, value=value)
    
    def attr__spe_iv(self, value=None):
        "Speed individual value."
        
        return self._getsetiv('spe_iv', mask=0x000f8000, shift=15, value=value)
    
    def attr__spa_iv(self, value=None):
        "Special attack individual value."
        
        return self._getsetiv('spa_iv', mask=0x01f00000, shift=20, value=value)
    
    def attr__spd_iv(self, value=None):
        "Special defense individual value."
        
        return self._getsetiv('spd_iv', mask=0x3e000000, shift=25, value=value)
    
    def attr__is_egg(self, value=None):
        "Is egg flag."
        
        egg_byte = self._get('L', 0x38)

        if value is not None:
            if value == True:
                new_byte = setbit(egg_byte, 30)
            elif value == False:
                new_byte = clearbit(egg_byte, 30)
            else:
                raise AttributeError('invalid is_egg value')
            
            self._set('L', 0x38, new_byte)

            return self.is_egg
        
        return getbit(egg_byte, 30) == 1
    
    def attr__is_nicknamed(self, value=None):
        "Is nicknamed flag."

        nick_byte = self._get('L', 0x38)

        if value is not None:
            if value == True:
                new_byte = setbit(nick_byte, 31)
            elif value == False:
                new_byte = clearbit(nick_byte, 31)
            else:
                raise AttributeError('invalid is_nicknamed value')
            
            self._set('L', 0x38, new_byte)

            return self.is_nicknamed
                
        return getbit(nick_byte, 31) == 1

    def attr__is_fateful(self, value=None):
        "Fateful encounter flag."
        
        fate_byte = self._get('B', 0x40)

        if value is not None:
            if value == True:
                new_byte = setbit(fate_byte, 0)
            elif value == False:
                new_byte = clearbit(fate_byte, 0)
            else:
                raise AttributeError('invalid is_fateful value')
            
            self._set('B', 0x40, new_byte)

            return self.is_fateful
        
        return getbit(fate_byte, 0) == 1
    
    def attr__gender(self, value=None):
        "Pokémon gender."
        
        genders = {
            0b11: 'm', # male
            0b01: 'f', # female
            0b10: 'n', # genderless
        }

        gender_byte = self._get('B', 0x40)
        gender_id = (gender_byte & 0x6) >> 1

        if value is not None:
            # @see http://www.daniweb.com/software-development/python/code/217019
            #gender_bits = [key for key, val in genders.iteritems() if val == value][0]

            if value == 'm':
                new_byte = setbit(gender_byte, 1)
                new_byte = setbit(new_byte, 2)
            elif value == 'f':
                new_byte = setbit(gender_byte, 1)
                new_byte = clearbit(new_byte, 2)
            elif value == 'n':
                new_byte = clearbit(gender_byte, 1)
                new_byte = setbit(new_byte, 2)
            else:
                raise ValueError('invalid gender value')

            self._set('B', 0x40, new_byte)
            
            return self.gender
        
        return genders[gender_id]
    
    def attr__shiny_leaves(self, value=None):
        "Shiny leaves. (HG/SS-only)"
        pass
    
    def attr__leaf_crown(self, value=None):
        "Leaf Crown. (HG/SS-only)"
        pass
    
    def attr__egg_location(self, value=None):
        "Location where the egg was received."
        
        return self._getset('egg_location', fmt='H', offset=0x7E, value=value)
    
    def attr__met_location(self, value=None):
        "Location where the Pokémon was met."
        
        return self._getset('met_location', fmt='H', offset=0x80, value=value)
    
    def attr__pt_egg_location(self, value=None):
        "Location where the egg was received. (Platinum-only)"
        
        return self._getset('pt_egg_location', fmt='H', offset=0x44, value=value)
    
    def attr__pt_met_location(self, value=None):
        "Location where the Pokémon was met. (Platinum-only)"
        
        return self._getset('pt_met_location', fmt='H', offset=0x44, value=value)
    
    def attr__nickname(self, value=None):
        "Pokémon nickname."
        pass
    
    def attr__hometown(self, value=None):
        "Pokémon hometown."
        
        return self._getset('hometown', fmt='B', offset=0x5F, value=value)
    
    def attr__ot_name(self, value=None):
        "Original trainer name."
        pass
    
    def attr__egg_date(self, value=None):
        "Date when the egg was received."
        
        date_year = self._get('B', 0x78)
        date_month = self._get('B', 0x79)
        date_day = self._get('B', 0x7A)

        return (date_year+2000, date_month, date_day)
    
    def attr__met_date(self, value=None):
        "Date when the Pokémon was met."
        
        date_year = self._get('B', 0x7B)
        date_month = self._get('B', 0x7C)
        date_day = self._get('B', 0x7D)

        return (date_year+2000, date_month, date_day)
    
    def attr__pokerus(self, value=None):
        """Pokérus.

        @see http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9rus
        """

        return self._getset('pokerus', fmt='B', offset=0x82, value=value)
    
    def attr__has_pokerus(self, value=None):
        "Check if a Pokémon is currently infected with Pokérus."
        
        rus_byte = self.pokerus

        return rus_byte % 16 != 0
    
    def attr__had_pokerus(self, value=None):
        "Check if a Pokémon has had Pokérus."
        
        rus_byte = self.pokerus

        return ((rus_byte % 16 == 0) and (rus_byte != 0))
    
    def attr__ball(self, value=None):
        "Poké Ball ID."
        
        return self._getset('ball', fmt='B', offset=0x83, value=value)
    
    def attr__met_level(self, value=None):
        "Level at which the Pokémon was met."
        
        metlv_byte = self._get('B', 0x84)

        if value is not None:
            new_byte = (metlv_byte & ~0x7f) | value
            self._set('B', 0x84, new_byte)

            return self.met_level
        
        return metlv_byte & 0x7f # first 7 bits
    
    def attr__ot_gender(self, value=None):
        "Original trainer gender."
        
        genders = {
            0: 'm', # male
            1: 'f', # female
        }
        gender_byte = self._get('B', 0x84)

        if value is not None:
            if value == 'm':
                new_byte = clearbit(gender_byte, 7)
            elif value == 'f':
                new_byte = setbit(gender_byte, 7)
            else:
                raise AttributeError('invalid ot_gender value')
            
            self._set('B', 0x84, new_byte)

            return self.ot_gender
        
        gender_id = getbit(gender_byte, 7)

        return genders[gender_id]
    
    def attr__encounter_type(self, value=None):
        "Pokémon encounter type."
        
        return self._getset('encounter_type', fmt='B', offset=0x85, value=value)
    
    def attr__hgss_ball(self, value=None):
        "Secondary Poké Ball ID. (HG/SS-only)"
        
        return self._getset('hgss_ball', fmt='B', offset=0x86, value=value)
    
    def attr__nature(self, value=None):
        "Nature. (B/W-only)"
        
        return self._getset('nature', fmt='B', offset=0x41, value=value)
    
    def attr__dw_ability(self, value=None):
        "Dream World ability flag. (B/W-only)"
        
        return self._getset('dw_ability', fmt='B', offset=0x42, value=value)
    
    def attr__level(self, value=None):
        "Level."
        pass

class Pkm(PkmAttr):
    """User-friendly PKM file manipulation API.
    
    These functions enable a clear and coherent way to edit PKM files instead
    of the developer manipulating raw bytes and dealing with endianness. I'd
    like to organize it similar to an ORM.
    """
    
    def new(self, generation, path=None):
        """Create a blank PKM file to be filled with custom data.
        
        Keyword arguments:
        path (string) -- the path to the file to create (optional)
        generation (int) -- the file's game generation (4 or 5)
        
        If you do not supply a save path here, you must supply one if you
        call save(). Note: there is no need to call the load() function after
        calling new().
        """
        pass
    
    def load_from_data(self, generation, data):
        """Load a PKM file from raw data to be edited.
        
        Keyword arguments:
        data (string) -- the raw file data
        generation (int) -- the file's game generation (4 or 5)
        
        Note: if you load raw data, you must supply a path to the save()
        method.
        """
        
        self._adddata(data)
        self._setgen(generation)
        
        return self
    
    def load_from_path(self, generation, path):
        """Load a PKM file from raw data to be edited.
        
        Keyword arguments:
        path (string) -- the path to the file to load
        generation (int) -- the file's game generation (4 or 5)
        
        Note: refer to save()'s documentation for what happens when you load
        from a path and save.
        """
        
        data = open(path).read()
        
        self._file_load_path = path
        self._adddata(data)
        self._setgen(generation)
        
        return self
    
    def save(self, path=None):
        """Save the most recent changes.
        
        Keyword arguments:
        path (string) -- the path to the file to save
        
        This will save changes to either a separate file in the
        _file_load_path directory or to a user-supplied path. Make sure, if
        you're supplying a path, to give a path to the file and not just the
        directory.
        
        Ex:
            # creates a new pkm file
            pkm = Pkm.new(generation=5)
            
            # saves to current working directory
            pkm.save('gengar.pkm')
            
            # loads the existing pkm file
            pkm = Pkm.load_from_path('gengar.pkm', generation=5)
            
            # saves to a new file in the same directory (./gengar_new.pkm)
            pkm.save()
        """
        
        if path is None:
            if self._file_load_path is None:
                raise AttributeError('invalid save path')
            
            filename, fileext = os.path.splitext(self._file_load_path)
            path = filename + '_new' + fileext
        
        # Make sure the checksum is correct or encryption/decryption
        # functions won't work!
        self.checksum = checksum(self._checksumdata())
        
        data = self._getdata()
        
        with open(path, 'w') as f:
            f.write(data)
        
        return self