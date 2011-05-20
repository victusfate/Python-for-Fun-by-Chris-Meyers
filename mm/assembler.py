#!/usr/bin/python
#
#    a s s e m b l e r . p y
#
import sys, string

codes={"hlt":0, "ld":1, "sto":2, "ld#":3, "ldi":4, "add":5, "sub":6, 
       "mul":7, "div":8, "jmp":10, "jz":11}

lookup={"r0":0,"r1":1,"r2":2,"r3":3,"r4":4,"r5":5,"r6":6,"r7":7,"r8":8,"r9":9}

def getVal (s) :
    "return numeric value of a symbol or number"
    if not s : return 0       # Empty symbol - zero
    a = lookup.get(s)         # Get value or None if not in lookup
    if a == None : return int(s)  # Just a number
    else         : return a

def pass1 (program) :
    "determine addresses for labels and add to the lookup dictionary"
    global lookup
    pReg= 100
    for lin in program :
        flds = string.split(lin)
        if not flds : continue        # just an empty line
        if lin[0] > ' ' :
            symb = flds[0]            # A symbol. Save its address in lookup
            lookup[symb] = pReg
            if len(flds) > 1 :        # Advance program counter unless only a symbol
                pReg = pReg + 1
        else : pReg = pReg + 1

def assemble (flds) :
    "assemble instruction to machine code"
    opval = codes.get(flds[0])
    if opval == None : return int(flds[0])     # just a number
    if opval ==    0 : return 0                # Halt. no address
    parts  = string.split(flds[1],",")         # see if reg,address
    if len(parts) == 1 : parts = [0,parts[0]]  # No register means 0
    return opval*10000 + getVal(parts[0])*1000 + getVal(parts[1])

def pass2 (program) :
    "translate assembly code and symbols to machine code"
    pReg= 100
    for lin in program :
        flds = string.split(lin)
        if lin[0] > ' ' : flds = flds[1:]     # drop symbol if there is one
        if not flds : print "            ", lin,   # print now if only a symbol
        else :
            try :
                instruction = assemble(flds)
                print "%03d %06d   %s" % (pReg, instruction, lin),
                pReg = pReg + 1
            except :
                print "*** ******   %s" % lin,

def main () :
    program = sys.stdin.readlines()
    pass1 (program)
    pass2 (program)

if __name__ == "__main__" : main ()
