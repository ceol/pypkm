# PyPKM - PKM File Manipulation

## Introduction

PyPKM is a [Python][0] [package][1] for creating, editing, and manipulating
individual Pokémon file data (commonly referred to as PKM or .pkm files).
The goal of this project is to allow a cross-platform way to easily work
with these files in an intuitive way.

PyPKM supports [generation IV][2] and [generation V][3] PKM files.

[0]: http://python.org/
[1]: http://pypi.python.org/pypi
[2]: http://projectpokemon.org/wiki/Pokemon_NDS_Structure
[3]: http://projectpokemon.org/wiki/Pokemon_Black/White_NDS_Structure

## Installation

To install PyPKM, download and unarchive the package from its [git repository][4].
Then, you can either `cd` into the newly-created `pypkm` directory and run
`python setup.py install` to install in your global Python path, or you can
open the `pypkm` directory and manually copy the `pypkm` subdirectory to a
place in your Python path.

[4]: https://github.com/ceol/pypkm

## Usage

First, import the `Pkm` class from the `pypkm` package:

    import pypkm

Then, create or load a PKM file (making sure to specify the file's game
generation):

    # Create from scratch
    my_pkm = pypkm.new(gen=4)

    # Load from a file
    my_pkm = pypkm.load(gen=4, path='MyPokemon.pkm')
    
    # Load from data
    pkm_data = open('/path/to/MyPokemon.pkm', 'r').read()
    my_pkm = pypkm.load(gen=4, data=pkm_data)

From here, you can edit your Pokémon's data by calling attributes of the
`my_pkm` instance. For example, to give your Pokémon the Leftovers item to
hold:

    my_pkm.item = 234

To teach your Pokémon the Roar of Time move:

    my_pkm.move1 = 459

To see your Pokémon trainer's secret ID:

    my_pkm.ot_secret_id
    # 65534

You might even want to change your Pokémon's species all together:

    my_pkm.id = 94

As you can tell, you need to know the correct [index number][5] for most
editing. A proper API reference will be made available in time. Until then,
refer to the appropriate function's documentation in the `pkm` module.

If you've edited the data, you probably want to save. If you've created the
Pokémon from scratch or loaded directly from data and did not specify a path
to save, you must do so now:

    my_pkm.save('/path/to/NewPokemon.pkm')

If you loaded data from a file and optionally do not specify a path, PyPKM
will create a new file in the same directory as the old to avoid overwriting
the old data:

    my_pkm.save()
    # MyPokemon_new.pkm

[5]: http://bulbapedia.bulbagarden.net/wiki/Index_number

## Contribute

If you'd like to contribute, you can do so at my [git repository][4]. I'd
love to hear any bugs or feature requests you have.

## Thanks

Many thanks to the folks at [Project Pokemon][6] for all of their research
into the structure of Pokémon data.

A big thanks to [Stephen Anthony Uy][7] for his pycrypto module. Somehow I
came across this module whilst looking for a way to encrypt and decrypt
Pokémon data, and it's been a huge help (the `shuffle()` function comes
directly from his work).

[6]: http://projectpokemon.org/
[7]: tsanth@iname.com