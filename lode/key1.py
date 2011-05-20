#!/usr/bin/env python
#
import ttyLinux, time

def test() :
	ttyLinux.setSpecial()
	for i in range(10) :
		time.sleep(1)
		keys = ttyLinux.readLookAhead()
		print "Got", [keys]
	ttyLinux.setNormal()
	
