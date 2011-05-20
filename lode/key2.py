#!/usr/bin/env python
#
import ttyLinux, time

def loop() :
	for i in range(10) :
		time.sleep(1)
		keys = ttyLinux.readLookAhead()
		print "Got", [keys]
	
def test() :
	try :
		ttyLinux.setSpecial()
		loop()
	finally : ttyLinux.setNormal()

