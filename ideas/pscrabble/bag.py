import whrandom
from dat import *

class Bag:
	def __init__(self):
		self.reset()

	def reset(self):
		self.list=reduce(lambda x,y: x+[y],
				'aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmmnnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz__', [])

	def grab(self, n):
		retval=[]
		for i in range(min(n,len(self.list))):
			c = whrandom.choice(self.list)
			self.list.remove(c)
			retval.append(c)
		return retval

	def swap(self,rack):
		self.list = self.list + rack
		return self.grab(RACKSIZE)
