# coding=utf-8

import os
import struct

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
    
    def new(self):
        "Create a new file from scratch."

        self.add_data('')
        
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
        self.file_load_path = path

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
            if self.file_save_path == '':
                path = self.file_load_path
            else:
                filename, fileext = os.path.splitext(self.file_load_path)
                path = filename + '_new' + fileext
        
        if data is not None:
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
    
    def checksum_data(self, data=None):
        """Returns the appropriate slice for calculating the file checksum.

        Keyword arguments:
        data (string) -- optional data to use instead of history
        """
        
        if data is None:
            data = self.get_data()
        
        return data[0x08:0x88]
    
    def new(self, gen):
        """Create the PKM from scratch.

        Keyword arguments:
        gen (int) -- the file's game generation (supports 4 or 5)
        """

        super(PkmBinaryFile, self).new()
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