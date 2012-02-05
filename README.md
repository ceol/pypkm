# PyPKM - Pokémon File Manipulation

## Introduction

PyPKM is a [Python][0] [package][1] for creating, editing, and manipulating
individual Pokémon file data (commonly referred to as PKM or .pkm files).
The goal of this project is to allow a cross-platform way to easily work
with these files.

PyPKM supports [generation IV][2] and [generation V][3] PKM files.

[0]: http://python.org/
[1]: http://pypi.python.org/pypi
[2]: http://projectpokemon.org/wiki/Pokemon_NDS_Structure
[3]: http://projectpokemon.org/wiki/Pokemon_Black/White_NDS_Structure

## Installation

To install PyPKM, download and unarchive the package from its [git repository][4].
Then, you can either `cd` into the newly-created directory and run
`python setup.py install` to install in your global Python path, or you can
enter the directory and manually copy the `pypkm` subdirectory to a place in
your Python path. PyPKM requires [Construct][5]==2.06 to parse file data.

[4]: https://github.com/ceol/pypkm
[5]: http://construct.wikispaces.com/

## Usage

First, import the `pypkm` package:

    >>> import pypkm

Then, create or load a PKM file (making sure to specify the file's game
generation):

    # Create from scratch
    >>> my_pkm = pypkm.new(gen=4)
    
    # Load from data
    >>> pkm_data = open('/path/to/MyPokemon.pkm', 'r').read()
    >>> my_pkm = pypkm.load(gen=4, data=pkm_data)

From here, you can edit your Pokémon's data by calling attributes of the
`my_pkm` instance. For example, to give your Pokémon the Leftovers item to
hold:

    >>> my_pkm.item = 234

To teach your Pokémon the Roar of Time move:

    >>> my_pkm.moves.move1 = 459

To see your Pokémon trainer's secret ID:

    >>> my_pkm.ot_secret_id
    65534

You might even want to change your Pokémon's species all together:

    >>> my_pkm.id = 94

As you can tell, you need to know the correct [index number][6] for most
editing. A proper API reference will be made available in time. Until then,
refer to the Struct declaration in `pypkm.structs`.

If you have GTS data, you can edit that as well:

    >>> gts_data = open('/path/to/gts_pkm.pkm.proper', 'r').open()
    >>> proper_pkm = pypkm.load(gen=4, data=gts_data)

    >>> proper_pkm.level
    5

    >>> proper_pkm.ot_name
    u'Trainer'

PyPKM also handles converting data. You can convert PC box data to party data,
to/from GTS server-sent data, and to/from GTS client-sent data. The list of
conversion methods are as follows:

* .togen5() - converts Gen 4 data to Gen 5
* .toparty() - adds battle data
* .togtsserver() - converts to data sent by the GTS server
* .togtsclient() - converts to data sent by the DS
* .topkm() - converts GTS data to a Pkm object

If you've edited the data, you probably want to save. PyPKM does not handle
saving data; you must save the file yourself. However, to convert an object
into a string of byte data:
    
    # you can call tostring() to return byte data
    >>> my_pkm.tostring()

[6]: http://bulbapedia.bulbagarden.net/wiki/Index_number

## Contribute

If you'd like to contribute, you can do so at my [git repository][4]. I'd
love to hear any bugs or feature requests you have.

## Thanks

The folks at [Project Pokemon][7] for all of their research
into the structure of Pokémon data.

[maxg][8] for answering my questions.

[Veekun][9] for looking over my code, introducing me to [Construct][5], and
providing an awesome database of Pokémon information.

[Stephen Anthony Uy][10] for his pycrypto module. Somehow I came across this
module whilst looking for a way to encrypt and decrypt Pokémon data, and
it's been a huge help (the `shuffle()` function comes directly from his work).

[7]: http://projectpokemon.org/
[8]: http://www.pokecheck.org/
[9]: http://veekun.com/
[10]: mailto:tsanth@iname.com