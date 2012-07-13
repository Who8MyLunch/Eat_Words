
from __future__ import division, print_function, unicode_literals

import os
import numpy as np
import matplotlib.pyplot as plt

import data_io as io

import pvlib as pv

import tiles

#########
# Setup.
folder_data = 'data'
fname_config = 'config.yml'

#####################################
# Do it.
path_module = os.path.dirname(os.path.abspath(__file__))
path_data = os.path.join(path_module, folder_data)

# Read config file.
f = os.path.join(path_data, fname_config)
info = io.read(f)

#
# Loop over reference images, carve out selected grid and rack tiles.
#
for fname_img, info_img in info['reference']['grid'].items():

    f = os.path.join(path_data, 'reference', fname_img)
    img, meta = io.read(f)

    tiles_grid, tiles_rack = tiles.carve_tiles(img, info)

    print(fname_img)
    
    # Save specified tiles to files.
    for label, ij in info_img.items():
        print(ij)
        for mn, tile in tiles_grid:
            # Got a match?
            if ij == mn:
                print(label)

                fname = 'tile_grid_%s.png' % (label)
                f = os.path.join(path_data, 'tiles', fname)
                io.write(f, tile)

                

for fname_img, info_img in info['reference']['rack'].items():
    f = os.path.join(path_data, 'reference', fname_img)
    img, meta = io.read(f)

    tiles_grid, tiles_rack = tiles.carve_tiles(img, info)

    # Save specified tiles to files.
    for label, ij in info_img.items():
        for mn, tile in tiles_rack:
            # Got a match?
            if ij == mn:
                print(label)

                fname = 'tile_rack_%s.png' % (label)
                f = os.path.join(path_data, 'tiles', fname)
                io.write(f, tile)

# Done.

#
# Display.
#
img_display = None
if img_display is not None:
    fig = plt.figure(1)
    fig.clear()

    ax = fig.add_subplot(1, 1, 1)
    pv.imshow(img_display)

    ax.vlines(i_grid, j0_grid, j0_grid+dx_grid*num_grid_y, color='cyan')
    ax.hlines(j_grid, i0_grid, i0_grid+dx_grid*num_grid_x, color='cyan')

    ax.vlines(i_rack, j0_rack, j0_rack+dx_rack*num_rack_y, color='cyan')
    ax.hlines(j_rack, i0_rack, i0_rack+dx_rack*num_rack_x, color='cyan')

    for ix, i in enumerate(i_grid):
        s = '%s' % ix
        xy = (i+dx_grid*.5, j0_grid-5)
        ax.annotate(s, xy)

    for ix, j in enumerate(j_grid):
        s = '%s' % ix
        xy = (i0_grid, j+dx_grid*.7)
        ax.annotate(s, xy)

    plt.draw()



    # fig = plt.figure(2)
    # fig.clear()

    # # i, j = 4, 6
    # i, j = 10, 10
    # ax = fig.add_subplot(1, 1, 1)
    # pv.imshow(tiles_grid[j, i])

    # plt.draw()



    # fig = plt.figure(3)
    # fig.clear()

    # i = 6
    # ax = fig.add_subplot(1, 1, 1)
    # pv.imshow(tiles_rack[i])

    # plt.draw()



    # Done.
    plt.show()
