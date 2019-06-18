from Tkinter import *
from board_defs import *
from scrabble_tiles import *

class Rack(Frame):
	Tiles = ['A','B','C','D','E','F','G']

	def __init__(self, master=None):
		self.Toplevel = Toplevel()
		Frame.__init__(self, self.Toplevel)
		self.create_canvas()
		self.pack()

	def create_canvas(self):
		self.Width = Cell * 8
		self.Height = Cell
		self.draw = Canvas (self, {"width":`self.Width`, 'height':`self.Height`})
		self.draw.create_line(0,0,self.Width,0)
		self.draw.create_line(0,0,0,self.Height)
		self.draw.create_line(0,self.Height,self.Width,self.Height)
		self.draw.create_line(self.Width, 0, self.Width, self.Height)
		self.display_letters()
		self.draw.pack()

	def display_letters(self):
		x = 0
		for i in self.Tiles:
			draw_tile(self.draw, i, (x+0.5)*Cell+(x+0.5)*Cell/len(self.Tiles), Cell/2)
			x=x+1
