import regsub
from dat import *

def start(x,y,o,n):
	if o == 'v':
		y = y - n + 1
	else:
		x = x - n + 1
	return x,y

def next(x,y,c):
	if c == 'v':
		y = y +1
	else:
		x = x +1
	return x,y

class Board:
	def __init__(self):
		self.square = square
		self.special = special

	def reset(self):
		for x in range(len(self.square)):
			for y in range(len(self.square[x])):
				self.square[x][y]=EMPTY

	def newletters(self,x,y,o,word):
		# return list of (x,y,ch) tuples (all the newly placed letters)
		list=[]
		word = regsub.gsub(BLANK,'',word)	# remove trailing _
		x,y = start(x,y,o,len(word))
		for ch in word:
			if self.square[x][y] == EMPTY:
				list.append(x,y,ch)
			x,y = next(x,y,o)
		return list

	def getword (self, x, y, o, word, rack):
		# Given requested word,endpoint and orientation,
		# and rack to draw letters from:
		# Return the word (with blanks shown if necessary)
		# or raise an exception if we can't do it with this rack
		print 'getword', x, y, o, word, rack
		r2 = rack[:]
		newword=''
		x,y = start(x,y,o,len(word))
		try:
			for ch in word:
				if self.square[x][y] == EMPTY:
					if ch in r2:
						newword = newword+ch
						r2.remove(ch)
					elif BLANK in r2:
						newword = newword + ch + BLANK
						r2.remove(BLANK)
					else:
						print "missing ",ch
						raise Badmove, "needed a " + ch + "for" + `x,y`
				else:
					if ch == self.square[x][y]:
						newword = newword + ch
					else:
						raise Badmove, "expected "+ch+"at "+`x,y`
				x,y = next(x,y,o)
		except IndexError:
			raise Badmove, "doesn't fit"
		return newword

	def play (self, list):
		for x,y,ch in list:
			self.square[x][y] = ch
