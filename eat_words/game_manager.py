
from __future__ import division, print_function, unicode_literals

import os

import data_io as io
import tiles

import board_manager
import trie_manager


########################################################
# Setup.
# fname_game = '2012-05-08 20.36.00.png'
fname_game = '2012-06-22 23.10.30.png'

fname_dictionary = 'words_zynga.txt'
fname_config = 'config.yml'

folder_data = 'data'
folder_games = 'games'
folder_dictionary = 'words and letters'

##########################################
# Do it.
path_module = os.path.dirname(os.path.abspath(__file__))

path_data = os.path.join(path_module, folder_data)
path_games = os.path.join(path_data, folder_games)
path_dictionary = os.path.join(path_data, folder_dictionary)

#
# Load data.
#

# Read config file.
f = os.path.join(path_data, fname_config)
info_config = io.read(f)

# Load dictionary into trie.
f = os.path.join(path_dictionary, fname_dictionary)
daggad = trie_manager.load_daggad_dictionary(f)

# Reference tiles.
info_reference_grid, info_reference_rack = tiles.load_reference_tiles()

# Load game image.
f = os.path.join(path_games, fname_game)
img_game, meta = io.read(f)

# Parse game image to game letters.
letters_game, letters_rack = tiles.parse_game_letters(img_game,
                                                      info_reference_grid,
                                                      info_reference_rack,
                                                      info_config)
# Build game board.
board = board_manager.Board()
board.set_game_letters(letters_game)

print(board)

print(letters_rack)

#
# Cross check.
#
for i, j in board.anchors:

    ij_pre, letters_pre = board.contiguous_vertical( (i, j-1) )
    ij_post, letters_post = board.contiguous_vertical( (i, j+1) )

    board.playables[i, j] = ''

    # Loop over rack letters, establish wich are playable.
    for L in letters_rack:
        word_test = letters_pre + L + letters_post
        if daggad.search(word_test):
            board.playables[i, j] += L




#
# Work with a single line.
#
j = 15
line, playable = board.get_line(j)
print(line)
print(playable)

# Pretty print.
template = '%1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s'
print()

val = [v for v in playable]
for k in range(7):
    line = [v[:1] for v in val]
    print(template % tuple(line))
    val = [v[1:] for v in val]

