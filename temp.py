def func(x):
	# Write n(x) function here in Python-stye. For example:
	if x > 62:
	    n = 35*exp(-(x-62)/1.2)
	else:
	    n = 0
	# Consider that you are just writing some func(x) that returns n value.
	#Note that n truncates to int in the end; x can be float.
	# Be careful, python-injections are posiible as this code interpreting
	# in program without any checks and changes.
	return int(n)