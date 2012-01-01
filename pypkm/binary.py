# coding=utf-8

"Binary data manipulation."

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import os
import struct
import sqlite3
from math import floor
from pypkm.sqlite import get_cursor

class BinaryFile(object):
    """Core binary editing functionality.

    This class is a wrapper for generic file manipulation including getting,
    setting, creating, and saving files. Knowledge of the file's structure
    is required.
    """

    # Path to the loaded file.
    file_load_path = ''
    
    # Path to the save file.
    file_save_path = ''

    # File type
    file_type = ''

    # File subtype
    file_subtype = ''

    # Edit history
    #
    # Note: I might not want to implement this completely due to a possible
    # memory issue if there are too many changes in a single session. If
    # that's the case, then just save the last revision in here.
    file_history = []

    def get_data(self):
        "Retrieve the current working data."

        return self.file_history[-1]
    
    def add_data(self, data):
        """Add a node of current working data.
        
        Keyword arguments:
        data (string) -- the data to add to work history
        """

        self.file_history.append(data)
    
    def get_filetype(self):
        "Retrieve the file's filetype."

        return self.file_type
    
    def set_filetype(self, type_):
        """Set the file's filetype.

        Keyword arguments:
        type (string) -- the file's type (normally capitalized)
        """

        self.file_type = type_
    
    def get_file_subtype(self):
        "Retrieve the file's subtype."

        return self.file_subtype
    
    def set_file_subtype(self, subtype):
        """Set the file's subtype.

        Keyword arguments:
        subtype (string or int) -- the file's subtype; distinguish between
            certain kinds files within the filetype
        """

        self.file_subtype = subtype
    
    def get(self, fmt, offset, data=None):
        """Retrieve a specific section.

        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        data (string) -- optional data to use instead of history
        """

        # Let them supply their own file data!
        if data is None:
            data = self.get_data()
        
        # Assert little-endian or the system might make longs eight bytes
        fmt = '<' + fmt
        size = struct.calcsize(fmt)
        unpacked = struct.unpack(fmt, data[offset:offset+size])

        return unpacked[0]
    
    def set(self, fmt, offset, value, data=None):
        """Set a value located at offset.
        
        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        value (mixed) -- the value to inject at the specific offset
        data (string) -- optional data to use instead of history
        """
        
        # Let them supply their own file data!
        if data is None:
            data = self.get_data()
        
        # Assert little-endian or the system might make longs eight bytes
        fmt = '<' + fmt
        size = struct.calcsize(fmt)
        packed = struct.pack(fmt, value)
        
        # Inject our packed data (it's hacky, but seems to do the job!)
        # strings are immutable and I don't want to unpack the entire string
        # so this will have to do. KISS.
        splitleft = data[:offset]
        splitright = data[offset+size:]
        new_data = splitleft + packed + splitright
        
        self.add_data(new_data)
    
    def getset(self, fmt, offset, value, data=None):
        """Retrieve data if value is None; otherwise, set value in data.

        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        value (mixed) -- the value to inject at the specific offset
        data (string) -- optional data to use instead of history
        """
        
        if value is not None:
            return self.set(fmt, offset, value, data)
        
        return self.get(fmt, offset, data)
    
    def new(self, data=''):
        "Create a new file from scratch."

        self.add_data(data)
        
        return self
    
    def load_from_data(self, data):
        """Load a file from binary data.

        Keyword arguments:
        data (string) -- the file's binary data
        """

        self.add_data(data)

        return self
    
    def load_from_path(self, path):
        """Load a file from the filesystem.

        Keyword arguments:
        path (string) -- path (local or absolute) to the file
        """

        data = open(path).read()
        self.add_data(data)
        self.file_load_path = os.path.abspath(path)

        return self
    
    def load(self, path=None, data=None):
        """Shorthand for loading a file.

        Keyword arguments:
        path (string) -- optional path, supplied if no data
        data (string) -- optional data, supplied if no path
        """

        if path is not None:
            self.load_from_path(path)
        elif data is not None:
            self.load_from_data(data)
        
        return self
    
    def save(self, path=None, data=None):
        """Save the most recent changes.
        
        Keyword arguments:
        path (string) -- the path to the file to save
        data (string) -- optional data to save
        
        This will save changes to either a separate file in the
        file_load_path directory or to a user-supplied path. Make sure, if
        you're supplying a path, to give a path to the file and not just the
        directory.
        """

        if path is None:
            if self.file_save_path != '':
                path = self.file_save_path
            elif self.file_load_path != '':
                filename, fileext = os.path.splitext(self.file_load_path)
                path = filename + '_new' + fileext
            else:
                raise AttributeError('missing path attribute')
                
        
        if data is None:
            data = self.get_data()
        
        with open(path, 'w') as f:
            f.write(data)
        
        return self


