# coding=utf-8

import sqlite3

from pypkm.utils import getbit, setbit, clearbit
from pypkm.binary import PkmBinaryFile

def _get_cursor(path):
    conn = sqlite3.connect(path)
    return conn.cursor()

def _get_letter(c, letter):
    query = 'SELECT `character` FROM `charmap` WHERE `id` = ?'
    return c.execute(query, (letter,)).fetchone()[0]

class AttrMapper(object):
    "Core attribute mapping functionality."

    def __getattr__(self, name):
        "Attempt to map any calls to missing attributes to functions."
        
        try:
            func_name = '{}{}'.format('attr__', name)
            return object.__getattribute__(self, func_name)()
        except AttributeError:
            # catch exception to raise a more helpful one
            error = "'{}' object has no attribute '{}'".format(self.__class__.__name__, name)
            raise AttributeError(error)
    
    def __setattr__(self, name, value):
        "Attempt to call attributes as functions."
        
        try:
            getattr(self, 'attr__' + name)(value)
        except AttributeError:
            self.__dict__[name] = value

class PkmAttrMapper(AttrMapper, PkmBinaryFile):
    """Functions used to map attribute calls.

    PkmAttrMapper relies on the child class also extending PkmBinaryFile to
    use the get and set methods.
    """
    
    def attr__pv(self, value=None):
        """Personality value.
        
        Note: Do NOT edit this unless you know what you are doing!
        """
        
        return self.getset(fmt='L', offset=0x00, value=value)
            
    def attr__checksum(self, value=None):
        """Checksum.
        
        This should only be edited when the byte data is changed. Use the
        appropriate pypkm.util function to calculate.
        """
        
        return self.getset(fmt='H', offset=0x06, value=value)
    
    def attr__id(self, value=None):
        "National Pokédex ID."
        
        return self.getset(fmt='H', offset=0x08, value=value)
    
    def attr__item(self, value=None):
        "Held item ID."
        
        return self.getset(fmt='H', offset=0x0A, value=value)
    
    def attr__ot_id(self, value=None):
        "Original trainer ID."
        
        return self.getset(fmt='H', offset=0x0C, value=value)
    
    def attr__ot_secret_id(self, value=None):
        "Original trainer secret ID."
        
        return self.getset(fmt='H', offset=0x0E, value=value)
    
    def attr__exp(self, value=None):
        "Experience points total."
        
        return self.getset(fmt='L', offset=0x10, value=value)
    
    def attr__happiness(self, value=None):
        "Happiness (or steps to hatch if an egg)."
        
        return self.getset(fmt='B', offset=0x14, value=value)
    
    def attr__ability(self, value=None):
        "Ability ID."
        
        return self.getset(fmt='B', offset=0x15, value=value)
    
    def attr__markings(self, value=None):
        "Pokédex markings. (I think?)"
        
        # Currently not used in favor of returning the raw value
        #markings = {
        #    0x01: 'circle',
        #    0x02: 'triangle',
        #    0x04: 'square',
        #    0x08: 'heart',
        #    0x10: 'star',
        #    0x20: 'diamond',
        #}

        return self.getset(fmt='B', offset=0x16, value=value)
    
    def attr__language(self, value=None):
        "Language ID."
        
        # Currently not used in favor of returning the raw value
        #languages = {
        #    0x01: 'jp',
        #    0x02: 'en',
        #    0x03: 'fr',
        #    0x04: 'it',
        #    0x05: 'de',
        #    0x07: 'es',
        #    0x08: 'kr',
        #}
        
        return self.getset(fmt='B', offset=0x17, value=value)
    
    def attr__hp_ev(self, value=None):
        "Hit points effort value."
        
        return self.getset(fmt='B', offset=0x18, value=value)
    
    def attr__atk_ev(self, value=None):
        "Attack effort value."
        
        return self.getset(fmt='B', offset=0x19, value=value)
    
    def attr__def_ev(self, value=None):
        "Defense effort value."
        
        return self.getset(fmt='B', offset=0x1A, value=value)
    
    def attr__spe_ev(self, value=None):
        "Speed effort value."
        
        return self.getset(fmt='B', offset=0x1B, value=value)
    
    def attr__spa_ev(self, value=None):
        "Special attack effort value."
        
        return self.getset(fmt='B', offset=0x1C, value=value)
    
    def attr__spd_ev(self, value=None):
        "Special defense effort value."
        
        return self.getset(fmt='B', offset=0x1D, value=value)
    
    def attr__cool_cv(self, value=None):
        "Cool contest value."
        
        return self.getset(fmt='B', offset=0x1E, value=value)
    
    def attr__beauty_cv(self, value=None):
        "Beauty contest value."
        
        return self.getset(fmt='B', offset=0x1F, value=value)
    
    def attr__cute_cv(self, value=None):
        "Cute contest value."
        
        return self.getset(fmt='B', offset=0x20, value=value)
    
    def attr__smart_cv(self, value=None):
        "Smart contest value."
        
        return self.getset(fmt='B', offset=0x21, value=value)
    
    def attr__tough_cv(self, value=None):
        "Tough contest value."
        
        return self.getset(fmt='B', offset=0x22, value=value)
    
    def attr__sheen_cv(self, value=None):
        "Sheen contest value."
        
        return self.getset(fmt='B', offset=0x23, value=value)
    
    def attr__ribbons(self, value=None):
        "Hoenn and Sinnoh ribbon sets."
        pass
    
    def attr__move1(self, value=None):
        "Move #1 ID."
        
        return self.getset(fmt='H', offset=0x28, value=value)
    
    def attr__move2(self, value=None):
        "Move #2 ID."
        
        return self.getset(fmt='H', offset=0x2A, value=value)
    
    def attr__move3(self, value=None):
        "Move #3 ID."
        
        return self.getset(fmt='H', offset=0x2C, value=value)
    
    def attr__move4(self, value=None):
        "Move #4 ID."
        
        return self.getset(fmt='H', offset=0x2E, value=value)
    
    def attr__move1_pp(self, value=None):
        "Current move #1 PP."
        
        return self.getset(fmt='B', offset=0x30, value=value)
    
    def attr__move2_pp(self, value=None):
        "Current move #2 PP."
        
        return self.getset(fmt='B', offset=0x31, value=value)
    
    def attr__move3_pp(self, value=None):
        "Current move #3 PP."
        
        return self.getset(fmt='B', offset=0x32, value=value)
    
    def attr__move4_pp(self, value=None):
        "Current move #4 PP."
        
        return self.getset(fmt='B', offset=0x33, value=value)
    
    def attr__move1_ppups(self, value=None):
        "Move #1 PP-Ups."
        
        return self.getset(fmt='B', offset=0x34, value=value)
    
    def attr__move2_ppups(self, value=None):
        "Move #2 PP-Ups."
        
        return self.getset(fmt='B', offset=0x35, value=value)
    
    def attr__move3_ppups(self, value=None):
        "Move #3 PP-Ups."
        
        return self.getset(fmt='B', offset=0x36, value=value)
    
    def attr__move4_ppups(self, value=None):
        "Move #4 PP-Ups."
        
        return self.getset(fmt='B', offset=0x37, value=value)
    
    def attr__hp_iv(self, value=None):
        "Hit point individual value."

        return self.getset_iv(mask=0x0000001f, shift=0, value=value)
    
    def attr__atk_iv(self, value=None):
        "Attack individual value."
        
        return self.getset_iv(mask=0x000003e0, shift=5, value=value)
    
    def attr__def_iv(self, value=None):
        "Defense individual value."
        
        return self.getset_iv(mask=0x00007c00, shift=10, value=value)
    
    def attr__spe_iv(self, value=None):
        "Speed individual value."
        
        return self.getset_iv(mask=0x000f8000, shift=15, value=value)
    
    def attr__spa_iv(self, value=None):
        "Special attack individual value."
        
        return self.getset_iv(mask=0x01f00000, shift=20, value=value)
    
    def attr__spd_iv(self, value=None):
        "Special defense individual value."
        
        return self.getset_iv(mask=0x3e000000, shift=25, value=value)
    
    def attr__is_egg(self, value=None):
        "Is egg flag."
        
        egg_byte = self.get('L', 0x38)

        if value is not None:
            if value == True:
                new_byte = setbit(egg_byte, 30)
            elif value == False:
                new_byte = clearbit(egg_byte, 30)
            else:
                raise AttributeError('invalid is_egg value')
            
            return self.set('L', 0x38, new_byte)
        
        return getbit(egg_byte, 30) == 1
    
    def attr__is_nicknamed(self, value=None):
        "Is nicknamed flag."

        nick_byte = self.get('L', 0x38)

        if value is not None:
            if value == True:
                new_byte = setbit(nick_byte, 31)
            elif value == False:
                new_byte = clearbit(nick_byte, 31)
            else:
                raise AttributeError('invalid is_nicknamed value')
            
            return self.set('L', 0x38, new_byte)
                
        return getbit(nick_byte, 31) == 1

    def attr__is_fateful(self, value=None):
        "Fateful encounter flag."
        
        fate_byte = self.get('B', 0x40)

        if value is not None:
            if value == True:
                new_byte = setbit(fate_byte, 0)
            elif value == False:
                new_byte = clearbit(fate_byte, 0)
            else:
                raise AttributeError('invalid is_fateful value')
            
            return self.set('B', 0x40, new_byte)
        
        return getbit(fate_byte, 0) == 1
    
    def attr__gender(self, value=None):
        "Pokémon gender."
        
        genders = {
            0b11: 'm', # male
            0b01: 'f', # female
            0b10: 'n', # genderless
        }

        gender_byte = self.get('B', 0x40)
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
            else:
                raise ValueError('invalid gender value')

            return self.set('B', 0x40, new_byte)
        
        return genders[gender_id]
    
    def attr__shiny_leaves(self, value=None):
        "Shiny leaves. (HG/SS-only)"
        pass
    
    def attr__has_leafcrown(self, value=None):
        "Leaf Crown. (HG/SS-only)"
        
        leaf_byte = self.get('B', 0x41)

        if value is not None:
            if value == True:
                new_byte = setbit(leaf_byte, 5)
            elif value == False:
                new_byte = clearbit(leaf_byte, 5)
            else:
                raise AttributeError('invalid has_leafcrown value')
            
            return self.set('B', 0x41, new_byte)
        
        return getbit(leaf_byte, 5) == 1
    
    def attr__egg_location(self, value=None):
        "Location where the egg was received."
        
        return self.getset(fmt='H', offset=0x7E, value=value)
    
    def attr__met_location(self, value=None):
        "Location where the Pokémon was met."
        
        return self.getset(fmt='H', offset=0x80, value=value)
    
    def attr__pt_egg_location(self, value=None):
        "Location where the egg was received. (Platinum-only)"
        
        return self.getset(fmt='H', offset=0x44, value=value)
    
    def attr__pt_met_location(self, value=None):
        "Location where the Pokémon was met. (Platinum-only)"
        
        return self.getset(fmt='H', offset=0x44, value=value)
    
    def attr__nickname(self, value=None):
        "Pokémon nickname."
        
        nickname = ''
        offset = 0x48

        if self.get_gen() == 4:
            import os
            this_dir = os.path.dirname(os.path.abspath(__file__))
            c = _get_cursor(path=os.path.join(this_dir, 'pypkm.sqlite'))

        while True:
            letter = self.get('H', offset)
            if letter == 0xFFFF or offset > 0x5B:
                break
            
            if self.get_gen() == 5:
                nickname += unichr(letter)
            elif self.get_gen() == 4:
                nickname += _get_letter(c, letter)
            
            offset += 2

        if self.get_gen() == 4:
            c.close()
        
        return nickname
    
    def attr__hometown(self, value=None):
        "Pokémon hometown."
        
        return self.getset(fmt='B', offset=0x5F, value=value)
    
    def attr__ot_name(self, value=None):
        "Original trainer name."
        pass
    
    def attr__egg_date(self, value=None):
        "Date when the egg was received."

        if value is not None:
            self.set('B', 0x78, (value[0]-2000)) # year - 2000
            self.set('B', 0x79, value[1]) # month
            self.set('B', 0x7A, value[2]) # day

            return
        
        date_year = self.get('B', 0x78)
        if date_year > 0:
            date_year += 2000
        date_month = self.get('B', 0x79)
        date_day = self.get('B', 0x7A)

        return (date_year, date_month, date_day)
    
    def attr__met_date(self, value=None):
        "Date when the Pokémon was met."

        if value is not None:
            self.set('B', 0x7B, (value[0]-2000)) # year - 2000
            self.set('B', 0x7C, value[1]) # month
            self.set('B', 0x7D, value[2]) # day

            return
        
        date_year = self.get('B', 0x7B)
        if date_year > 0:
            date_year += 2000
        date_month = self.get('B', 0x7C)
        date_day = self.get('B', 0x7D)

        return (date_year, date_month, date_day)
    
    def attr__pokerus(self, value=None):
        """Pokérus.

        @see http://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9rus
        """

        return self.getset(fmt='B', offset=0x82, value=value)
    
    def attr__has_pokerus(self, value=None):
        "Check if a Pokémon is currently infected with Pokérus."
        
        rus_byte = self.pokerus

        return rus_byte % 16 != 0
    
    def attr__had_pokerus(self, value=None):
        "Check if a Pokémon has had Pokérus."
        
        rus_byte = self.pokerus

        return ((rus_byte % 16 == 0) and (rus_byte != 0))
    
    def attr__ball(self, value=None):
        "Poké Ball ID."
        
        return self.getset(fmt='B', offset=0x83, value=value)
    
    def attr__met_level(self, value=None):
        "Level at which the Pokémon was met."
        
        metlv_byte = self.get('B', 0x84)

        if value is not None:
            new_byte = (metlv_byte & ~0x7f) | value
            self.set('B', 0x84, new_byte)
        
        return metlv_byte & 0x7f # first 7 bits
    
    def attr__ot_gender(self, value=None):
        "Original trainer gender."
        
        genders = {
            0: 'm', # male
            1: 'f', # female
        }
        gender_byte = self.get('B', 0x84)

        if value is not None:
            if value == 'm':
                new_byte = clearbit(gender_byte, 7)
            elif value == 'f':
                new_byte = setbit(gender_byte, 7)
            else:
                raise AttributeError('invalid ot_gender value')
            
            self.set('B', 0x84, new_byte)
        
        gender_id = getbit(gender_byte, 7)

        return genders[gender_id]
    
    def attr__encounter_type(self, value=None):
        "Pokémon encounter type."
        
        return self.getset(fmt='B', offset=0x85, value=value)
    
    def attr__hgss_ball(self, value=None):
        "Secondary Poké Ball ID. (HG/SS-only)"
        
        return self.getset(fmt='B', offset=0x86, value=value)
    
    def attr__nature(self, value=None):
        "Nature. (B/W-only)"
        
        return self.getset(fmt='B', offset=0x41, value=value)
    
    def attr__dw_ability(self, value=None):
        "Dream World ability flag. (B/W-only)"
        
        return self.getset(fmt='B', offset=0x42, value=value)