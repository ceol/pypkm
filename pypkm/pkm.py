# coding=utf-8

"""Retrieve Pokémon information from a PKM file.


"""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

from pypkm.structs import g4pkm, g5pkm
from pypkm.crypto import encrypt, decrypt
from pypkm.sqlite import get_level, get_nature, get_basestats
from pypkm.util import calcstat

class BasePkm(object):

    # Constructor Struct object
    _strc = None

    # Construct Container object
    _ctnr = None

    def __getattr__(self, attr):
        return getattr(self._ctnr, attr)
    
    def __setattr__(self, attr, value):
        if hasattr(self._ctnr, attr):
            setattr(self._ctnr, attr, value)
        else:
            self.__dict__[attr] = value
    
    def _load(self, strc, data):
        self._strc = strc
        self._ctnr = self._strc.parse(data)
    
    def tostring(self):
        return self._strc.build(self._ctnr)

class Gen4Pkm(BasePkm):

    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 136
        
        if len(data) == 136:
            strc = g4pkm.pkm_struct
        elif len(data) == 236:
            strc = g4pkm.pkm_party_struct
        else:
            raise ValueError('Unsupported PKM file length: expected 136 or 236, received {}'.format(len(data)))
        
        self._load(strc, data)
    
    def toparty(self):
        # even if it's already a party file, we should process it
        data = self.tostring()[:136]
        # create empty data to load into Struct
        data = ''.join([data, '\x00' * 100])
        new_pkm = Gen4Pkm(data)

        new_pkm.level = get_level(pokemon_id=new_pkm.id, exp=new_pkm.exp)

        nature = get_nature(new_pkm.pv % 25)
        base_stats = get_basestats(pokemon_id=new_pkm.id)

        new_pkm.stats.current_hp = calcstat(iv=new_pkm.ivs.hp, ev=new_pkm.evs.hp, base=base_stats[0],
                              level=new_pkm.level, nature_stat=None)
        new_pkm.stats.max_hp = new_pkm.stats.current_hp
        new_pkm.stats.attack = calcstat(iv=new_pkm.ivs.attack, ev=new_pkm.evs.attack, base=base_stats[1],
                            level=new_pkm.level, nature_stat=nature[2])
        new_pkm.stats.defense = calcstat(iv=new_pkm.ivs.defense, ev=new_pkm.evs.defense, base=base_stats[2],
                            level=new_pkm.level, nature_stat=nature[3])
        new_pkm.stats.speed = calcstat(iv=new_pkm.ivs.speed, ev=new_pkm.evs.speed, base=base_stats[3],
                            level=new_pkm.level, nature_stat=nature[4])
        new_pkm.stats.spattack = calcstat(iv=new_pkm.ivs.spattack, ev=new_pkm.evs.spattack, base=base_stats[4],
                            level=new_pkm.level, nature_stat=nature[5])
        new_pkm.stats.spdefense = calcstat(iv=new_pkm.ivs.spdefense, ev=new_pkm.evs.spdefense, base=base_stats[5],
                            level=new_pkm.level, nature_stat=nature[6])
        
        return new_pkm

    def togts(self):
        pass

    def togen5(self):
        data = self.tostring()
        if len(data) == 236:
            # shave off the unused data if it's a party file. we don't
            # need to for pc files because they're the same size
            # between gens
            data = data[:220]
        new_pkm = Gen5Pkm(data)

        # nature gets its own byte in gen 5
        new_pkm.nature = new_pkm.pv % 25

        # the stringadapters automatically return unicode, and gen 5's
        # string encoding is unicode, so leverage the work we've
        # already done
        new_pkm.nickname = self.nickname
        new_pkm.ot_name = self.ot_name

        # set locations to faraway place; there's only one location set
        # at a time (either the pkm was met in the wild or received as
        # an egg)
        if new_pkm.egg_location != 0:
            new_pkm.egg_location = 2
        if new_pkm.met_location != 0:
            new_pkm.met_location = 2
        
        # these location bytes aren't used anymore
        new_pkm.egg_location_pt = 0
        new_pkm.met_location_pt = 0

        return new_pkm

class Gen5Pkm(BasePkm):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 136
        
        if len(data) == 136:
            strc = g5pkm.pkm_struct
        elif len(data) == 220:
            strc = g5pkm.pkm_party_struct
        else:
            raise ValueError('Unsupported PKM file length: expected 136 or 220, received {}'.format(len(data)))
        
        self._load(strc, data)
    
    def toparty(self):
        # even if it's already a party file, we should process it
        data = self.tostring()[:136]
        # create empty data to load into Struct
        data = ''.join([data, '\x00' * 84])
        new_pkm = Gen5Pkm(data)

        new_pkm.level = get_level(pokemon_id=new_pkm.id, exp=new_pkm.exp)

        nature = get_nature(new_pkm.pv % 25)
        base_stats = get_basestats(pokemon_id=new_pkm.id)

        new_pkm.stats.current_hp = calcstat(iv=new_pkm.ivs.hp, ev=new_pkm.evs.hp, base=base_stats[0],
                              level=new_pkm.level, nature_stat=None)
        new_pkm.stats.max_hp = new_pkm.stats.current_hp
        new_pkm.stats.attack = calcstat(iv=new_pkm.ivs.attack, ev=new_pkm.evs.attack, base=base_stats[1],
                            level=new_pkm.level, nature_stat=nature[2])
        new_pkm.stats.defense = calcstat(iv=new_pkm.ivs.defense, ev=new_pkm.evs.defense, base=base_stats[2],
                            level=new_pkm.level, nature_stat=nature[3])
        new_pkm.stats.speed = calcstat(iv=new_pkm.ivs.speed, ev=new_pkm.evs.speed, base=base_stats[3],
                            level=new_pkm.level, nature_stat=nature[4])
        new_pkm.stats.spattack = calcstat(iv=new_pkm.ivs.spattack, ev=new_pkm.evs.spattack, base=base_stats[4],
                            level=new_pkm.level, nature_stat=nature[5])
        new_pkm.stats.spdefense = calcstat(iv=new_pkm.ivs.spdefense, ev=new_pkm.evs.spdefense, base=base_stats[5],
                            level=new_pkm.level, nature_stat=nature[6])
        
        return new_pkm
    
    def togts(self):
        pass