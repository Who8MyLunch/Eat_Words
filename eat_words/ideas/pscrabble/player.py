import scrabble
from dat import *

def r2s(rack):
	return reduce (lambda x,y: x+y, rack, '')

class Player:
	def __init__(self, screen, board, bag):
		self.rack = bag.grab(RACKSIZE)
		self.score = 0
		self.screen = screen
		self.board = board
		self.bag = bag

	def reset(self):
		self.rack = self.bag.grab(RACKSIZE)
		self.score = 0

	def pass_turn(self):
		self.rack = self.bag.swap(self.rack)

	def rackempty(self):
		return not len(self.rack)

	def trypoints(self, sx,sy,ex,ey):
		# given the endpoints the user has selected, return
		# a list of (x,y,o) tuples
		# where x,y is the end of the word, o is orientation: 'h' or 'v'
		deltas=[0,1,-1,2,-2]
		if sx == ex:
			if sy>ey:
				ey,ex = sy,sx
			return map(lambda dy,x=ex,y=ey: (x,y+dy,'v'), deltas)
		else:
			if sx>ex:
				ey,ex = sy,sx
			return map(lambda dx,x=ex,y=ey: (x+dx,y,'h'), deltas)

	def hmove(self,word,sx,sy,ex,ey):
		for x,y,o in self.trypoints(sx,sy,ex,ey):
			try:
				self.trymove(x,y,o,word)
				return		# if no exception
			except Badmove, reason:
				continue
			except ValueError, reason:
				continue
		raise Badmove, "exhausted all options"

	def trymove(self, x,y,o,word):
		word = self.board.getword(x,y,o,word,self.rack)
		score = scrabble.scoremove(x,y,o,word)
		self.move(x,y,o,word)

	def cmove(self):
		try:
			x,y,o,word =  scrabble.findmove(r2s(self.rack))
			self.move(x,y,o,word)
		except ValueError:
			self.screen.message("Computer couldn't find a move")
			self.pass_turn()

	def move(self,x,y,o,word):
		self.score = self.score + scrabble.scoremove(x,y,o,word)
		scrabble.makemove(x,y,o,word)
		list = self.board.newletters(x,y,o,word)
		self.screen.showmove(list)
		self.board.play(list)
		self.replenish(list)

	def replenish(self, list):
		for x,y,ch in list:
			if ch in self.rack:
				self.rack.remove(ch)
			else:
				self.rack.remove(BLANK)

		self.rack = self.rack + self.bag.grab(RACKSIZE - len(self.rack))
