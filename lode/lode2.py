#!/usr/bin/env python
#
#   l o d e 2 . p y
#
import time, ttyLinux
from util import *

class You :
	def __init__ (self, Row=1, Col=10, Face='^') :
		self.row = Row; self.col = Col; self.face=Face
		self.dir = (0,0)

	def setDirection (self, keys) :
		if not keys : return
		if keys == '\033[A' : self.dir=( 0, 1)  # up
		if keys == '\033[B' : self.dir=( 0,-1)  # down
		if keys == '\033[C' : self.dir=( 1, 0)  # right
		if keys == '\033[D' : self.dir=(-1, 0)  # left

	def move (self) :
		spot = getSpot(self.row,self.col)
		horz,vert = self.dir
		writeScreen(self.row,self.col,spot)
		if   spot == '_' : self.col += horz  # by left/right arself.row
		elif spot == '|' : self.row -= vert  # by up/down arrow
		elif spot == ' ' : self.row += 1     # always fall in air
		writeScreen(self.row,self.col,self.face)

def main () :
	setBoard(0)
	try :
		ttyLinux.setSpecial()
		playGame()
	finally : ttyLinux.setNormal()

def playGame() :
	writeBoard ()
	you = You()
	while 1 :
		time.sleep(.1)
		keys = ttyLinux.readLookAhead()
		you.setDirection(keys)
		you.move()
		writeScreen (20,0,'')
	writeScreen (20,0,'')

if __name__ == "__main__" : main()
