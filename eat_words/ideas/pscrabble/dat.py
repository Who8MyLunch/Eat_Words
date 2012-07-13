squaresize = 48
RACKSIZE=7
BLANK='_'
EMPTY=' '
Badmove = "illegal move attempted"	# exception

# location of special squares 
# T triple word
# t triple letter
# D double word
# d double letter
# S star	(double word in center of board)

special = [
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

square = [
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
]
# points for each letter
scores ={	
	'a':1, 'b':3, 'c':3, 'd':2, 'e':1, 'f':4, 'g':2, 'h':4, 'i':1,
	'j':8, 'k':5, 'l':1, 'm':3, 'n':1, 'o':1, 'p':3, 'q':10, 'r':1,
	's':1, 't':1, 'u':1, 'v':4, 'w':4, 'x':8, 'y':4, 'z':10, '_':0
};

boardsquares = len(special)
boardsize = squaresize * (boardsquares+1)

colorspecial = {
	'T':{'bitmap':'@bitmap/tw.xbm','background':	'red'},
	'D':{'bitmap':'@bitmap/dw.xbm','background':	'pink'},
	'S':{'bitmap':'@bitmap/star.xbm','background':	'pink'},
	't':{'bitmap':'@bitmap/tl.xbm','background':	'blue'},
	'd':{'bitmap':'@bitmap/dl.xbm','background':	'light blue'},
	' ':{'bitmap':'@bitmap/blank.xbm','background':	'grey'}
}
bwspecial = {
	'T':{'bitmap':'@bitmap/tw.xbm'},
	'D':{'bitmap':'@bitmap/dw.xbm'},
	'S':{'bitmap':'@bitmap/star.xbm'},
	't':{'bitmap':'@bitmap/tl.xbm'},
	'd':{'bitmap':'@bitmap/dl.xbm'},
	' ':{'bitmap':'@bitmap/blank.xbm'}
}

helpmsg = '''
Drag a line with the mouse to indicate where you want to place a word,
and type the whole word,then press return.

From the 'Game' menu,you can choose to have the computer move for you,
or "Pass": which means you turn all your letters in,and redraw from
the bag.
'''
