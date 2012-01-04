from pypkm.decorators import auto_property, getset_property

class Gen3AttrMapper(object):
    def __init__(self, bin_):
        self.bin = bin_

class Gen4AttrMapper(object):
    def __init__(self, bin_):
        self.bin = bin_
    
    @getset_property
    def pv(self):
        return ('L', 0x00)

class Gen5AttrMapper(Gen4AttrMapper):
    def __init__(self, bin_):
        self.bin = bin_

def load_mapper(bin_):
    "Return an instance of the appropriate attribute mapper."

    gen = bin_.get_gen()
    if gen == 5:
        return Gen5AttrMapper(bin_=bin_)
    elif gen == 4:
        return Gen4AttrMapper(bin_=bin_)
    elif gen == 3:
        return Gen3AttrMapper(bin_=bin_)