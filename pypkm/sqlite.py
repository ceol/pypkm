# coding=utf-8

"A small wrapper for the PyPKM SQLite database."

__author__ = "Patrick Jacobs <ceolwulf@gmail.com>"

import os
import sqlite3

this_dir = os.path.dirname(os.path.abspath(__file__))

def get_cursor():
    "Return a SQLite cursor for queries."
    conn = sqlite3.connect(os.path.join(this_dir, 'pypkm.sqlite'))
    
    return conn.cursor()

def get_chr(ord_):
    """Retrieve a character from the gen 4 character table.

    Keyword arguments:
    ord_ (int) -- the character's index
    """

    db = get_cursor()

    query = 'SELECT `character` FROM `character_table` WHERE `id` = ? LIMIT 1'
    chr_ = db.execute(query, (ord_,)).fetchone()[0]

    db.close()

    return chr_

def get_ord(chr_):
    """Retrieve an ordinal from the gen 4 character table.

    Keyword arguments:
    chr_ (str) -- the ordinal's character
    """

    db = get_cursor()

    query = 'SELECT `id` FROM `character_table` WHERE `character` = ? LIMIT 1'
    ord_ = db.execute(query, (chr_,)).fetchone()[0]

    db.close()

    return ord_

def get_growthrate(self, pokemon_id):
    """Retrieve the growth rate ID of a Pokémon by its Dex ID.

    Keyword arguments:
    pokemon_id (int) -- the national dex ID of the Pokémon
    """

    db = get_cursor()

    query = 'SELECT `growth_rate_id` FROM `pokemon_growth_rates` WHERE `pokemon_id` = ?'
    growth_id = db.execute(query, (pokemon_id,)).fetchone()[0]

    db.close()

    return growth_id

def get_level(self, pokemon_id, exp):
    """Retrieve the level of a Pokémon by their experience points.

    Keyword arguments:
    pokemon_id (int) -- the national dex ID of the Pokémon
    exp (int) -- the experience points of the Pokémon
    """

    growth_id = get_growthrate(pokemon_id)

    db = get_cursor()

    # select the level that's closest to the pokemon's exp without
    # going over
    query = 'SELECT `level` FROM `levels` WHERE `growth_rate_id` = ? AND `experience` <= ? ORDER BY `experience` DESC LIMIT 1'
    level = db.execute(query, (growth_id,exp)).fetchone()[0]

    db.close()

    return level

def get_exp(self, pokemon_id, level):
    """Retrieve the experiance points of a Pokémon by their level.

    Keyword arguments:
    pokemon_id (int) -- the national dex ID of the Pokémon
    level (int) -- the level of the Pokémon
    """

    growth_id = get_growthrate(pokemon_id)

    db = get_cursor()

    # select the exp using the growth ID and level
    query = 'SELECT `experience` FROM `levels` WHERE `growth_id` = ? AND `level` = ?'
    exp = db.execute(query, (growth_id,level)).fetchone()[0]

    db.close()

    return exp

def get_nature(self, nature_id):
    """Retrieves a set of information about a nature.

    Keyword arguments:
    nature_id (int) -- the ID of the nature (0-24)
    """

    db = get_cursor()

    query = 'SELECT `id`, `name`, `atk`, `def`, `spe`, `spa`, `spd` FROM `natures` WHERE `id` = ?'
    nature = db.execute(query, (nature_id,)).fetchone()

    db.close()

    return nature

def get_basestats(self, pokemon_id, alt_form=0):
    """Retrieve base stats for a Pokémon.

    Keyword arguments:
    pokemon_id (int) -- the national dex ID
    alt_form (int) -- the optional alternate form
    """

    db = get_cursor()

    query = 'SELECT `base_hp`, `base_atk`, `base_def`, `base_spe`, `base_spa`, `base_spd` FROM `pokemon_base_stats` WHERE `pokemon_id` = ? AND `pokemon_form_id` = ?'
    base_stats = db.execute(query, (pokemon_id, alt_form)).fetchone()

    return base_stats