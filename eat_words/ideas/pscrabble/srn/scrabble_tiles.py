from Tkinter import *
from board_defs import *

def draw_tile(canvas, letter, x, y):
 	canvas.create_bitmap(x, y, {'bitmap':BaseName+letter+'.xbm', 'background':'ivory'})
	canvas.create_text(x  + Cell/5, y+Cell/5,
	     {'text':`Scores[letter]`, 'font':'-b&h-lucida-medium-r-normal-sans-12-*-*-*-p-*-iso8859-1'})
