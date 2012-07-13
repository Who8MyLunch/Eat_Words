
from __future__ import division, print_function, unicode_literals

import os
import glob
import numpy as np

import data_io as io



#########################################


def carve_tiles(img, info_config):
    """
    Carve out grid and rack tiles from screenshot image.
    """
    dx_grid = info_config['grid_parameters']['dx']
    i0_grid = info_config['grid_parameters']['i0']
    j0_grid = info_config['grid_parameters']['j0']

    num_grid_x = info_config['grid_parameters']['num_x']
    num_grid_y = info_config['grid_parameters']['num_y']

    dx_rack = info_config['rack_parameters']['dx']
    i0_rack = info_config['rack_parameters']['i0']
    j0_rack = info_config['rack_parameters']['j0']

    num_rack_x = info_config['rack_parameters']['num_x']
    num_rack_y = info_config['rack_parameters']['num_y']


    # Grid coordinates.
    i_grid = np.arange(i0_grid, i0_grid + dx_grid*(num_grid_x), dx_grid)
    j_grid = np.arange(j0_grid, j0_grid + dx_grid*(num_grid_y), dx_grid)

    i_rack = np.arange(i0_rack, i0_rack + dx_rack*(num_rack_x), dx_rack)
    j_rack = np.arange(j0_rack, j0_rack + dx_rack*(num_rack_y), dx_rack)

    # Carve out grid tiles.
    tiles_grid = []
    for jj, j in enumerate(j_grid):
        for ii, i in enumerate(i_grid):
            tile = img[j:j+dx_grid, i:i+dx_grid]
            tile = apply_mask(tile, info_config)
            tiles_grid.append( ([ii, jj], tile) )

    # Carve out rack tiles.
    tiles_rack = []
    for jj, j in enumerate(j_rack):
        for ii, i in enumerate(i_rack):
            tile = img[j:j+dx_rack, i:i+dx_rack, :]
            tile = apply_mask(tile, info_config)
            tiles_rack.append( ([ii, jj], tile) )

    # Done.
    return tiles_grid, tiles_rack



def apply_mask(tile, info_config):
    """
    Mask out portion of tile.
    """

    tile = np.asarray(tile).copy()
    wid = tile.shape[0]

    if wid == info_config['grid_parameters']['dx']:
        info_mask = info_config['grid_tile_mask']
        symmetric = False
    elif wid == info_config['rack_parameters']['dx']:
        info_mask = info_config['rack_tile_mask']
        symmetric = True
    else:
        raise Exception('Invalid tile size: %s' % wid)

    for i,j in info_mask:
        tile[j, i:, :] = 0

        if symmetric:
            tile[j, :-i, :] = 0
            tile[-j-1, i:, :] = 0
            tile[-j-1, :-i, :] = 0
            
    # Done.
    return tile



def load_reference_tiles(path_base=None):
    """
    Load reference tile images.
    """

    ix_name_label = 10
    pattern_grid_tiles = 'tile_grid_*.png'
    pattern_rack_tiles = 'tile_rack_*.png'

    if path_base is None:
        path_base = os.path.dirname(os.path.abspath(__file__))
    
    folder_tiles = os.path.join('data', 'tiles')
    path_tiles = os.path.join(path_base, folder_tiles)

    # Load reference grid tiles and rack tiles.
    p = os.path.join(path_tiles, pattern_grid_tiles)
    files_grid = glob.glob(p)

    p = os.path.join(path_tiles, pattern_rack_tiles)
    files_rack = glob.glob(p)

    info_reference_grid = {}
    for f in files_grid:
        # Load tile from file.
        tile, meta = io.read(f)

        # Extract label.
        name, ext = os.path.splitext(os.path.basename(f))
        label = name[ix_name_label:]

        # Store.
        info_reference_grid[label] = tile

    info_reference_rack = {}
    for f in files_rack:
        # Load tile from file.
        tile, meta = io.read(f)

        # Extract label.
        name, ext = os.path.splitext(os.path.basename(f))
        label = name[ix_name_label:]

        # Store.
        info_reference_rack[label] = tile

    # Done.
    return info_reference_grid, info_reference_rack

    
    
def match_tile_letter(tile_test, info_reference):
    thresh = 10**2
    
    scores = []
    labels = []
    for label, tile_reference in info_reference.items():
        if tile_test.shape == tile_reference.shape:
            diff = tile_test.astype(np.float) - tile_reference.astype(np.float)
            rms = np.mean( diff**2 )
            
            scores.append(rms)
            labels.append(label)
        
    bool_pass = np.asarray(scores) < thresh
    num = np.sum(bool_pass)
    if num != 1:
        raise Exception('Number of matching tiles is not unique: %d' % num)
    
    ix_best = np.argmin(scores)
    label_best = labels[ix_best]
    
    # Labels are multiple-character strings.  First letter is the one we want.
    if 1 <= len(label_best) <= 2:
        letter = label_best[0].lower()
    else:
        letter = None
    
    # Done.
    return letter

    
    
def parse_game_letters(img_game, info_reference_grid, info_reference_rack, info_config):
    """
    Match game tiles to played letters.
    """
    
    # Carve game tiles.
    tiles_grid_game, tiles_rack_game = carve_tiles(img_game, info_config)

    # Determine letters on game grid.
    letters_grid = []
    for ij_test, tile_test in tiles_grid_game:
        letter = match_tile_letter(tile_test, info_reference_grid)

        if letter:
            ij_test[0] += 1
            ij_test[1] += 1
            letters_grid.append( (ij_test, letter) )
            
    # Determine letters on game rack.
    letters_rack = ''
    for ij_test, tile_test in tiles_rack_game:
        letter = match_tile_letter(tile_test, info_reference_rack)

        if letter:
            ij_test[0] += 1
            ij_test[1] += 1
            letters_rack += letter
                
    # Done.
    return letters_grid, letters_rack
    