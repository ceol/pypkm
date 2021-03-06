# coding=utf-8

"""Retrieve Pokémon information from a PKM file."""

__author__ = 'Patrick Jacobs <ceolwulf@gmail.com>'

import datetime
import struct
from pypkm.structs import gen4, gen5
from pypkm.crypto import checksum, encrypt, decrypt
from pypkm.sqlite import get_level, get_nature, get_basestats
from pypkm.util import calcstat, LengthError
        

class StructData(object):
    """A wrapper class for the construct Container object."""

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
        data = self._strc.build(self._ctnr)

        return data

class PkmData(StructData):
    """A base class for Pokémon data."""
    
    def tostring(self):
        data = super(PkmData, self).tostring()

        # we need to recalculate the checksum when we build...
        # since building removes any trash bytes in the nickname and
        # ot name fields, if you're just reading the file, you should
        # store the loaded data instead of using tostring()
        chksum = checksum(data[0x08:])
        packed = struct.pack('<H', chksum)
        data = ''.join([
            data[:0x06],
            packed,
            data[0x08:],
        ])

        return data

class Gen4BoxPkm(PkmData):

    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 136
        elif len(data) != 136:
            raise LengthError(136, len(data))
        
        self._load(gen4.pkm_struct, data)
    
    def toparty(self):
        # even if it's already a party file, we should process it
        data = self.tostring()[:136]
        
        # create empty data to load into Struct
        data = ''.join([data, '\x00' * 100])
        new_pkm = Gen4PartyPkm(data)

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
    
    def togtsserver(self):
        # have to do this in case our old data isn't party
        obj = self
        # check if it's a party file (this hopefully saves us from
        # building data twice)
        try:
            obj.level
        except AttributeError:
            obj = self.toparty()
        
        # pkm data sent over the GTS is both party and encrypted
        data = encrypt(obj.tostring())

        # create empty data to load into Struct
        gts = Gen4ServerPkm('\x00' * 292)

        gts.encrypted_pkm = data

        gts.id = obj.id
        if obj.is_genderless:
            gts.gender = 0x03
        elif obj.is_female:
            gts.gender = 0x02
        else:
            gts.gender = 0x01
        gts.level = obj.level

        gts.requested.id = 1 # bulbasaur
        gts.requested.gender = 0x02 # female
        gts.requested.min_level = 0 # any
        gts.requested.max_level = 0 # any
        
        if obj.ot_is_female:
            gts.ot_gender = 0x01

        now = datetime.datetime.now()
        gts.deposited_time.year = now.year
        gts.deposited_time.month = now.month
        gts.deposited_time.day = now.day
        gts.deposited_time.hour = now.hour
        gts.deposited_time.minute = now.minute
        gts.deposited_time.second = now.second

        gts.traded_time.year = now.year
        gts.traded_time.month = now.month
        gts.traded_time.day = now.day
        gts.traded_time.hour = now.hour
        gts.traded_time.minute = now.minute
        gts.traded_time.second = now.second

        gts.pv = obj.pv
        gts.ot_name = obj.ot_name
        gts.ot_id = obj.ot_id

        gts.country = 0xDB # not sure, taken from ir-gts
        gts.city = 0x02 # not sure, taken from ir-gts
        
        if gts.ot_gender == 0x01:
            # if female, set to lass; if male, leave at 0 for youngster
            gts.ot_sprite = 0x08
        
        gts.is_exchanged = True
        gts.version = 0x08 # soulsilver version
        gts.language = obj.language

        return gts
    
    def togtsclient(self):
        # have to do this in case our old data isn't party
        obj = self
        # check if it's a party file (this hopefully saves us from
        # building data twice)
        try:
            obj.level
        except AttributeError:
            obj = self.toparty()
        
        # pkm data sent over the GTS is both party and encrypted
        data = encrypt(obj.tostring())

        # create empty data to load into Struct
        gts = Gen4ClientPkm('\x00' * 296)

        gts.encrypted_pkm = data

        gts.id = obj.id
        if obj.is_genderless:
            gts.gender = 0x03
        elif obj.is_female:
            gts.gender = 0x02
        else:
            gts.gender = 0x01
        gts.level = obj.level

        gts.requested.id = 1 # bulbasaur
        gts.requested.gender = 0x02 # female
        gts.requested.min_level = 0 # any
        gts.requested.max_level = 0 # any
        
        if obj.ot_is_female:
            gts.ot_gender = 0x01

        now = datetime.datetime.now()
        gts.deposited_time.year = now.year
        gts.deposited_time.month = now.month
        gts.deposited_time.day = now.day
        gts.deposited_time.hour = now.hour
        gts.deposited_time.minute = now.minute
        gts.deposited_time.second = now.second

        gts.traded_time.year = now.year
        gts.traded_time.month = now.month
        gts.traded_time.day = now.day
        gts.traded_time.hour = now.hour
        gts.traded_time.minute = now.minute
        gts.traded_time.second = now.second

        gts.pv = obj.pv
        gts.ot_name = obj.ot_name
        gts.ot_id = obj.ot_id

        gts.country = 0xDB # not sure, taken from ir-gts
        gts.city = 0x02 # not sure, taken from ir-gts
        
        if gts.ot_gender == 0x01:
            # if female, set to lass; if male, leave at 0 for youngster
            gts.ot_sprite = 0x08
        
        gts.is_exchanged = True
        gts.version = 0x08 # soulsilver version
        gts.language = obj.language

        return gts
    
    def togen5(self):
        data = self.tostring()
        if len(data) == 236:
            # shave off the unused data if it's a party file. we don't
            # need to for pc files because they're the same size
            # between gens
            data = data[:220]
            new_pkm = Gen5PartyPkm(data)
        else:
            new_pkm = Gen5BoxPkm(data)

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

        return new_pkm

