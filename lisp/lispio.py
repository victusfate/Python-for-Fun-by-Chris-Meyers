#!/usr/local/bin/python
#
#   l i s p i o . p y
#
#   Copyright 2001 by Chris Meyers. 
#
import string, sys

inputter = None
inlin = ""

def putSexp (s):
    "return string form of an S expression"
    if type(s) == type([]) :
        if 0 and len(s) and s[0] == 'quote' : return "'" + putSexp(s[1:])
        else : return '(' + string.join(map(putSexp,s)) + ')'
    else : return str(s)

def getSexp () :       # get an S expression from the user
    "return and discard the next S expression, along with any nested ones in input"
    a = getToken()
    if   a == "'" : return ['quote', getSexp()]
    elif a != '(' : return a
    a = []
    while 1 :
        b = getSexp()
        if b == ')' : return a
        a.append(b)

def getToken () :
    "return and discard the next symbol, number or special character in input"
    while nextChar() <= ' ': getChar()  # skip whitespace
    a = getChar()
    if a in ['(',')',"'"] : return a
    while nextChar() > ' ' and nextChar() not in ['(',')'] :
        a = a + getChar()
    try    : return float(a)   # if a number, make it a float
    except : return a          # otherwise a string with the symbol name
        
def nextCharOld() :
    """return (but don't discard) the next character in the input stream
       get more from the user if needed"""
    global inlin
    if inlin == "" : inlin = raw_input("Lisp>") + '\n'
    return inlin[0:1]
    
def nextChar() :
    """return (but don't discard) the next character in the input stream
       get more from the user if needed"""
    global inlin, inputter
    if not inputter :
        import userInput
        inputter = userInput.InputString()
    if inlin == "" : 
        inlin = inputter.get("Lisp>")
        if inlin == "" : raise "EOF error"
    return inlin[0:1]
    
def getChar() :
    """return and discard the next character in the input stream"""
    global inlin
    c = nextChar()
    inlin = inlin[1:]
    return c
    
