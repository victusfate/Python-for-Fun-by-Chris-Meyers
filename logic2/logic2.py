#!/usr/local/bin/python
#
from logic import *

class Nand (Gate2) :       # two input NAND Gate
	def __init__ (self, name) :
		Gate2.__init__ (self, name)
	def evaluate (self) :
		self.C.set(not(self.A.value and self.B.value))

class Latch (LC) :
	def __init__ (self, name) :
		LC.__init__ (self, name)
		self.A = Connector(self,'A',1)
		self.B = Connector(self,'B',1)
		self.Q = Connector(self,'Q',monitor=1)
		self.N1 = Nand ("N1")
		self.N2 = Nand ("N2")
		self.A.connect ([self.N1.A])
		self.B.connect ([self.N2.B])
		self.N1.C.connect ([self.N2.A, self.Q])
		self.N2.C.connect ([self.N1.B])

class DFlipFlop (LC) :
	def __init__ (self, name) :
		LC.__init__ (self, name)
		self.D = Connector(self,'D',1)
		self.C = Connector(self,'C',1)
		self.Q = Connector(self,'Q')
		self.Q.value=0
		self.prev=None

	def evaluate (self) :
		if self.C.value==0 and self.prev==1 :  #clock drop
			self.Q.set(self.D.value)
		self.prev = self.C.value

class Div2 (LC) :
	def __init__ (self, name) :
		LC.__init__ (self, name)
		self.C = Connector(self,'C',activates=1)
		self.D = Connector(self,'D')
		self.Q = Connector(self,'Q',monitor=1)
		self.Q.value=0
		self.DFF = DFlipFlop('DFF')
		self.NOT = Not('NOT')
		self.C.connect ([self.DFF.C])
		self.D.connect ([self.DFF.D])
		self.DFF.Q.connect ([self.NOT.A,self.Q])
		self.NOT.B.connect ([self.DFF.D])
		self.DFF.Q.activates = 1
		self.DFF.D.value = 1 - self.DFF.Q.value

class Counter (LC) :
	def __init__ (self, name) :
		LC.__init__ (self, name)
		self.B0 = Div2('B0')
		self.B1 = Div2('B1')
		self.B2 = Div2('B2')
		self.B3 = Div2('B3')
		self.B0.Q.connect( self.B1.C )
		self.B1.Q.connect( self.B2.C )
		self.B2.Q.connect( self.B3.C )

def testDivBy2 () :
	x = Div2("X")
	c = 0; x.C.set(c)
	while 1 :
		raw_input("Clock is %d. Hit return to toggle clock" % c)
		c = not c
		x.C.set(c)

def testCounter () :
	x = Counter("x")    # x is a four bit counter
	x.B0.C.set(1)       # set the clock line 1
	while 1 :
		print "Count is ", x.B3.Q.value, x.B2.Q.value,
		print              x.B1.Q.value, x.B0.Q.value,
		ans = raw_input("\nHit return to pulse the clock")
		x.B0.C.set(0)   # toggle the clock
		x.B0.C.set(1)

def testLatch () :
	x = Latch("ff1")
	x.A.set(1); x.B.set(1)
	while 1 :
		ans = raw_input("Input A or B to drop:")
		if ans == "" : break
		if ans == 'A' : x.A.set(0); x.A.set(1)
		if ans == 'B' : x.B.set(0); x.B.set(1)

testDivBy2()