class Gen4PartyPkm(Gen4BoxPkm):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 236
        elif len(data) != 236:
            raise LengthError(236, len(data))
        
        self._load(gen4.pkm_party_struct, data)
    
class Gen5BoxPkm(PkmData):

    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 136
        elif len(data) != 136:
            raise LengthError(136, len(data))
        
        self._load(gen5.pkm_struct, data)
    
    def toparty(self):
        # even if it's already a party file, we should process it
        data = self.tostring()[:136]
        
        # create empty data to load into Struct
        data = ''.join([data, '\x00' * 100])
        new_pkm = Gen5PartyPkm(data)

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
    
    def togtsserver(self):
        # have to do this in case our old data isn't party
        obj = self
        # check if it's a party file (this hopefully saves us from
        # building data twice)
        try:
            obj.level
        except AttributeError:
            obj = self.toparty()
        
        # pkm data sent over the GTS is both party and encrypted
        data = encrypt(obj.tostring())

        # create empty data to load into Struct
        gts = Gen5ServerPkm('\x00' * 296)

        gts.encrypted_pkm = data

        gts.id = obj.id
        if obj.is_genderless:
            gts.gender = 0x03
        elif obj.is_female:
            gts.gender = 0x02
        else:
            gts.gender = 0x01
        gts.level = obj.level

        gts.requested.id = 1 # bulbasaur
        gts.requested.gender = 0x02 # female
        gts.requested.min_level = 0 # any
        gts.requested.max_level = 0 # any
        
        if obj.ot_is_female:
            gts.ot_gender = 0x01

        now = datetime.datetime.now()
        gts.deposited_time.year = now.year
        gts.deposited_time.month = now.month
        gts.deposited_time.day = now.day
        gts.deposited_time.hour = now.hour
        gts.deposited_time.minute = now.minute
        gts.deposited_time.second = now.second

        gts.traded_time.year = now.year
        gts.traded_time.month = now.month
        gts.traded_time.day = now.day
        gts.traded_time.hour = now.hour
        gts.traded_time.minute = now.minute
        gts.traded_time.second = now.second

        gts.pv = obj.pv
        gts.ot_id = obj.ot_id
        gts.ot_secret_id = obj.ot_secret_id
        gts.ot_name = obj.ot_name

        gts.country = 0xDB # not sure, taken from ir-gts
        gts.city = 0x02 # not sure, taken from ir-gts
        
        if gts.ot_gender == 0x01:
            # if female, set to lass; if male, leave at 0 for youngster
            gts.ot_sprite = 0x08
        
        gts.is_exchanged = True
        gts.version = 0x14 # white version
        gts.language = obj.language

        return gts
    
    def togtsclient(self):
        # have to do this in case our old data isn't party
        obj = self
        # check if it's a party file (this hopefully saves us from
        # building data twice)
        try:
            obj.level
        except AttributeError:
            obj = self.toparty()
        
        # pkm data sent over the GTS is both party and encrypted
        data = encrypt(obj.tostring())

        # create empty data to load into Struct
        gts = Gen5ClientPkm('\x00' * 444)

        gts.encrypted_pkm = data

        gts.pv = obj.pv
        gts.length = 432

        gts.id = obj.id
        if obj.is_genderless:
            gts.gender = 0x03
        elif obj.is_female:
            gts.gender = 0x02
        else:
            gts.gender = 0x01
        gts.level = obj.level

        gts.requested.id = 1 # bulbasaur
        gts.requested.gender = 0x02 # female
        gts.requested.min_level = 0 # any
        gts.requested.max_level = 0 # any
        
        if obj.ot_is_female:
            gts.ot_gender = 0x01
        gts.ot_nature = 24 # quirky

        now = datetime.datetime.now()
        gts.deposited_time.year = now.year
        gts.deposited_time.month = now.month
        gts.deposited_time.day = now.day
        gts.deposited_time.hour = now.hour
        gts.deposited_time.minute = now.minute
        gts.deposited_time.second = now.second

        gts.traded_time.year = now.year
        gts.traded_time.month = now.month
        gts.traded_time.day = now.day
        gts.traded_time.hour = now.hour
        gts.traded_time.minute = now.minute
        gts.traded_time.second = now.second

        gts.ot_id = obj.ot_id
        gts.ot_secret_id = obj.ot_secret_id
        gts.ot_name = obj.ot_name

        gts.country = 0xDB # not sure, taken from ir-gts
        gts.city = 0x02 # not sure, taken from ir-gts
        
        if gts.ot_gender == 0x01:
            # if female, set to lass; if male, leave at 0 for youngster
            gts.ot_sprite = 0x08
        
        gts.is_exchanged = True
        gts.version = 0x14 # white version
        gts.language = obj.language

        gts.unknown_0to8 = 8 # no idea!

        gts.terminator = 128

        return gts

