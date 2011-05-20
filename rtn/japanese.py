#
#  j a p a n e s e . p y
#
	
net = {
	':noun1':  {
		#     book         table          top
		1: (("hon",None), ("taberu",None),("ue",None), )
		},
	
	':adjective':  {
		#    big            red
		1: (("ookii",None), ("akai",None), )
		},
	
	':preposition':  {
		#    on          of
		1: (("ni",None), ("no",None), )
		},
	
	':noun2':  {
		1: ((':adjective', 1), (':noun1', None), )
		},
	
	':prepPhrase':  {
		1: ((':noun2', 2), ),
		2: ((':preposition', None), )
		},
	
	':noun3':  {
		1: ((':noun2', None), (':prepPhrase', 1), ),
		2: ((':noun2', None), )
		},
}

