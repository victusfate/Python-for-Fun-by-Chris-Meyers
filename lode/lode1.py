#!/usr/bin/env python
#
#  lode1.py - simple game loop
from util import *
import time

def main () :
	setBoard(0)
	writeBoard ()
	time.sleep(2)
	writeScreen (3,10,'^')
	row=3; col=10
	while 1 :
		spot = getSpot(row,col)
		writeScreen(row,col,spot)
		if   spot == '_' : col += 1
		elif spot == '|' : row -= 1
		elif spot == ' ' : row += 1
		else : break
		writeScreen(row,col,'^')
		writeScreen (20,0,'')
		time.sleep(.1)
	writeScreen (20,0,'')
	
if __name__ == "__main__" : main()