class Gen5PartyPkm(Gen5BoxPkm):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 220
        elif len(data) != 220:
            raise LengthError(220, len(data))
        
        self._load(gen5.pkm_party_struct, data)

class GTSData(StructData):
    """A base class for data sent to or from the GTS server."""
    pass

class Gen4ServerData(GTSData):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 292
        elif len(data) != 292:
            raise LengthError(292, len(data))
        
        self._load(gen4.pkm_gtsserver_struct, data)
    
    def topkm(self):
        data = decrypt(self.encrypted_pkm)

        return Gen4PartyPkm(data)

class Gen4ClientData(GTSData):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 296
        elif len(data) != 296:
            raise LengthError(296, len(data))
        
        self._load(gen4.pkm_gtsclient_struct, data)
    
    def topkm(self):
        data = decrypt(self.encrypted_pkm)

        return Gen4PartyPkm(data)

class Gen5ServerData(GTSData):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 296
        elif len(data) != 296:
            raise LengthError(296, len(data))
        
        self._load(gen5.pkm_gtsserver_struct, data)
    
    def topkm(self):
        data = decrypt(self.encrypted_pkm)

        return Gen5PartyPkm(data)

class Gen5ClientData(GTSData):
    
    def __init__(self, data=None):
        if data is None:
            data = '\x00' * 444
        elif len(data) != 444:
            raise LengthError(444, len(data))
        
        self._load(gen5.pkm_gtsclient_struct, data)
    
    def topkm(self):
        data = decrypt(self.encrypted_pkm)

        return Gen5PartyPkm(data)

def get_pkmobj(gen, data):
    objs = {
        4: {
            136: Gen4BoxPkm,
            236: Gen4PartyPkm,
            292: Gen4ServerData,
            296: Gen4ClientData,
        },
        5: {
            136: Gen5BoxPkm,
            220: Gen5PartyPkm,
            296: Gen5ServerData,
            444: Gen5ClientData,
        }
    }
    
    return objs.get(gen).get(len(data))(data)
