#!/usr/bin/python
#
#       s i m u l a t o r . p y
#
import sys, string
panel = """
               The Mythical Machine
 
        P reg  000000       I reg 000000
                      
        reg 0  000000       reg 5 000000
        reg 1  000000       reg 6 000000
        reg 2  000000       reg 7 000000
        reg 3  000000       reg 8 000000
        reg 4  000000       reg 9 000000
"""
# loc has row/column information for each register
loc = {'pReg': (3, 15), 'iReg': (3, 34)}
mem = [0]*1000       # 1000 words of main memory
reg = [0]*10         # 10 General registers (0-9)

# tell loc[] where to write each general register in "panel"
for i in range(0,5) : loc["r%d"%i] = (5+i,15)
for i in range(5,9) : loc["r%d"%i] = (0+i,34)

confirm=1

def updatePanel (r, value) :
    "update screen with new value for register r"
    (x,y) = loc[r]
    print "\033[%d;%dH%06d" % (x+1,y+1,value),

def pause (msg) :
    "If confirm true, make user hit the return key to continue"
    global confirm
    if not confirm : return
    ans = raw_input("\033[18;10H\033[0K%s" % msg)
    if ans[0:1] in ('a','A') : confirm=0

def cycle () :
    global pReg, iReg, reg, mem
    # retrieve next instruction to the Ireg
    pause ("About to Retrieve Instruction: ")
    iReg = mem[pReg]; updatePanel('iReg', iReg);

    # execute instruction
    pause ("About to Execute Instruction: ")
    pReg = pReg + 1 ; updatePanel('pReg', pReg);
    opcode = (iReg/10000)            # break instruction into its pieces
    r      = (iReg/1000) % 10
    addr   = (iReg) % 1000
    if   opcode == 0 : return 0                  # stop instruction
    elif opcode == 1 : reg[r]=mem[addr]          # load register
    elif opcode == 2 : mem[addr]=reg[r]          # store register
    elif opcode == 3 : reg[r]=addr               # load register immediate
    elif opcode == 4 : reg[r]=mem[reg[addr]]     # load register indexed
    elif opcode == 5 : reg[r]=reg[r]+reg[addr]   # add register
    elif opcode == 6 : reg[r]=reg[r]-reg[addr]   # sub register
    elif opcode == 7 : reg[r]=reg[r]*reg[addr]   # mul register
    elif opcode == 8 : reg[r]=reg[r]/reg[addr]   # div register
    elif opcode ==10 :
        pReg=addr; updatePanel('pReg',pReg)      # jump unconditionally
    elif opcode ==11 :
        if reg[r]==0 :
            pReg=addr; updatePanel('pReg',pReg)  # jump if register zero
    updatePanel("r%d" % r, reg[r])               # the register affected
    return 1

def loadProgram (file) :
    global pReg, iReg, reg, mem
    fil = open (file,"r")    # file with machine code
    while 1 :
        lin = fil.readline()
        if lin == "" : break
        if lin[0] < '0' : continue   # a comment
        try :
            flds = string.split(lin)
            address = int(flds[0])
            instruc = int(flds[1])
            mem[address] = instruc
        except : pass
    fil.close()

def main () :
    global pReg, iReg, reg, mem
    loadProgram(sys.argv[1])
    print "\033[1;1H\033[0J%s" % panel
    pReg = 100
    updatePanel('pReg', pReg)
    while 1 :
        if not cycle() : break
    print "\033[20;1H"  # Get low on the screen and exit

if __name__ == "__main__" : main()