class PkmBinaryFile(BinaryFile):
    "Extension of the BinaryFile class for PKM files."

    def __init__(self):
        super(PkmBinaryFile, self).__init__()

        self.set_filetype('PKM')
    
    def get_gen(self):
        "Return the file's generation."

        return self.get_file_subtype()
    
    def set_gen(self, gen):
        """Set the file's generation.

        Keyword arguments:
        gen (int) -- the file's game generation (supports 4 or 5)
        """

        return self.set_file_subtype(subtype=gen)
    
    def is_gen(self, gen):
        """Check if the file's generation matches the one provided.

        gen (int) -- the game generation to check against
        """

        return self.get_gen() == gen
    
    def get_iv(self, mask, shift, data=None):
        """Returns an IV specified by the mask and shift.

        Keyword arguments:
        mask (int) -- mask to apply to the IV word
        shift (int) -- number of bits to shift
        data (string) -- optional data to use instead of history
        """

        iv_word = self.get(fmt='L', offset=0x38, data=data)

        return (iv_word & mask) >> shift
    
    def set_iv(self, mask, shift, value, data=None):
        """Sets an IV using the mask and shift.

        Keyword arguments:
        mask (int) -- mask to apply to the IV word
        shift (int) -- number of bits to shift
        value (int) -- integer to inject into the word
        data (string) -- optional data to use instead of history
        """
        iv_word = self.get(fmt='L', offset=0x38, data=data)
        new_word = (iv_word & ~mask) | (value << shift)

        return self.set('L', 0x38, new_word)
    
    def getset_iv(self, mask, shift, value, data=None):
        """Common logic for getting and setting an IV.

        IVs are stored in 5-bit nibbles in the 4 bytes located at
        offset 0x38 (bits 0 through 29 inclusive).

        Keyword arguments:
        mask (int) -- mask to apply to the IV byte
        shift (int) -- number of bits to shift
        value (int) -- integer to inject into the byte
        data (string) -- optional data to use instead of history
        """

        if value is not None:
            return self.set_iv(mask=mask, shift=shift, value=value)
        
        return self.get_iv(mask=mask, shift=shift)
    
    def get_string(self, offset, length):
        """Retrieve a string from a PKM file.

        Keyword arguments:
        offset (int) -- the byte offset (inclusive)
        length (int) -- the length of the string (not including the
            terminator byte)
        """

        if self.is_gen(4):
            db = get_cursor()

        string = ''
        term_byte = offset + (offset * 2)

        while True:
            ord_ = self.get('H', offset)
            
            # stop the loop at the terminator, wherever it may be
            if offset >= term_byte or ord_ == 0xFFFF:
                break
            
            if self.is_gen(5):
                string += unichr(ord_)
            elif self.is_gen(4):
                query = 'SELECT `character` FROM `charmap` WHERE `id` = ?'
                string += db.execute(query, (ord_,)).fetchone()[0]

            offset += 2
        
        if self.is_gen(4):
            db.close()
        
        return string
    
    def set_string(self, offset, length, value):
        """Set a string in a PKM file.

        Keyword arguments:
        offset (int) -- the byte offset (inclusive)
        length (int) -- the length of the string (not including the
            terminator byte)
        value (string) -- the letters to insert
        """

        if self.is_gen(4):
            db = get_cursor()
        
        count = 1
        term_byte = offset + (offset * 2)

        # loop over the nickname bytes, injecting the nickname then
        # overwriting the remaining bytes
        while offset <= term_byte:
            if count <= len(value):
                letter = value[count-1]
                if self.is_gen(5):
                    word = ord(letter.decode('utf8'))
                elif self.is_gen(4):
                    query = 'SELECT `id` FROM `charmap` WHERE `character` = ?'
                    word = db.execute(query, (letter,)).fetchone()[0]
            else:
                if self.is_gen(4):
                    # in gen 5, the bytes immediately after the last
                    # letter are 0xFF, then everything after that is
                    # 0x00, followed by two 0xFF at 0x5C
                    if (count == len(value) + 1) or (offset == 0x5C):
                        word = 0xFFFF
                    else:
                        word = 0x0000
                elif self.is_gen(4):
                    # in gen 4, everything after the last letter up to
                    # 0x5D is 0xFF
                    word = 0xFFFF
            
            self.set('H', offset, word)
            count += 1
            offset += 2
        
        if self.is_gen(4):
            db.close()
        
        return
    
    def getset_string(self, offset, length, value):
        """Common logic for getting and setting a string.

        Keyword arguments:
        value (string) -- the string to set
        """

        if value is not None:
            return self.set_string(offset, length, value)
        
        return self.get_string(offset, length)
    
    def get_growthrate(self, pokemon_id):
        """Retrieve the growth rate ID of a Pokémon by its National Dex ID.

        Keyword arguments:
        pokemon_id (int) -- the national dex ID of the Pokémon
        """

        db = get_cursor()

        query = 'SELECT `growth_rate_id` FROM `pokemon_growth_rates` WHERE `pokemon_id` = ?'
        growth_id = db.execute(query, (pokemon_id,)).fetchone()[0]

        db.close()

        return growth_id
    
    def get_level(self, pokemon_id, exp):
        """Retrieve the level of a Pokémon by their experience points.

        Keyword arguments:
        pokemon_id (int) -- the national dex ID of the Pokémon
        exp (int) -- the experience points of the Pokémon
        """
        
        growth_id = self.get_growthrate(pokemon_id)

        db = get_cursor()

        # select the level that's closest to the pokemon's exp without going over
        query = 'SELECT `level` FROM `levels` WHERE `growth_rate_id` = ? AND `experience` <= ? ORDER BY `experience` DESC LIMIT 1'
        level = db.execute(query, (growth_id,exp)).fetchone()[0]

        db.close()

        return level
    
    def get_exp(self, pokemon_id, level):
        """Retrieve the experiance points of a Pokémon by their level.

        Keyword arguments:
        pokemon_id (int) -- the national dex ID of the Pokémon
        level (int) -- the level of the Pokémon
        """

        growth_id = self.get_growthrate(pokemon_id)

        db = get_cursor()

        # select the exp using the growth ID and level
        query = 'SELECT `experience` FROM `levels` WHERE `growth_id` = ? AND `level` = ?'
        exp = db.execute(query, (growth_id,level)).fetchone()[0]

        db.close()

        return exp
    
    def get_nature(self, nature_id):
        """Retrieves a set of information about a nature.

        Keyword arguments:
        nature_id (int) -- the ID of the nature (0-24)
        """

        db = get_cursor()

        query = 'SELECT `id`, `name`, `atk`, `def`, `spe`, `spa`, `spd` FROM `natures` WHERE `id` = ?'
        nature = db.execute(query, (nature_id,)).fetchone()

        db.close()

        return nature
    
    def get_basestats(self, pokemon_id, alt_form=0):
        """Retrieve base stats for a Pokémon.

        Keyword arguments:
        pokemon_id (int) -- the national dex ID
        alt_form (int) -- the optional alternate form
        """

        db = get_cursor()

        query = 'SELECT `base_hp`, `base_atk`, `base_def`, `base_spe`, `base_spa`, `base_spd` FROM `pokemon_base_stats` WHERE `pokemon_id` = ? AND `pokemon_form_id` = ?'
        base_stats = db.execute(query, (pokemon_id, alt_form)).fetchone()

        return base_stats
    
    def calcstat(self, iv, ev, base, level, nature_stat):
        """Calculate the battle stat of a Pokémon.

        Note that some stats may be off by one compared to the "official"
        PKM data. I've only found this to be true on a specific FAL2010 Mew
        file, but it's worth mentioning. If you would like to be safe,
        deposit the Pokémon in the Day Care and take it back out to recreate
        the battle data.

        Keyword arguments:
        iv (int) -- IV stat
        ev (int) -- EV stat
        base (int) -- base stat (from lookup table)
        level (int) -- level (1-100)
        nature_stat (float) -- the stat's nature multiplier (set to None if HP)
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
    
    def get_checksumdata(self, data=None):
        """Returns the appropriate slice for calculating the file checksum.

        Keyword arguments:
        data (string) -- optional data to use instead of history
        """
        
        if data is None:
            data = self.get_data()
        
        return data[0x08:0x88]
    
    def get_boxdata(self, data=None):
        "Return the first 136 bytes of PKM data."

        if data is None:
            data = self.get_data()

        return data[0:136]
    
    def new(self, gen):
        """Create the PKM from scratch.

        Keyword arguments:
        gen (int) -- the file's game generation (supports 4 or 5)
        """

        super(PkmBinaryFile, self).new(data='\x00'*136)
        self.set_gen(gen)

        return self
    
    def load(self, gen, path=None, data=None):
        """Load the PKM file either by path or by data.

        Keyword arguments:
        gen (int) -- the file's game generation (supports 4 or 5)
        path (string) -- optional path, supplied if no data
        data (string) -- optional data, supplied if no path
        """

        super(PkmBinaryFile, self).load(path=path, data=data)
        self.set_gen(gen)

        return self