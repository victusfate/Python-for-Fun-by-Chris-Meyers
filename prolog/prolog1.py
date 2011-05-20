#!/usr/bin/env python
#
#   p r o l o g 1 . p y
#
import sys, copy, re
rules     = []
trace     = 0
goalId    = 100

def fatal (mesg) :
    sys.stdout.write ("Fatal: %s\n" % mesg)
    sys.exit(1)

class Term :
    def __init__ (self, s) :   # expect "x(y,z...)"
        if s[-1] != ')' : fatal("Syntax error in term: %s" % [s])
        flds = s.split('(')
        if len(flds) != 2 : fatal("Syntax error in term: %s" % [s])
        self.args = flds[1][:-1].split(',')
        self.pred = flds[0]

    def __repr__ (self) :
        return "%s(%s)" % (self.pred,",".join(self.args))

class Rule :
    def __init__ (self, s) :   # expect "term-:term;term;..."
        flds = s.split(":-")
        self.head = Term(flds[0])
        self.goals = []
        if len(flds) == 2 :
            flds = re.sub("\),",");",flds[1]).split(";")
            for fld in flds : self.goals.append(Term(fld))

    def __repr__ (self) :
        rep = str(self.head)
        sep = " :- "
        for goal in self.goals :
            rep += sep + str(goal)
            sep = ","
        return rep
        
class Goal :
    def __init__ (self, rule, parent=None, env={}) :
        global goalId
        goalId += 1
        self.id = goalId
        self.rule = rule
        self.parent = parent
        self.env = copy.deepcopy(env)
        self.inx = 0      # start search with 1st subgoal

    def __repr__ (self) :
        return "Goal %d rule=%s inx=%d env=%s" % (self.id,self.rule,self.inx,self.env)

def main () :
    for file in sys.argv[1:] :
        if file == '.' : return    # early out. no user interaction
        procFile(open(file),'')    # file on the command line
    procFile (sys.stdin,'? ')      # let the user have her say

def procFile (f, prompt) :
    global rules, trace
    env = []
    while 1 :
        if prompt :
            sys.stdout.write(prompt)
            sys.stdout.flush()
        sent = f.readline()
        if sent == "" : break
        s = re.sub("#.*","",sent[:-1])   # clip comments and newline
        s = re.sub(" ", "",s)           # remove spaces
        if s == "" : continue

        if s[-1] in '?.' : punc=s[-1]; s=s[:-1]
        else             : punc='.'

        if   s == 'trace=0' : trace = 0
        elif s == 'trace=1' : trace = 1
        elif s == 'quit'    : sys.exit(0)
        elif s == 'dump'  :
            for rule in rules : print rule
        elif punc == '?' : search(Term(s))
        else             : rules.append(Rule(s))

# A Goal is a rule in at a certain point in its computation. 
# env contains definitions (so far), inx indexes the current term
# being satisfied, parent is another Goal which spawned this one
# and which we will unify back to when this Goal is complete.
#

def unify (srcTerm, srcEnv, destTerm, destEnv) :
    "update dest env from src. return true if unification succeeds"
    nargs = len(srcTerm.args)
    if nargs        != len(destTerm.args) : return 0
    if srcTerm.pred != destTerm.pred      : return 0
    for i in range(nargs) :
        srcArg  = srcTerm.args[i]
        destArg = destTerm.args[i]
        if srcArg <= 'Z' : srcVal = srcEnv.get(srcArg)
        else             : srcVal = srcArg
        if srcVal :    # constant or defined Variable in source
            if destArg <= 'Z' :  # Variable in destination
                destVal = destEnv.get(destArg)
                if not destVal : destEnv[destArg] = srcVal  # Unify !
                elif destVal != srcVal : return 0           # Won't unify
            elif     destArg != srcVal : return 0           # Won't unify
    return 1

def search (term) :
    global goalId
    goalId = 0
    if trace : print "search", term
    goal = Goal(Rule("got(goal):-x(y)"))      # Anything- just get a rule object
    goal.rule.goals = [term]                  # target is the single goal
    if trace : print "stack", goal
    stack = [goal]                            # Start our search
    while stack :
        c = stack.pop()        # Next goal to consider
        if trace : print "  pop", c
        if c.inx >= len(c.rule.goals) :       # Is this one finished?
            if c.parent == None :             # Yes. Our original goal?
                if c.env : print  c.env       # Yes. tell user we
                else     : print "Yes"        # have a solution
                continue
            parent = copy.deepcopy(c.parent)  # Otherwise resume parent goal
            unify (c.rule.head,                  c.env,
                   parent.rule.goals[parent.inx],parent.env)
            parent.inx = parent.inx+1         # advance to next goal in body
            if trace : print "stack", parent
            stack.append(parent)              # let it wait its turn
            continue

        # No. more to do with this goal.
        term = c.rule.goals[c.inx]            # What we want to solve
        for rule in rules :                     # Walk down the rule database
            if rule.head.pred      != term.pred      : continue
            if len(rule.head.args) != len(term.args) : continue
            child = Goal(rule, c)               # A possible subgoal
            ans = unify (term, c.env, rule.head, child.env)
            if ans :                            # if unifies, stack it up
                if trace : print "stack", child
                stack.append(child)

if __name__ == "__main__" : main ()
