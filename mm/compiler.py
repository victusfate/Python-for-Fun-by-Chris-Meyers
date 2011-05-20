#!/usr/bin/python
#
#   c o m p i l e r . p y
#
import re, sys
from string import split, letters, digits, strip, join

nextLabel = 1
vars = {}

def search (a,b) :
	"return index of b within a or -1"
	match = re.search(a,b)
	if match : return match.start()
	else     : return -1

def getToken (prog) :
    "extract next word, number or symbol. return it and rest of prog"
    prog = strip(prog)                         # remove leading whitespace
    if prog == "" : return ['','']             # if no more prog then no token
    if prog[0] in letters :                    # a symbol
        p = search('[^a-zA-z0-9]',prog)        # search for non-alphanumeric
        if p < 0 : return [prog,""]            # return the very last token
        else     : return [prog[:p],prog[p:]]  # or the next alphanumeric token
    elif prog[0] in digits :
        p = search('[^0-9]',prog)              # find first non-numeric
        if p < 0 : return [prog,""]            # return the very last token
        else     : return [prog[:p],prog[p:]]  # or the next numeric token
    else : return [prog[0], prog[1:]]          # or the next (non-alpha) token

def getStat (prog, reg) :
    global nextLabel, vars
    [token, rest] = getToken(prog)          # get statement keyword if any
    if not token : return ['','']           # return if we're all done
    if token == "while" :
        [code1,rest] = getExpr(rest,reg)    # get true/false code to reg
        [code2,rest] = getStat (rest, reg+1) # get main body to next reg

        l1=nextLabel; l2=nextLabel+1; nextLabel=nextLabel+2
        code = "z%d\n%s  jz  r%d,z%d\n%s  jmp  z%d\nz%d\n" % \
                            (l1,code1,reg,l2,code2,l1,l2)
        return [code, rest]
    elif token == "{" :                 # a compound statement. inside {}
        code = ""
        while 1 :
            [tok,rest1] = getToken(rest)    # get statments until "}"
            if not tok    : return ['','']
            if tok == '}' : return [code,rest1]
            [code1,rest] = getStat(rest,reg)
            code = code + code1
    else :
        [second,rest1] = getToken(rest)        # assignment ?
        if second == '=' :
            [code,rest] = getExpr (rest1, reg)
            vars[token] = 1               # remember variable name
            return [code+'  sto r%d,%s\n' % (reg,token), rest]
        else : return getExpr (prog, reg)
    
def getExpr (prog, reg) :
    global nextLabel
    [code1,rest] = getTerm (prog, reg)
    if not code1 : return ['','']
    [opcode,rest1] = getToken(rest)
    if opcode in ['+','*','-','/'] :
        # Use next higher register for 2nd expression
        [code2, rest] = getExpr (rest1, reg+1)
        if opcode == '+' :
            code = '  add r%d,r%d\n' % (reg,reg+1)
        if opcode == '-' :
            code = '  sub r%d,r%d\n' % (reg,reg+1)
        if opcode == '*' :
            code = '  mul r%d,r%d\n' % (reg,reg+1)
        if opcode == '/' :
            code = '  div r%d,r%d\n' % (reg,reg+1)
        return [code1+code2+code, rest]
    else : return [code1, rest]

def getTerm (prog, reg) :
    "Extract number, variable, or nested expression"
    [token, rest] = getToken(prog)    # peek at the first token
    if not token : return ['','']
    if token == "(" :                        # a nested expression
        [code,rest] = getExpr(rest, reg)     # go get it and just make
        if not code : return ['','']
        [token,rest] = getToken(rest)        # make sure closes with ")"
        if token != ")" : return ['','']
        else            : return [code,rest]
    elif token < 'A' :     # got a number - just load to register
        return ['  ld# r%d,%s\n' % (reg,token), rest]
    else :
        return ['  ld  r%d,%s\n' % (reg, token), rest]   # load a variable

def main () :
    "compile program from command line or standard input"
    if len(sys.argv) < 2 : program = sys.stdin.read()
    else                 : program = sys.argv[1]
    rest = program
    while rest :
        [code,rest] = getStat(rest, 0)
        print code,
    print "  hlt"                # End of program. Allocations for vars
    for var in vars.keys():
        print var,0              # Output each var to get a word of memory

if __name__ == "__main__" : main()
