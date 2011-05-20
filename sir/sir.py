#!/usr/bin/env python
#
#   s i r . p y
#
import re, sys

debug = 0
facts = []
rules = (
 ( "(every|any|an|a) (.*) is (a|an) (.*)",   lambda g: addFact(g,"1s3|3S1")),
 ( "(.*) is (a|an) (.*)",                    lambda g: addFact(g,"0m2|2M0")),
 ( "(.*) is (.*)",                           lambda g: addFact(g,"0e1|1e0")),
 
 ( "(every|any|an|a) (.*) owns (a|an) (.*)", lambda g: addFact(g,"1p3|3P1")),
 ( "(.*) owns (a|an) (.*)",                  lambda g: addFact(g,"0p2|2P0")),
 ( "(.*) owns (.*)",                         lambda g: addFact(g,"0p1|1P0")),
 
 ( "is (every|an|a) (.*) (a|an) (.*)",       lambda g: getPath(g,"1e*s*3")),
 ( "is (.*) (a|an) (.*)",                    lambda g: getPath(g,"0e*ms*2")),
 ( "does (every|an|a) (.*) own (a|an) (.*)", lambda g: getPath(g,"1e*ms*ps*3")),
 ( "does any (.*) own (a|an) (.*)",          lambda g: getPath(g,"0S*Me*ps*2")),
 ( "does (.*) own (a|an) (.*)",              lambda g: getPath(g,"0e*ms*ps*2")),
 ( "dump",                                   lambda g: dump()              ),
 ( "debug",                                  lambda g: toggleDebug()       ),
 ( "quit",                                   lambda g: sys.exit()          ),
)

def addFact(grp, phrases) :
    global facts
    for p in phrases.split("|") :
        f = (grp[int(p[0])], p[1], grp[int(p[2])])
        if debug : print "  adding fact", f
        facts.append(f)
    print "  I understand"

def matchSent (sent) :
    sent = re.sub("  *"," ",sent.strip().lower())
    for pattern, action in rules :
        match = re.match(pattern, sent)
        if match :
            action(match.groups())
            return
            
def getPath (grp, rule) :
    pattern = rule[1:-1]; start=grp[int(rule[0])]; stop=grp[int(rule[-1])]
    ans = []
    p = path(pattern, start, stop, ans=ans)
    if debug : detail = "%s %s" % (pattern,ans)
    else     : detail = ""
    if ans : print "  Yes", detail
    else   : print "  Not sure", detail

def path (pat, start, end, before={}, ans=[], sofar="", indent=" ") :
    used = {}
    used.update(before)
    if debug : print indent,"path - ",start," to ",end
    if len(indent) > 20 : return
    for fact in facts :
        if used.get(fact) : continue
        a,rel,b = fact
        if  a != start : continue
        sts = okSoFar(pat, sofar+rel)
        if not sts : continue
        used[fact] = 1
        if b == end :
            if sts == 2 : ans.append(sofar+rel)
        else :
            # find inner solutions recursively
            path (pat, b, end, used, ans, sofar+rel, indent+"  ")

def okSoFar (a, b) :
    "return 1 for partial match, 2 for complete match"
    ans = 2
    while a :
        if re.match("^%s$"%a, b) : return ans
        if a[-1] == '*' : a = a[:-2]
        else            : a = a[:-1]
        ans = 1
    return 0

def toggleDebug () :
    global debug
    debug = not debug

def dump () :
    for p,rel,q in facts : print "  %-10s : %s : %s" % (p,rel,q)

def main () :
    sys.stderr = sys.stdout
    for file in sys.argv[1:] :
        if file == '.' : return
        lins = open(file).readlines()
        for lin in lins :
            print lin.strip()
            matchSent (lin)
    while 1 :
        sent = raw_input("? ")
        matchSent(sent)
        
if __name__ == "__main__" : main()
