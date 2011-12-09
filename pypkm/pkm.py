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

import random
import struct
from array import array

import rng
from bitutils import setbit, getbit, clearbit, checksum, shuffle

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
    
    # Path to the loaded file.
    _file_load_path = ''
    
    # Path to the save file.
    _file_save_path = ''
    
    # Data of the loaded file.
    #
    # Subsequent changes should be stored in the file_edit_history list.
    _file_load_data = ''
    
    # Edit history list to undo/redo changes.
    # 
    # Note: I might not want to implement this due to a possible memory issue
    # if there are too many changes in a single session. If that's the case,
    # then just save the last revision in here.
    _file_edit_history = []
    
    def _encrypt(self):
        """Encrypt the loaded PKM data.
        """
        pass
    
    def _decrypt(self):
        """Decrypt the loaded PKM data.
        """
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
        
        return getattr(self, '_' + name)()
    
    def __setattr__(self, name, value):
        "Attempt to map any calls to missing attributes to functions."
        
        return getattr(self, '_' + name)(self, value)
    
    def new(self, path=None, generation):
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
        
        Note: if you load raw data, you must supply a path if you decide to
        call save().
        """
        pass
    
    def load_from_path(self, path, generation):
        """Load a PKM file from raw data to be edited.
        
        Keyword arguments:
        path (string) -- the path to the file to load
        generation (int) -- the file's game generation (4 or 5)
        
        Note: refer to save()'s documentation for what happens when you load
        from a path and save.
        """
        pass
    
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
        pass