
from __future__ import division, print_function, unicode_literals

import numpy as np



class Board(object):
    """
    A scrabble board.
    """

    def __init__(self):
        """
        Instantiate a new board class.
        Set multipliers.
        No letters on the board.
        """

        # Component boards.
        self.width = 15 + 2   # includes moat
        shape = (self.width, self.width)

        self.letters = np.zeros(shape, dtype='|S1')
        self.xL = np.ones(shape, dtype=np.uint8)
        self.xW = np.ones(shape, dtype=np.uint8)

        self.blank = '.'
        
        self.playables = np.zeros(shape, dtype='|S7')
        
        self.reset()
        
        # Done.
    

    def reset(self):
        """
        Reset board to clean slate.
        """
        
        self.letters[:] = self.blank
        self._anchors = None
        self._clear_tiles = None

        self._player_moves = []
        
        self.initialize_multipliers()
        
        # Done.
        
        
    def __repr__(self):
        """
        Nice class visualization.
        """

        s = '\n' + \
            '      1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 \n' + \
            '     ---------------------------------------------\n'

        pretty_letters = self.letters.copy()
        for i,j in self.anchors:
            pretty_letters[i, j] = '+'

        for j in range(1, self.width-1):
            r = [j]
            r.extend( [L[0].upper() for L in pretty_letters[1:-1, j]] )

            rs = ' %2d | %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s  %1s |\n' % tuple(r)
            s += rs

        s += '     ---------------------------------------------\n'

        # Done.
        return s



    def initialize_multipliers(self):
        """
        Set default values for letter and word multipliers.
        """

        # First quadrant.
        ij_DL = [[3, 2],
                 [2, 3],
                 [5, 3],
                 [3, 5],
                 [7, 5],
                 [5, 7]]

        ij_TL = [[7, 1],
                 [4, 4],
                 [6, 6],
                 [1, 7]]

        ij_DW = [[6, 2],
                 [8, 4],
                 [2, 6],
                 [4, 8]]

        ij_TW = [[4, 1],
                 [1, 4]]

        # DL.
        for i,j in ij_DL:
            self.xL[i, j] = 2                             # Q1
            self.xL[self.width-i-1, j] = 2                # Q2
            self.xL[self.width-i-1, self.width-j-1] = 2   # Q3
            self.xL[i, self.width-j-1] = 2                # Q4

        # TL.
        for i,j in ij_TL:
            self.xL[i, j] = 3                             # Q1
            self.xL[self.width-i-1, j] = 3                # Q2
            self.xL[self.width-i-1, self.width-j-1] = 3   # Q3
            self.xL[i, self.width-j-1] = 3                # Q4

        # DW.
        for i,j in ij_DW:
            self.xW[i, j] = 2                             # Q1
            self.xW[self.width-i-1, j] = 2                # Q2
            self.xW[self.width-i-1, self.width-j-1] = 2   # Q3
            self.xW[i, self.width-j-1] = 2                # Q4

        # TW.
        for i,j in ij_TW:
            self.xW[i, j] = 3                             # Q1
            self.xW[self.width-i-1, j] = 3                # Q2
            self.xW[self.width-i-1, self.width-j-1] = 3   # Q3
            self.xW[i, self.width-j-1] = 3                # Q4

            
        # Moat around the edges.
        self.xL[ 0, :] = 0
        self.xL[-1, :] = 0
        self.xL[:,  0] = 0
        self.xL[:, -1] = 0

        self.xW[ 0, :] = 0
        self.xW[-1, :] = 0
        self.xW[:,  0] = 0
        self.xW[:, -1] = 0

        # Done.


    #########################################
    # Line stuff.
    def get_line(self, j):

        # Get the board letters.
        line = self.letters[:, j]
        
        # Identify anchor points.
        for i in range(self.width):
            if self._cell_is_anchor( (i, j) ):
                line[i] = '+'
                
        # Playable letters.
        playable = np.zeros(self.width, dtype='|S7')
        
        # Update.
        for i in range(self.width):
            if line[i] == '+':
                playable[i] = self.playables[i, j]
        
        # Done.
        return line, playable
    
    #########################################
    def set_game_letters(self, ij_letters):
        """
        PLace initial game letters on the board.  Clobber any multipliers underneath.
        """
        for ij, letter in ij_letters:
            i, j = ij
            self.letters[i, j] = letter
            self.xL[i, j] = 1
            self.xW[i, j] = 1


        self._anchors = None
        # Done.

        
    def play_letters(self, ij_letters):
        """
        Place new letters on the board.
        This represents a possible move by the player.
        This operation may be undone.
        """
        
        self._anchors = None
        
        # Undo prior candidate moves, if any.
        self.undo_play_letters()
        self._player_moves = []
        
        # Play the letters.
        for ij, L in ij_letters:
            i, j = ij
            
            # Only allowed to apply a move to a blank tile.
            assert(self.letters[i, j] == self.blank)
            self.letters[i, j] = L
            
            # Store move for later undo.
            self._player_moves.append( (ij, L) )
        
        # Done.
        
        
    def unplay_letters(self):
        """
        Undo just-played letters.
        """
        count = 0
        for ij, L in self._player_moves:
            count += 1
            # Verify letter.
            i, j = ij
            assert(L == self.letters[i, j])

            # Remove it.
            self.letters[i, j] = self.blank
            
        # Done.
        self._player_moves = []
        
        return count
        
    ##############################################
    
    @property
    def clear_tiles(self):
        """
        List of non-anchor empty tiles.
        """
        if self._clear_tiles is None:
            self._clear_tiles = []
            for i in range(self.width):
                for j in range(self.width):
                    ij = i, j
                    if not self._cell_is_letter(ij) and not ij in self.anchors:
                        self._clear_tiles.append(ij)

        return self._clear_tiles
        
    
    @property
    def anchors(self):
        """
        List of anchor points' coordinates.
        """
        if self._anchors is None:
            self._clear_tiles = None
            self._anchors = []
            for i in range(self.width):
                for j in range(self.width):
                    ij = i, j
                    if self._cell_is_anchor(ij):
                        self._anchors.append(ij)

        return self._anchors



    def _cell_is_anchor(self, (i, j) ):
        """
        Determine if given cell is an anchor.
        Return True or False.
        """

        # # valid cell?
        # if not self.valid_cell_coordinates( (i, j) ):
            # raise Exception('Invalid cell coordinates: %d, %d.' % (i, j) )

        # Check for moat.
        if i == 0 or i == self.width-1:
            return False

        if j == 0 or j == self.width-1:
            return False

        # Check self.
        if self.letters[i, j] != self.blank:
            return False

        # Check the four neighbors.
        have_neighbor = False

        # Check above, below, left and right.
        if self._cell_is_letter( (i, j-1) ):
            have_neighbor = True

        if self._cell_is_letter( (i, j+1) ):
            have_neighbor = True

        if self._cell_is_letter( (i-1, j) ):
            have_neighbor = True

        if self._cell_is_letter( (i+1, j) ):
            have_neighbor = True

        # Done.
        return have_neighbor


        
    def _cell_is_letter(self, (i, j) ):
        """
        Return True if cell coordinates map to a valid letter.
        """
        L = self.letters[i, j]
        return self._value_is_letter(L)
        

    def _value_is_letter(self, L):
        """
        Return True if character is a valid letter.
        """
        return not (L == self.blank)


        
    ############################

    def contiguous_vertical(self, (i, j) ):
        """
        Find contiguous set of letters connected to cell (i, j) in vertical direction.
        Return starting ij and letters.
        """
        line = self.letters[i, :]
        k, num = self._contiguous(line, j)

        ik = i, k

        letters = self.letters[i, k:k+num].tostring()

        return ik, letters


    def contiguous_horizontal(self, (i, j) ):
        """
        Find contiguous set of letters connected to cell ij in horizontal direction.
        Return starting ij and letters.
        """
        line = self.letters[:, j]
        k, num = self._contiguous(line, i)

        kj = k, j

        letters = self.letters[k:k+num, j].tostring()
        
        return kj, letters


    def _contiguous(self, line, k):
        """
        Search for contiguous letters in a row or column, crossing over position k.
        Return starting index and number of letters.
        """
        width = len(line)

        # Check initial point.
        if line[k] == self.blank:
            # Nothing here.
            return -1, 0

        # Search backwards.
        k_beg = k
        while self._value_is_letter(line[k_beg]):
            k_beg -= 1
        k_beg += 1

        # Search forwards.
        k_end = k
        while self._value_is_letter(line[k_end]):
            k_end += 1
        k_end -= 1

        # Verify start & end points are inside the moat.
        assert( 1 <= k_beg <= width-2)
        assert( 1 <= k_end <= width-2)

        num = k_end - k_beg + 1

        # Done.
        return k_beg, num



if __name__ == '__main__':
    """
    Testing.
    """
    b = Board()

    print(b)

    some_letters = [(( 5,  5), 'b'),
                    (( 6,  5), 'o'),
                    (( 7,  5), 'y'),
                    (( 6,  4), 't'),
                    (( 6,  6), 't'),
                    (( 6,  7), 'e'),
                    (( 6,  8), 's'),
                    (( 7,  8), 'p'),
                    (( 8,  8), 'e'),
                    (( 9,  8), 'c'),
                    ((10,  8), 'i'),
                    ((11,  8), 'a'),
                    ((12,  8), 'l'),
                    (( 9,  7), 'a'),
                    (( 9,  9), 'e'),
                    (( 9, 10), 's'),
                    ]


    b.set_game_letters(some_letters)

    print(b)

    more_letters = [((12,  7), 'o'),
                    ((12,  9), 'd'),
                    ((12, 10), 's')]
                    
    b.play_letters(more_letters)
    print(b)


    print(b.contiguous_horizontal( (5,5) ))
    print(b.contiguous_horizontal( (6,8) ))
    print(b.contiguous_vertical( (6,8) ))
    print(b.contiguous_vertical( (1,1) ))
