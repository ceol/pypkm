# coding=utf-8

"Binary data manipulation."

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import os
import struct
import sqlite3
from math import floor
from pypkm.sqlite import get_cursor
from pypkm.utils import getbit, setbit, clearbit

class BinaryFile(object):
    """Core binary editing functionality.

    This class is a wrapper for generic file manipulation including
    getting, setting, creating, and saving files. Knowledge of the
    file's structure is required.
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
    # Note: I might not want to implement this completely due to a
    # possible memory issue if there are too many changes in a single
    # session. If that's the case, then just save the last revision in
    # here.
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
        subtype (string or int) -- the file's subtype; distinguish
            between certain kinds files within the filetype
        """

        self.file_subtype = subtype
    
    def get(self, fmt, offset):
        """Retrieve a specific section.

        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        data (string) -- optional data to use instead of history
        """

        data = self.get_data()
        
        # Assert little-endian or the system might make longs eight
        # bytes
        fmt = '<' + fmt
        size = struct.calcsize(fmt)
        unpacked = struct.unpack(fmt, data[offset:offset+size])

        return unpacked[0]
    
    def set(self, fmt, offset, value):
        """Set a value located at offset.
        
        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        value (mixed) -- the value to inject at the specific offset
        data (string) -- optional data to use instead of history
        """
        
        data = self.get_data()
        
        # Assert little-endian or the system might make longs eight
        # bytes
        fmt = '<' + fmt
        size = struct.calcsize(fmt)
        packed = struct.pack(fmt, value)
        
        # Inject our packed data (it's hacky, but seems to do the job!)
        # strings are immutable and I don't want to unpack the entire
        # string so this will have to do. KISS.
        splitleft = data[:offset]
        splitright = data[offset+size:]
        new_data = splitleft + packed + splitright
        
        self.add_data(new_data)
    
    def getset(self, fmt, offset, value):
        """Retrieve data if value is None; otherwise, set value.

        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        value (mixed) -- the value to inject at the specific offset
        """
        
        if value is not None:
            return self.set(fmt, offset, value)
        
        return self.get(fmt, offset)
    
    def new(self, data=''):
        """Create a new file from scratch.

        Keyword arguments:
        data (string) -- the binary data template
        """

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
    
    def save(self, path=None):
        """Save the most recent changes.
        
        This will save changes to either a separate file in the
        file_load_path directory or to a user-supplied path. Make sure,
        if you're supplying a path, to give a path to the file and not
        just the directory.

        Keyword arguments:
        path (string) -- the path to the file to save
        """

        if path is None:
            if self.file_save_path != '':
                path = self.file_save_path
            elif self.file_load_path != '':
                filename, fileext = os.path.splitext(self.file_load_path)
                path = filename + '_new' + fileext
            else:
                raise AttributeError('missing path attribute')
                
        
        data = self.get_data()
        
        with open(path, 'w') as f:
            f.write(data)
        
        return self

class PkmBinaryFile(BinaryFile):
    "Extension of the BinaryFile class for PKM files."
    
    def __init__(self):
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
    
    def get_bitflag(self, fmt, offset, bit):
        """Return a boolean value stored in a bit.

        Keyword arguments:
        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        bit (int) -- the bit offset (inclusive)
        """

        byte = self.get(fmt=fmt, offset=offset)
        return bool(getbit(byte, bit))
    
    def set_bitflag(self, fmt, offset, bit, value):
        """Set a boolean flag stored in a bit.

        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        bit (int) -- the bit offset (inclusive)
        value (bool) -- the flag
        """

        byte = self.bin.get(fmt=fmt, offset=offset)
        if bool(value):
            byte = setbit(byte, bit)
        else:
            byte = clearbit(byte, bit)
        self.set(fmt=fmt, offset=offset, value=byte)
    
    def getset_bitflag(self, fmt, offset, bit, value=None):
        """Common logic for getting and setting a bitflag.

        fmt (string) -- a struct format string
        offset (int) -- the byte offset (inclusive)
        bit (int) -- the bit offset (inclusive)
        value (bool) -- (optional) the flag
        """

        if value is not None:
            return self.set_bitflag(fmt=fmt, offset=offset, bit=bit,
                                    value=value)
        
        return self.get_bitflag(fmt=fmt, offset=offset, bit=bit, value=value)

