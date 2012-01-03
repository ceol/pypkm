# @see http://adam.gomaa.us/blog/2008/aug/11/the-python-property-builtin/
def Property(func):
    return property(**func())

def CommonProperty(func):
    obj, fmt, offset = func()

    def fget():
        return obj.bin.get(fmt=fmt, offset=offset)
    
    def fset(value):
        obj.bin.set(fmt=fmt, offset=offset, value=value)
    
    def fdel():
        obj.bin.set(fmt=fmt, offset=offset, value=0)
    
    return property(fget, fset, fdel)