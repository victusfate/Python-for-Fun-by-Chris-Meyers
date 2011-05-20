#   w a v e . p y
#
import sys
from Tkinter import *
from math    import *

class wave :
	def __init__ (self, points=400, formula=None) :
		self.data = [0.0]*points
		self.points= points
		if formula :
			for p in range(points) :
				x = p*pi*2/points
				self.data[p] = eval(formula)

	def __add__ (self, other) :
		target = wave(points=self.points)
		for i in range(self.points) :
			target.data[i] = self.data[i] + other.data[i]
		return target

	def __mul__ (self, other) :
		target = wave(points=self.points)
		if type(other) == type(5) or type(other) == type(5.0) :
			for i in range(self.points) :
				target.data[i] = self.data[i] * other
		else :
			for i in range(self.points) :
				target.data[i] = self.data[i] * other.data[i]
		return target

	def __sub__ (self, other) :
		target = wave(points=self.points)
		for i in range(self.points) :
			target.data[i] = self.data[i] - other.data[i]
		return target

	def integral(self) :
		ans = 0.0
		for pt in self.data : ans = ans+pt
		return ans*2*pi/self.points

	def plot (self, title="??", pixHeight=None, maxY=None, others=[]) :
		if not pixHeight : pixHeight = self.points*2/3   # Pleasant ratio
		pixWidth = self.points
		# find max and min data to scale
		if not maxY :
			maxY = max (max(self.data), -min(self.data))
		offset = pixHeight/2
		scale = offset/maxY

		win = Tk()
		win.title (title)
		canvas = Canvas(win,width=pixWidth,height=pixHeight)
		# create zero line
		canvas.create_line(0,offset,pixWidth,offset)
		canvas.pack()

		self.plotOne (canvas, pixWidth, scale, offset)
		for i in range(len(others)) :
			others[i].plotOne (canvas, pixWidth, scale, offset)
		if sys.platform == "win32" : win.mainloop()

	def plotOne (self, canvas, pixWidth, scale, offset) :
		for x in range(pixWidth) :
			y = offset - self.data[x] * scale
			if x : canvas.create_line(x-1,yprev,x,y)
			yprev = y

	def fft (self) :
		work = self * 1   # Harmonics will be stripped from this
		for harm in range(1,10) :
			formula="-sin(%d*x)" % harm
			area = (wave(formula=formula)*work).integral()
			amplitude = area/-pi
			if amplitude > .000001 :
				 print "Harmonic=",harm, " Amplitude=%.04f" % amplitude
			takeAway = wave(formula="sin(%d*x) * %f" % (harm,amplitude))
			work = work-takeAway

def test() :
	p1 = wave(formula="sin(x)/1")
	p3 = wave(formula="sin(3*x)/3")
	p5 = wave(formula="sin(5*x)/5")
	mys = p1+p3+p5
	mys.fft()

if __name__ == "__main__" : test()