class Gen4BinaryFile(PkmBinaryFile):
    "Extension of the PkmBinaryFile class for Gen 4 files."

    def __init__(self):
        super(Gen4BinaryFile, self).__init__()
        self.set_gen(4)
    
    def get_iv(self, mask, shift):
        """Return an IV specified by the mask and shift.

        Keyword arguments:
        mask (int) -- mask to apply to the IV word
        shift (int) -- number of bits to shift
        data (string) -- optional data to use instead of history
        """

        iv_word = self.get(fmt='L', offset=0x38)

        return (iv_word & mask) >> shift
    
    def set_iv(self, mask, shift, value):
        """Sets an IV using the mask and shift.

        Keyword arguments:
        mask (int) -- mask to apply to the IV word
        shift (int) -- number of bits to shift
        value (int) -- integer to inject into the word
        data (string) -- optional data to use instead of history
        """
        iv_word = self.get(fmt='L', offset=0x38)
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

        db = get_cursor()

        string = []
        term_byte = offset + (length * 2)

        while True:
            ord_ = self.get('H', offset)
            
            # stop the loop at the terminator, wherever it may be
            if offset >= term_byte or ord_ == 0xFFFF:
                break
            
            query = 'SELECT `character` FROM `charmap` WHERE `id` = ?'
            string.append(db.execute(query, (ord_,)).fetchone()[0])

            offset += 2
        
        db.close()
        
        return ''.join(string)
    
    def set_string(self, offset, length, value):
        """Set a string in a PKM file.

        Keyword arguments:
        offset (int) -- the byte offset (inclusive)
        length (int) -- the length of the string (not including the
            terminator byte)
        value (string) -- the letters to insert
        """

        db = get_cursor()
        
        count = 1
        term_byte = offset + (length * 2)

        # loop over the nickname bytes, injecting the nickname then
        # overwriting the remaining bytes
        while offset <= term_byte:
            if count <= len(value):
                letter = value[count-1]
                query = 'SELECT `id` FROM `charmap` WHERE `character` = ?'
                word = db.execute(query, (letter,)).fetchone()[0]
            else:
                # in gen 4, everything after the last letter up to
                # 0x5D is 0xFF
                word = 0xFFFF
            
            self.set('H', offset, word)
            count += 1
            offset += 2
        
        db.close()
    
    def getset_string(self, offset, length, value):
        """Common logic for getting and setting a string.

        Keyword arguments:
        offset (int) -- the byte offset (inclusive)
        length (int) -- the length of the string (not including the
            terminator byte)
        value (string) -- the letters to insert
        """

        if value is not None:
            return self.set_string(offset, length, value)
        
        return self.get_string(offset, length)
    
    def get_checksumdata(self):
        """Returns appropriate slice for calculating the file checksum."""
        
        return self.get_data()[0x08:0x88]
    
    def get_boxdata(self):
        """Return the first 136 bytes of PKM data."""

        return self.get_data()[:136]
    
    def get_cryptdata(self):
        "Return the part of PKM data to be encrypted/decrypted."

        return self.get_data()[8:136]
    
    def new(self):
        """Create the PKM from scratch.

        Keyword arguments:
        gen (int) -- the file's game generation (supports 4 or 5)
        """

        super(Gen4BinaryFile, self).new(data='\x00'*136)

        return self
    
    def togen5(self):
        "Convert a generation 4 file to generation 5."
        
        bin5 = load_handler(gen=5).load(data=self.get_boxdata())

        # nickname
        nick = self.get_string(offset=0x48, length=10)
        bin5.set_string(offset=0x48, length=10, value=nick)

        # trainer name
        otname = self.get_string(offset=0x68, length=7)
        bin5.set_string(offset=0x68, length=7, value=otname)

        # nature gets its own byte in gen 5
        nature = self.get('B', 0x00) % 25
        bin5.set('B', 0x41, nature)

        # egg location
        if self.get('H', 0x7E) != 0:
            bin5.set('H', 0x7E, 2) # set to Faraway Place
        
        # met location
        if self.get('H', 0x80) != 0:
            bin5.set('H', 0x7E, 2) # set to Faraway Place
        
        # zero out some unused values
        bin5.set('B', 0x86, 0)
        bin5.set('B', 0x43, 0)
        bin5.set('H', 0x44, 0)
        bin5.set('H', 0x46, 0)

        return bin5.get_data()

class Gen5BinaryFile(Gen4BinaryFile):
    "Extension of the PkmBinaryFile class for Gen 5 files."

    def __init__(self):
        super(Gen5BinaryFile, self).__init__()
        self.set_gen(5)
    
    def get_string(self, offset, length):
        """Retrieve a string from a PKM file.

        Keyword arguments:
        offset (int) -- the byte offset (inclusive)
        length (int) -- the length of the string (not including the
            terminator byte)
        """

        string = []
        term_byte = offset + (length * 2)

        while True:
            ord_ = self.get('H', offset)
            
            # stop the loop at the terminator, wherever it may be
            if offset >= term_byte or ord_ == 0xFFFF:
                break
            
            string.append(unichr(ord_))

            offset += 2
        
        return ''.join(string)
    
    def set_string(self, offset, length, value):
        """Set a string in a PKM file.

        Keyword arguments:
        offset (int) -- the byte offset (inclusive)
        length (int) -- the length of the string (not including the
            terminator byte)
        value (string) -- the letters to insert
        """

        count = 1
        term_byte = offset + (length * 2)

        # loop over the nickname bytes, injecting the nickname then
        # overwriting the remaining bytes
        while offset <= term_byte:
            if count <= len(value):
                letter = value[count-1]
                word = ord(letter.decode('utf8'))
            else:
                # in gen 5, the bytes immediately after the last
                # letter are 0xFF, then everything after that is
                # 0x00, followed by two 0xFF at 0x5C
                if (count == len(value) + 1) or (offset == 0x5C):
                    word = 0xFFFF
                else:
                    word = 0x0000
            
            self.set('H', offset, word)
            count += 1
            offset += 2

def load_handler(gen):
    if gen == 5:
        return Gen5BinaryFile()
    elif gen == 4:
        return Gen4BinaryFile()