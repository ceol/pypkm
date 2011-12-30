# coding=utf-8

"""Linear congruent random number generators.

This is a type of pseudo-random number generator used to create
personality values (PVs or PIDs) and individual values (IVs). It is defined
as a recursive function in the following form:

    X[n+1] = ((a * X[n]) + c) % m

where 

`a` is the multiplier
`c` is the increment
`m` is the modulus
`X[n]` is the seed

The product of the function is used as the seed of the next call to the
function. In the Pokémon games, the modulus isn't used, being replaced by an
AND mask to force the number to the last 32 (or 64) bits. The other
modification to the function is the addition of a right shift to the created
seed on return but not when the created seed replaces the old seed.
"""

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

class Rng(object):
    """Base class for the linear congruent random number generator.
    
    I may refer to this class as the `RNG`, the `LC RNG`, or the `LCRNG`
    throughout documentation. All of these mean the same thing: this
    pseudo-random number generator.
    """
    
    # Store every iteration of the LC RNG.
    frames = []
    
    seed = 0
    
    # Variables for the LC RNG. They may change depending on what child RNG
    # class is being used.
    mult = 0
    add = 0
    mask = 0xFFFFFFFF
    width = 0x10
    
    def __init__(self):
        pass
    
    def _advance(self):
        "Calculate the next LC RNG step."
        
        self.seed *= self.mult
        self.seed &= self.mask
        self.seed += self.add
        self.seed &= self.mask
        
        return self.seed >> self.WIDTH
    
    def advance(self, steps=1):
        "Advance the LC RNG the specified number of steps."
        
        for i in range(steps):
            self.frames.append(self._advance())
        
        return self.frames.pop()
    
    def _reverse(self):
        "Calculate the previous LC RNG step."
        pass
    
    def reverse(self, steps):
        "Reverse the LC RNG the specified number of steps."
        pass

class Prng(Rng):
    """Widely-used extension of the base LC RNG.
    
    This class is used in the creation of Pokémon PVs and IVs. There are
    various ways this class is called, such as the `A-B-C-D` form, where a
    Pokémon's PV is created from four successive calls to the PRNG.
    """
    
    def __init__(self, seed=0):
        super(Prng, self).__init__()

        self.seed = seed
        self.mult = 0x41C64E6D
        self.add = 0x6073

class Arng(Rng):
    """Rarely-used extension of the base LC RNG.
    
    As the title says, this extension of the LC RNG is rarely used. I believe
    it's only called when a Mystery Gift Pokémon is shiny in order to force
    it back to normal color. Kept in for posterity.
    """
    
    def __init__(self, seed=0):
        super(Arng, self).__init__()

        self.seed = seed
        self.mult = 0x6C078965
        self.add = 0x1

class Grng(Rng):
    """Extension of the LC RNG used in GTS encryption and decryption.

    This LC RNG is seeded with the checksum and 
    """

    def __init__(self, seed=0):
        super(Grng, self).__init__()

        self.seed = seed | (seed << 16)
        self.mult = 0x45
        self.add = 0x1111
        self.mask = 0x7FFFFFFF
    
    def _advance(self):
        return (super(Grng, self)._advance()) & 0xFF

class Mtrng(Rng):
    """Mersenne Twister wrapper.
    
    Under some circumstances, a Pokémon game may use a Mersenne Twister
    pseudo-random number generator. One such circumstance is when an egg's PV
    is created.
    """
    
    def __init__(self, seed=0):
        random.seed(seed)
    
    def _advance(self):
        return random.randint(0x00, self.mask)