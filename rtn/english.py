#
#  e n g l i s h . p y
#
END = None

net = {
	":noun1": {
		1: (("book",END),("table",END),("top",END),("cover",END))
		},

	":article": {
		1: (("the",END),("a",END),("an",END))
		},

	":adjective": {
		1: (("big",END),("small",END),("red",END))
		},

	":preposition": {
		1: (("on",END),("of",END),("in",END),("with",END))
		},

	":noun2": {
		1: ((":article", 2), ("",2)),
		2: ((":adjective", 2), (":noun1", END))
		},

	":prepPhrase": {
		1: ((":preposition", 2), ),
		2: ((":noun3", END), )
		},

	":noun3": {
		1: ((":noun2", END), (":noun2", 2)),
		2: ((":prepPhrase", END), (":prepPhrase", 2))
		},
}

