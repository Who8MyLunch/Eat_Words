
from __future__ import division, print_function, unicode_literals

import os

import numpy as np
import data_io as io

import tile_utilities
import board
import trie

########################################################
# Setup.
fname_game = '2012-05-08 20.36.00.png'

fname_config = 'config.yml'
folder_data = 'data'
folder_games = 'games'

#####################################
# Do it.
path_module = os.path.dirname(os.path.abspath(__file__))
path_data = os.path.join(path_module, folder_data)
path_games = os.path.join(path_module, folder_data, folder_games)

# Read config file.
f = os.path.join(path_data, fname_config)
info = io.read(f)

# Load reference tiles.
reference_grid = tile_utilities.load_reference_tiles()

# Load game and parse letters.
f = os.path.join(path_games, fname_game)
img_game, meta = io.read(f)

letters_game = tile_utilities.parse_game_grid(img_game, reference_grid, info)

# Make a board.
b = board.Board()
b.place_starting_letters(letters_game)

print( repr(b) )

i, j = 9, 3
j_start, num = b.contiguous_vertical((i,j))

print(j_start, num)
print(b.letters[i, j_start:j_start+num])

i_start, num = b.contiguous_horizontal((i,j))

print(i_start, num)
print(b.letters[i_start:i_start+num, j])
