#!/usr/local/bin/python
#
#	r t n . p y
#
#	Based on states labeled as numbers
#	Arcs contain what to match in order to advance to next state
#
from __future__ import generators
import random
END   = None
debug = 1

def gen1(net) :
	"Generate random sentence from simple net. Non recursive"
	p = net[1]; s = ""
	while 1 :
		choose = random.randrange(len(p))
		s = s + " " + p[choose][0]
		next = p[choose][1]
		if next == END : return s
		p = net[next]

def gen2(network, name) :
	"Generate random sentence, allow recursive network"
	net = network.get(name)
	if not net : return name     # terminal node
	p = net[1]; s = ""
	while 1 :
		choose = random.randrange(len(p))
		s = s + " " + gen2(network, p[choose][0])
		next = p[choose][1]
		if next == END : return s
		p = net[next]

def gen3(network, label, state) :
	"Use generator to yield all possible sentences"
	if not network.get(label) : yield label  # if not a subnet stands for itself
	elif state == END         : yield ""     # no state. end of road
	else :
		net = network[label]
		p = net[state]; s = ""
		for labl,nextState in p :
			for word in gen3(network,labl,1) :
				for rest in gen3(network,label,nextState) :
					yield word + " " + rest

def dbg (ind, mesg) :
	"Print value at proper indent, pass it back unchanged"
	if debug : print "dbg",".  "*ind + str(mesg)
	return mesg

def match1a(network, label, state, input,ind=0) :
	"match1 with nested diagnostic tracing"
	ind += 1
	dbg(ind, "Entering label=%s state=%s" %(label,state))
	if   state == END : yield input[:]
	elif not input    : dbg(ind, "Returning"); return
	elif not network.get(label) :
		if label == ""       : yield input[0:]  # empty = free pass
		if label == input[0] : yield input[1:]  # A match. yield remaining input
	else :
		net = network[label]
		p = net[state]; s = ""
		for labl,nextState in p :
			for input1 in match1a(network,labl, 1, input,ind) :
				for rest in match1a(network,label,nextState, input1, ind) :
					yield dbg(ind,rest)

def match1(network, label, state, input) :
	if   state == END : yield input[:]
	elif not input    : return
	elif not network.get(label) :
		if label == ""       : yield input[0:]  # free pass
		if label == input[0] : yield input[1:]
	else :
		net = network[label]
		p = net[state]; s = ""
		for labl,nextState in p :
			for input1 in match1(network,labl, 1, input) :
				for rest in match1 (network,label,nextState, input1) :
					yield rest

def match2(network, label, state, input,ind=0) :
	if   state == END : yield input[:],None
	elif not input    : return
	elif not network.get(label) :
		if label == ""       : yield input[0:],label  # free pass
		if label == input[0] : yield input[1:],label
	else :
		net = network[label]
		p = net[state]; s = ""
		trace = [label]
		for labl,nextState in p :
			sav1 = trace[:]
			for input1,trace1 in match2(network,labl,1,input) :
				if trace1 : trace.append(trace1)
				sav2 = trace[:]
				for rest,trace2 in match2(network,label,nextState,input1) :
					if trace2 : trace = trace + list(trace2[1:])
					yield rest, tuple(trace[:])
					trace = sav2[:]
				trace = sav1[:]

def match3 (network, label, state, input) :
	"Use generator to yield all possible matching sentences that consume input"
	import string
	for input,trace in match2(network, label, state, input) :
		if not input : yield trace

if __name__ == "__main__" :
	import simple, sys, english
#	print gen1(simple.net1['sentence'])
#	print gen2(simple.net2, 'sentence')
#	pump = gen3(simple.net3, 'sentence', 1)
#	for sent in pump : print sent

	import sys
	startLabel = sys.argv[1]
	sentence   = sys.argv[2:]
#	for t in match3(simple.net3, startLabel, 1, sentence) : print "Got one!!", t
	for t in match3(english.net, startLabel, 1, sentence) : print "Got one!!", t
