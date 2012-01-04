# coding=utf-8

# @see http://adam.gomaa.us/blog/2008/aug/11/the-python-property-builtin/
def auto_property(func):
    return property(**func())

def getset_property(func):
    """Return a property instance aimed at editing PKM binary data.

    Functions wishing to utilize this decorator should return a tuple
    of the struct format and the offset byte. For example:

        @getset_property
        def my_attribute(self):
            return ('B', 0x04)
    
    my_attribute would enable editing the single byte located at 0x04.
    """
    
    def fget(self):
        fmt, offset = func(self)
        return self.bin.get(fmt=fmt, offset=offset)
    
    def fset(self, value):
        fmt, offset = func(self)
        self.bin.set(fmt=fmt, offset=offset, value=value)
    
    def fdel(self):
        fmt, offset = func(self)
        self.bin.set(fmt=fmt, offset=offset, value=0)
    
    return property(fget, fset, fdel)