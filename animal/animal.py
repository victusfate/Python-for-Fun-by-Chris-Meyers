#
#  A n i m a l . p y
#
#  Copyright 2001 by Chris Meyers. 
#
import string

class node :
    "Node objects have a question, and  left and right pointer to other nodes"
    def __init__ (self, question, left=None, right=None) :
        self.question = question
        self.left     = left
        self.right    = right

def yes (ques) :
    "Force the user to answer "yes" or "no" or something similar. Yes returns true"
    while 1 :
        ans = raw_input (ques)
        ans = string.lower(ans[0:1])
        if ans == 'y' : return 1
        else          : return 0

knowledge = node("bird")

def main () :
    "Guess the animal. Add a new node for a wrong guess."

    while 1 :
        print
        if not yes("Are you thinking of an animal? ") : break
        p = knowledge
        while p.left != None :
            if yes(p.question+"? ") : p = p.right
            else                    : p = p.left
    
        if yes("Is it a " + p.question + "? ") : continue
        animal   = raw_input ("What is the animals name? ")
        question = raw_input ("What question would distinguish a %s from a %s? "
                                            % (animal,p.question))
        p.left     = node(p.question)
        p.right    = node(animal)
        p.question = question
    
        if not yes ("If the animal were %s the answer would be? " % animal) :
            (p.right, p.left) = (p.left, p.right)

if __name__ == "__main__" : main ()
