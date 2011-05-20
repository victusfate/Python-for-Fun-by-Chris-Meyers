#
#  b u c k e t s . p y
#
#  Copyright 2001 by Chris Meyers. 
#
import string, sys

class manager :
    """ Manage game queue. keep track of states already seen
      and who their parent states are"""
    def __init__ (self) :
        self.queue = []
        self.seen  = {}

    def getState (self) :
        "return next state and pop it off the queue"
        
        if not self.queue : return None
        state = self.queue[0]
        self.queue = self.queue[1:]
        return state

    def addState (self, parentState, newState) :
        "add state if it's new. Remember its parent"
        if self.seen.has_key(str(newState)) : return
        self.seen[str(newState)] = str(parentState)
        self.queue.append (newState)
        #print '--- Adding ', newState

    def getSolution (self) :
        "Return solution from latest state added"
        solution = []
        state = self.queue[-1]
        while state :
            solution.append (str(state))
            state = self.getParent(state)
        solution.reverse()
        return solution

    def getParent (self, childState) :
        """return parent of state, if it exists"""
        try    : return self.seen[str(childState)]
        except : return None

class bucketPlayer :
    def __init__ (self, manager) :
        self.manager = manager
    
    def test (self, oldstate, newstate) :
        [newA, newB] = newstate
        won = (newA == self.goal or newB == self.goal)
        self.manager.addState (oldstate, newstate)
        return won

    def playGame (self, aMax, bMax, goal) :
        "grab a state and generate 8 more to submit to the manager"
        self.goal = goal
        self.manager.addState("", [0,0])   # start with 2 empty buckets
        while 1 :
            oldstate = self.manager.getState()
            [aHas,bHas] = oldstate
            if self.test (oldstate, [aMax,bHas]): break # fill A from well
            if self.test (oldstate, [0   ,bHas]): break # empty A to well
            if self.test (oldstate, [aHas,bMax]): break # fill B from well
            if self.test (oldstate, [aHas,0   ]): break # empty B to well
            howmuch = min(aHas, bMax-bHas)
            if self.test (oldstate, [aHas-howmuch,bHas+howmuch]): break # pour A to B
            howmuch = min(bHas, aMax-aHas)
            if self.test (oldstate, [aHas+howmuch,bHas-howmuch]): break # pour B to A
        print "Solution is "
        print string.join (self.manager.getSolution(), "\n")

