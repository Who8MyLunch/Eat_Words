from Tkinter import *
import posix, string, sys
from menubar import MenuBar
from board_defs import *
from scrabble_rack import *
import scrabble_tiles

def dummy_function():
	pass

def quit_game():
	sys.exit(0)

def test(event):
	print event

class Board(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.menubar = MenuBar(self)
                self.menubar.master.pack({'side':'top', 'fill':'x'})
                self.menubar.pack({'fill':'x'})
		self.create_file_menu()
		self.Squares = Squares
		self.create_canvas()
		self.pack()

	def create_file_menu(self):
		self.file = self.menubar.new('File')
		self.file.add('command', {'label':'Quit', 'command':quit_game})

	def create_canvas(self):
		BoardWidth = Cell * 15
		self.draw = Canvas(self, {"width" : `BoardWidth`, "height" : `BoardWidth`})
		for x in range(16):
			self.draw.create_line(x * Cell,0, x * Cell, BoardWidth)
			self.draw.create_line(0, x * Cell, BoardWidth, x * Cell)
			self.draw.create_line(x * Cell-1,0, x * Cell-1, BoardWidth)
			self.draw.create_line(0, x * Cell-1, BoardWidth, x * Cell-1)
		for x in range(15):
			for y in range(15):
				self.draw.create_bitmap(x*Cell+Cell/2, y*Cell+Cell/2,
				Bitmaps[self.Squares[x][y]])

#		Widget.bind(self.draw, '<Button-1>', test)
		self.draw.pack({'side': 'left'})

	def place_tile(self, row, column, letter):
		self.draw.create_bitmap(row*Cell+Cell/2, column*Cell+Cell/2, 
			{'bitmap':BaseName+letter+'.xbm', 'background':'ivory'})

b = Board()
b.place_tile(4,4,'Z')
r = Rack()
b.mainloop()
