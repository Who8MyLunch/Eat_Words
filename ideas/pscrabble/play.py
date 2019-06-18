#!/usr/pgrad/gary/bin/sun4d/python
import screen, bag, board, player, string, sys, scrabble
from dat import *

def __init__(self,screen, board, bag, human, computer):
	self.s = screen
	self.board = board
	self.bag = bag
	self.human = human
	self.computer = computer

def pass_turn():
	human.pass_turn()
	human_moved()

def help():
	s.message(helpmsg)

def savegame():
	s.message("can't save game")

def newgame():
	for i in [human,computer, board,bag, s, scrabble]:
		i.reset()
	s.refresh_rack(human.rack)
	s.refresh_score(`human.score`, `computer.score`)

def hint():
	human.cmove()
	human_moved()

def human_moved():
	human.rack.sort()
	s.refresh_rack(human.rack)
	if human.rackempty():
		gameover()
		return
	computer.cmove()	
	if computer.rackempty():
		gameover()
		return
	s.refresh_score(`human.score`, `computer.score`)

def trymove(word, sx,sy, ex, ey):
	try:
		human.hmove(word, sx,sy, ex, ey)
		human_moved()
	except Badmove, reason:
		s.message ("can't put "+word+" there, sorry")

def gameover():
	hpoints = reduce(lambda x,y:x+scores[y], human.rack, 0)
	cpoints = reduce(lambda x,y:x+scores[y], computer.rack, 0)
	cscore = computer.score + hpoints - cpoints
	hscore = human.score + cpoints - hpoints
	msg = "My mighty score "+`cscore`+"\n your feeble effort "+`hscore`
	s.gameoverdialog(msg)
	newgame()

# main
#
if __name__ == '__main__':
	menus = [
		('File',[('New',newgame),('Help',help),('Quit',gameover)]),
		('Game',[('Move for me',hint),('Pass',pass_turn),('Over',gameover)])
		]
	s = screen.Screen(menus,trymove)
	s.master.maxsize(1280,1024)
	bag = bag.Bag()
	board = board.Board()
	human = player.Player(s, board, bag)
	computer = player.Player(s, board, bag)
	s.refresh_rack(human.rack)
	s.mainloop()
