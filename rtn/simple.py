#  S i m p l e . p y
#
#
END = None

net1 = {
 'sentence': {
         1: (("red",  2),    ),
         2: (("book", END), )
         }
}

net2 = {
 'sentence': {
         1: (("red", 2), ),
         2: (("red", 2), ("book", END))
         }
}

net3 = {
 'sentence': {
         1: (('adjective', 2), ),
         2: (('noun'  ,  END), )
         },

 'noun'  : {
         1: (("book",END),("table",END),("top",END),("cover",END))
         },

 'adjective': {
         1: (("big",END),("small",END),("red",END))
         }
}

