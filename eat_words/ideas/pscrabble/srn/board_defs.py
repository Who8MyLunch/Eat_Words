# This file defines the board layout, as well as some other information
# about the bitmaps.

BaseName = '@/usr/home/srn/work/scrabble/bitmaps/'
Bitmaps = {
	'D':{'bitmap':BaseName + 'DW.xbm', 'background':'pink'},
	'd':{'bitmap':BaseName + 'DL.xbm', 'background':'sky blue'},
	'T':{'bitmap':BaseName + 'TW.xbm', 'background':'red'},
	't':{'bitmap':BaseName + 'TL.xbm', 'background':'blue'},
	' ':{'bitmap':BaseName + 'Blank.xbm', 'background':'light yellow'},
	'S':{'bitmap':BaseName + 'Star.xbm', 'background':'pink'}
}

Squares = [
        ['T',' ',' ','d',' ',' ',' ','T',' ',' ',' ','d',' ',' ','T'],
        [' ','D',' ',' ',' ','t',' ',' ',' ','t',' ',' ',' ','D',' '],
        [' ',' ','D',' ',' ',' ','d',' ','d',' ',' ',' ','D',' ',' '],
        ['d',' ',' ','D',' ',' ',' ','d',' ',' ',' ','D',' ',' ','d'],
        [' ',' ',' ',' ','D',' ',' ',' ',' ',' ','D',' ',' ',' ',' '],
        [' ','t',' ',' ',' ','t',' ',' ',' ','t',' ',' ',' ','t',' '],
        [' ',' ','d',' ',' ',' ','d',' ','d',' ',' ',' ','d',' ',' '],
        ['T',' ',' ','d',' ',' ',' ','S',' ',' ',' ','d',' ',' ','T'],
        [' ',' ','d',' ',' ',' ','d',' ','d',' ',' ',' ','d',' ',' '],
        [' ','t',' ',' ',' ','t',' ',' ',' ','t',' ',' ',' ','t',' '],
        [' ',' ',' ',' ','D',' ',' ',' ',' ',' ','D',' ',' ',' ',' '],
        ['d',' ',' ','D',' ',' ',' ','d',' ',' ',' ','D',' ',' ','d'],
        [' ',' ','D',' ',' ',' ','d',' ','d',' ',' ',' ','D',' ',' '],
        [' ','D',' ',' ',' ','t',' ',' ',' ','t',' ',' ',' ','D',' '],
        ['T',' ',' ','d',' ',' ',' ','T',' ',' ',' ','d',' ',' ','T']
]

# This is the size of a "hole" in the board - bitmaps are Cell - 2.

Cell = 45

Scores ={       
        'A':1, 'B':3, 'C':3, 'D':2, 'E':1, 'F':4, 'G':2, 'H':4, 'I':1,
        'J':8, 'K':5, 'L':1, 'M':3, 'N':1, 'O':1, 'P':3, 'Q':10, 'R':1,
        'S':1, 'T':1, 'U':1, 'V':4, 'W':4, 'X':8, 'Y':4, 'Z':10, '_':0
};


