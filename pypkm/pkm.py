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

import struct  # getting/setting data
import sqlite3 # creating battle data and gen 4 text encoding
from bitutils import setbit, getbit, clearbit # setting/getting certain flags

# Encryption/decryption functions
#from array import array
#import rng
#from bitutils import checksum, shuffle

class PkmCore(object):
    """Core PKM file manipulation functions.
    
    These functions are more specific to PKM files but will be— for the most
    part— abstracted out in the Pkm class. Because of this, they should not
    be called directly, so I've prefaced each with an underscore to signify
    that.
    
    The plan for file manipulation is to unpack the part that needs to be
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
        
        return self._file_edit_history.pop()
    
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
    
    def _encrypt(self):
        "Encrypt the loaded PKM data."
        pass
    
    def _decrypt(self):
        "Decrypt the loaded PKM data."
        pass

class Pkm(PkmCore):
    """User-friendly PKM file manipulation API.
    
    These functions enable a clear and coherent way to edit PKM files instead
    of the developer manipulating raw bytes and dealing with endianness. I'd
    like to organize it similar to an ORM.
    """
    
    def __init__(self):
        pass
    
    def __getattr__(self, name):
        "Attempt to map any calls to missing attributes to functions."
        
        return object.__getattribute__(self, '_' + name)()
    
    def __setattr__(self, name, value):
        "Attempt to map any calls to missing attributes to functions."
        
        try:
            self.__dict__[name] = value
        except AttributeError:
            new_data = getattr(self, '_' + name)(self, value)
            self._adddata(new_data)
    
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
    
    def load_from_data(self, data, generation):
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
        
        data = self._getdata()
        
        with open(path, 'w') as f:
            f.write(data)
        
        return self
    
    # Attribute functions.
    
    def _pv(self, value=None):
        "Personality value."
        pass
    
    def _checksum(self, value=None):
        "Checksum."
        pass
    
    def _dex(self, value=None):
        "National Pokédex ID."
        
        fmt = 'H'
        offset = 0x08
        
        if value is not None:
            data = self._set(fmt, offset, value)
            
            return self.dex
        
        return self._get(fmt, offset)
    
    def _item(self, value=None):
        "Held item ID."
        pass
    
    def _ot_id(self, value=None):
        "Original trainer ID."
        pass
    
    def _ot_secret_id(self, value=None):
        "Original trainer secret ID."
        pass
    
    def _exp(self, value=None):
        "Experience points total."
        pass
    
    def _happiness(self, value=None):
        "Happiness (or steps to hatch if an egg)."
        pass
    
    def _ability(self, value=None):
        "Ability ID."
        pass
    
    def _markings(self, value=None):
        "Pokédex markings (I think?)."
        
        markings = {
            'circle': 0x01,
            'triangle': 0x02,
            'square': 0x04,
            'heart': 0x08,
            'star': 0x10,
            'diamond': 0x20,
        }
    
    def _language(self, value=None):
        "Language."
        
        languages = {
            'jp': 0x01,
            'en': 0x02,
            'fr': 0x03,
            'it': 0x04,
            'de': 0x05,
            'es': 0x07,
            'kr': 0x08,
        }
    
    def _evs(self, value=None):
        "Effort values."
        pass
    
    def _cvs(self, value=None):
        "Contest values."
        pass
    
    def _ribbons(self, value=None):
        "Hoenn and Sinnoh ribbon sets."
        pass
    
    def _moves(self, value=None):
        "Moveset IDs."
        pass
    
    def _move_pp(self, value=None):
        "Current move PP."
        pass
    
    def _move_ppup(self, value=None):
        "Move PP-Ups."
        pass
    
    def _ivs(self, value=None):
        "Individual values."
        pass
    
    def _fateful_encounter(self, value=None):
        "Fateful encounter flag."
        pass
    
    def _gender(self, value=None):
        "Pokémon gender."
        pass
    
    def _shiny_leaves(self, value=None):
        "Shiny leaves (HG/SS-only)."
        pass
    
    def _leaf_crown(self, value=None):
        "Leaf Crown (HG/SS-only)."
        pass
    
    def _egg_location(self, value=None):
        "Location where the egg was received."
        pass
    
    def _met_location(self, value=None):
        "Location where the Pokémon was met."
        pass
    
    def _nickname(self, value=None):
        "Pokémon nickname."
        pass
    
    def _hometown(self, value=None):
        "Pokémon hometown."
        pass
    
    def _ot_name(self, value=None):
        "Original trainer name."
        pass
    
    def _egg_date(self, value=None):
        "Date when the egg was received."
        pass
    
    def _met_date(self, value=None):
        "Date when the Pokémon was met."
        pass
    
    def _pokerus(self, value=None):
        "Pokérus flag."
        pass
    
    def _pokeball(self, value=None):
        "Poké Ball ID."
        pass
    
    def _met_level(self, value=None):
        "Level at which the Pokémon was met."
        pass
    
    def _ot_gender(self, value=None):
        "Original trainer gender."
        pass
    
    def _encounter_type(self, value=None):
        "Pokémon encounter type."
        pass
    
    def _hgss_pokeball(self, value=None):
        "Poké Ball ID specific to HG/SS."
        pass
    
    def _level(self, value=None):
        "Level."
        pass
    
    def _dw_ability(self, value=None):
        "Dream World ability flag."
        pass
    
    def _nature(self, value=None):
        "Nature (B/W-only)."
        pass