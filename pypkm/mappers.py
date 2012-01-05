# coding=utf-8

class Gen4AttrMapper(object):

    def __init__(self, bin_):
        self.bin = bin_
    
    def pv(self, value=None):
        """Personality value
        
        Note: Do NOT edit this unless you know what you are doing!
        """

        return self.bin.getset('L', 0x00, value=value)
            
    def checksum(self, value=None):
        """Checksum
        
        This should only be edited when the byte data is changed. Use
        the appropriate pypkm.utils function to calculate.
        """
        
        return self.bin.getset('H', 0x06, value=value)
    
    def id(self, value=None):
        "National Pokédex ID"
        
        return self.bin.getset('H', 0x08, value=value)
    
    def item(self, value=None):
        "Held item ID"
        
        return self.bin.getset('H', 0x0A, value=value)
    
    def ot_id(self, value=None):
        "Original trainer ID"
        
        return self.bin.getset('H', 0x0C, value=value)
    
    def ot_secret_id(self, value=None):
        "Original trainer secret ID"
        
        return self.bin.getset('H', 0x0E, value=value)
    
    def exp(self, value=None):
        "Experience points total"
        
        return self.bin.getset('L', 0x10, value=value)
    
    def happiness(self, value=None):
        "Happiness (or steps to hatch if an egg)"
        
        return self.bin.getset('B', 0x14, value=value)
    
    def ability(self, value=None):
        "Ability ID"
        
        return self.bin.getset('B', 0x15, value=value)
    
    def markings(self, value=None):
        "PC box markings"
        
        markings = {
            0x01: 'circle',
            0x02: 'triangle',
            0x04: 'square',
            0x08: 'heart',
            0x10: 'star',
            0x20: 'diamond',
        }
    
    def language(self, value=None):
        "Language ID"
        
        #languages = {
        #    0x01: 'jp',
        #    0x02: 'en',
        #    0x03: 'fr',
        #    0x04: 'it',
        #    0x05: 'de',
        #    0x07: 'es',
        #    0x08: 'kr',
        #}

        return self.bin.getset('B', 0x17, value=value)
    
    def hp_ev(self, value=None):
        "Hit points effort value"
        
        return self.bin.getset('B', 0x18, value=value)
    
    def atk_ev(self, value=None):
        "Attack effort value"
        
        return self.bin.getset('B', 0x19, value=value)
    
    def def_ev(self, value=None):
        "Defense effort value"
        
        return self.bin.getset('B', 0x1A, value=value)
    
    def spe_ev(self, value=None):
        "Speed effort value"
        
        return self.bin.getset('B', 0x1B, value=value)
    
    def spa_ev(self, value=None):
        "Special attack effort value"
        
        return self.bin.getset('B', 0x1C, value=value)
    
    def spd_ev(self, value=None):
        "Special defense effort value"
        
        return self.bin.getset('B', 0x1D, value=value)
    
    def cool_cv(self, value=None):
        "Cool contest value"
        
        return self.bin.getset('B', 0x1E, value=value)
    
    def beauty_cv(self, value=None):
        "Beauty contest value"
        
        return self.bin.getset('B', 0x1F, value=value)
    
    def cute_cv(self, value=None):
        "Cute contest value"
        
        return self.bin.getset('B', 0x20, value=value)
    
    def smart_cv(self, value=None):
        "Smart contest value"
        
        return self.bin.getset('B', 0x21, value=value)
    
    def tough_cv(self, value=None):
        "Tough contest value"
        
        return self.bin.getset('B', 0x22, value=value)
    
    def sheen_cv(self, value=None):
        "Sheen contest value"
        
        return self.bin.getset('B', 0x23, value=value)
    
    def ribbons(self, value=None):
        "Hoenn and Sinnoh ribbon sets"
        pass
    
    def move1(self, value=None):
        "Move #1 ID"
        
        return self.bin.getset('H', 0x28, value=value)
    
    def move2(self, value=None):
        "Move #2 ID"
        
        return self.bin.getset('H', 0x2A, value=value)
    
    def move3(self, value=None):
        "Move #3 ID"
        
        return self.bin.getset('H', 0x2C, value=value)
    
    def move4(self, value=None):
        "Move #4 ID"
        
        return self.bin.getset('H', 0x2E, value=value)
    
    def move1_pp(self, value=None):
        "Current move #1 PP"
        
        return self.bin.getset('B', 0x30, value=value)
    
    def move2_pp(self, value=None):
        "Current move #2 PP"
        
        return self.bin.getset('B', 0x31, value=value)
    
    def move3_pp(self, value=None):
        "Current move #3 PP"
        
        return self.bin.getset('B', 0x32, value=value)
    
    def move4_pp(self, value=None):
        "Current move #4 PP"
        
        return self.bin.getset('B', 0x33, value=value)
    
    def move1_ppups(self, value=None):
        "Move #1 PP-Ups"
        
        return self.bin.getset('B', 0x34, value=value)
    
    def move2_ppups(self, value=None):
        "Move #2 PP-Ups"
        
        return self.bin.getset('B', 0x35, value=value)
    
    def move3_ppups(self, value=None):
        "Move #3 PP-Ups"
        
        return self.bin.getset('B', 0x36, value=value)
    
    def move4_ppups(self, value=None):
        "Move #4 PP-Ups"
        
        return self.bin.getset('B', 0x37, value=value)
    
    def hp_iv(self, value=None):
        "Hit point individual value"

        return self.bin.getset_iv(mask=0x0000001f, shift=0, value=value)
    
    def atk_iv(self, value=None):
        "Attack individual value"

        return self.bin.getset_iv(mask=0x000003e0, shift=5, value=value)
    
    def def_iv(self, value=None):
        "Defense individual value"

        return self.bin.getset_iv(mask=0x00007c00, shift=10, value=value)
    
    def spe_iv(self, value=None):
        "Speed individual value"

        return self.bin.getset_iv(mask=0x000f8000, shift=15, value=value)
    
    def spa_iv(self, value=None):
        "Special attack individual value"

        return self.bin.getset_iv(mask=0x01f00000, shift=20, value=value)
    
    def spd_iv(self, value=None):
        "Special defense individual value"

        return self.bin.getset_iv(mask=0x3e000000, shift=25, value=value)
    
    def is_egg(self, value=None):
        "Egg flag"
        
        return self.bin.getset_bitflag('L', 0x38, 30, value=value)
    
    def is_nicknamed(self, value=None):
        "Nicknamed flag"

        return self.bin.getset_bitflag('L', 0x38, 31, value=value)

    def is_fateful(self, value=None):
        "Fateful encounter flag"
        
        return self.bin.getset_bitflag('B', 0x40, 0, value=value)
    
    def gender(self, value=None):
        "Pokémon gender"
        
        genders = {
            0b11: 'm', # male
            0b01: 'f', # female
            0b10: 'n', # genderless
        }

        gender_byte = self.bin.get('B', 0x40)
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

            return self.bin.set('B', 0x40, new_byte)
        
        return genders[gender_id]
    
    def shiny_leaves(self, value=None):
        "Shiny leaves (HG/SS-only)"
        pass
    
    def has_leafcrown(self, value=None):
        "Leaf Crown (HG/SS-only)"
        
        return self.bin.getset_bitflag('B', 0x41, 5, value=value)
    
    def egg_location(self, value=None):
        "Location where the egg was received"
        
        return self.bin.getset('H', 0x7E, value=value)
    
    def met_location(self, value=None):
        "Location where the Pokémon was met"
        
        return self.bin.getset('H', 0x80, value=value)
    
    def pt_egg_location(self, value=None):
        "Location where the egg was received (Platinum-only)"
        
        return self.bin.getset('H', 0x44, value=value)
    
    def pt_met_location(self, value=None):
        "Location where the Pokémon was met (Platinum-only)"
        
        return self.bin.getset('H', 0x44, value=value)
    
    def nickname(self, value=None):
        "Pokémon nickname"

        return self.bin.getset_string(0x48, length=10, value=value)
    
    def hometown(self, value=None):
        "Pokémon hometown"
        
        return self.bin.getset('B', 0x5F, value=value)
    
    def ot_name(self, value=None):
        "Original trainer name"

        return self.bin.getset_string(0x68, length=7, value=value)
    
    def egg_date(self, value=None):
        "Date when the egg was received"

        if value is not None:
            # make sure it's not negative
            if value[0] < 2000:
                value[0] += 2000
            
            self.bin.set('B', 0x78, (value[0]-2000)) # year - 2000
            self.bin.set('B', 0x79, value[1]) # month
            self.bin.set('B', 0x7A, value[2]) # day

            return
        
        date_year = self.bin.get('B', 0x78)
        if date_year > 0:
            date_year += 2000
        date_month = self.bin.get('B', 0x79)
        date_day = self.bin.get('B', 0x7A)

        return (date_year, date_month, date_day)
    
    def met_date(self, value=None):
        "Date when the Pokémon was met"

        if value is not None:
            # make sure it's not negative
            if value[0] < 2000:
                value[0] += 2000
            
            self.bin.set('B', 0x7B, (value[0]-2000)) # year - 2000
            self.bin.set('B', 0x7C, value[1]) # month
            self.bin.set('B', 0x7D, value[2]) # day

            return
        
        date_year = self.bin.get('B', 0x7B)
        if date_year > 0:
            date_year += 2000
        date_month = self.bin.get('B', 0x7C)
        date_day = self.bin.get('B', 0x7D)

        return (date_year, date_month, date_day)
    
    def pokerus(self, value=None):
        """Pokérus

        @see http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9rus
        """

        return self.bin.getset('B', 0x82, value=value)
    
    def has_pokerus(self, value=None):
        "Check if a Pokémon is currently infected with Pokérus"
        
        rus_byte = self.pokerus

        return rus_byte % 16 != 0
    
    def had_pokerus(self, value=None):
        "Check if a Pokémon has had Pokérus"
        
        rus_byte = self.pokerus

        return ((rus_byte % 16 == 0) and (rus_byte != 0))
    
    def ball(self, value=None):
        "Poké Ball ID"
        
        return self.bin.getset('B', 0x83, value=value)
    
    def met_level(self, value=None):
        "Level at which the Pokémon was met"
        
        metlv_byte = self.bin.get('B', 0x84)

        if value is not None:
            new_byte = (metlv_byte & ~0x7f) | value
            self.bin.set('B', 0x84, new_byte)
        
        return metlv_byte & 0x7f # first 7 bits
    
    def ot_gender(self, value=None):
        "Original trainer gender"
        
        genders = {
            0: 'm', # male
            1: 'f', # female
        }
        gender_byte = self.bin.get('B', 0x84)

        if value is not None:
            if value == 'm':
                new_byte = clearbit(gender_byte, 7)
            elif value == 'f':
                new_byte = setbit(gender_byte, 7)
            
            self.bin.set('B', 0x84, new_byte)
        
        gender_id = getbit(gender_byte, 7)

        return genders[gender_id]
    
    def encounter_type(self, value=None):
        "Pokémon encounter type"
        
        return self.bin.getset('B', 0x85, value=value)
    
    def hgss_ball(self, value=None):
        "Secondary Poké Ball ID (HG/SS-only)"
        
        return self.bin.getset('B', 0x86, value=value)

class Gen5AttrMapper(Gen4AttrMapper):
    def __init__(self, bin_):
        super(Gen5AttrMapper, self).__init__(bin_)
    
    def nickname(self, value=None):
        "Pokémon nickname"

        return self.bin.getset_string(0x48, length=10, value=value)
    
    def ot_name(self, value=None):
        "Original trainer name"

        return self.bin.getset_string(0x68, length=7, value=value)
    
    def nature(self, value=None):
        "Nature (B/W-only)"
        
        return self.bin.getset('B', 0x41, value=value)
    
    def dw_ability(self, value=None):
        "Dream World ability flag (B/W-only)"
        
        return self.bin.getset('B', 0x42, value=value)

def load_mapper(bin_):
    "Return an instance of the appropriate attribute mapper."

    gen = bin_.get_gen()
    if gen == 5:
        return Gen5AttrMapper(bin_=bin_)
    elif gen == 4:
        return Gen4AttrMapper(bin_=bin_)
    elif gen == 3:
        return Gen3AttrMapper(bin_=bin_)